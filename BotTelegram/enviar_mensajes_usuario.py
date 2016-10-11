import json
import shutil
from os.path import exists
from os.path import splitext
from random import random

import datetime

from django.core.exceptions import ObjectDoesNotExist

from BotTelegram.models import Usuario, RespuestaServidor, Imagen
import requests
from time import sleep
from django.utils import timezone
from PIL import Image, ImageDraw, ImageFont

# Fuente usada para escribir sobre los memes
FUENTE = "staticfiles/ufonts.com_impact.ttf"

# Codigo del BOT dado por el API de Telegram -- Token
CODE_BOT = "119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg"

# URL para acceder al API de Telegram
URL_TG_API = "https://api.telegram.org/bot" + CODE_BOT + "/"


def responder_callback_query(query_id):
    return requests.get(URL_TG_API + 'answerCallbackQuery', params={'callback_query_id': query_id})


def obtener_info_webhook():
    return requests.get(URL_TG_API + 'getWebhookInfo')


def obtener_info_me():
    return requests.get(URL_TG_API + 'getMe')

def mostrar_accion(chat_id,accion):
    return requests.get(URL_TG_API + 'sendChatAction', params={'chat_id': chat_id, 'action': accion})


def enviar_mensaje_usuario(chat_id, mensaje, reply_markup=None):

    params = {'chat_id': chat_id, 'text': mensaje}

    if reply_markup:
        params["reply_markup"] = json.dumps(reply_markup)

    mostrar_accion(chat_id,"typing")
    requests.get(URL_TG_API + 'sendMessage', params=params)


# Envia un mensaje a todos los usuarios del bot
def enviar_mensaje_usuarios(mensaje):
    usuarios = Usuario.objects.all()

    for usuario in usuarios:
        if usuario.is_suscrito_actu:
            enviar_mensaje_usuario(usuario.pk, mensaje)
            sleep(5)


# envia una imagen a un chat
# notar que primero se debe guardar la imagen localmente
def enviar_imagen(chat_id, imagen, reply_markup=None):
    # Colocamos el estado en el bot "subiendo foto"

    requests.get(URL_TG_API + 'sendChatAction', params={'chat_id': chat_id, 'action': 'upload_photo'})

    guardar_imagen(imagen)
    return enviar_mensaje_imagen(chat_id, imagen.ruta_imagen, imagen.title, reply_markup)


def enviar_mensaje_imagen(chat_id, ruta_foto, caption="", reply_markup=None):
    files = {'photo': open(ruta_foto, 'rb')}

    data_message = {'chat_id': chat_id}

    if reply_markup:
        data_message["reply_markup"] = json.dumps(reply_markup)

    if caption:
        data_message["caption"] = caption
    try:
        requests.get(URL_TG_API + 'sendChatAction', params={'chat_id': chat_id, 'action': 'upload_photo'})
        r = requests.post(
            URL_TG_API + "sendPhoto",
            data=data_message,
            files=files
        )
    except:
        return -1

    if r.status_code != 200:
        print r.text
        return -1

    respuesta = json.loads(r.text)
    if not respuesta["ok"]:
        print r.text
        return 1

    return 0


def borrar_cache_espera(usuario):
    if usuario.datos_imagen_borrador:
        usuario.datos_imagen_borrador.delete()
        usuario.save()

    usuario.comando_en_espera = "None"

    usuario.save()


# Parsea el string guardado en el archivo xml strings.xml
# construyendo el mensaje en un formato entendible por la api de TG
def enviar_mensaje_ayuda_comando(chat_id, comando, root_xml):
    elemento_ayuda = root_xml.findall("help[@comando='{0}']".format(comando))

    if elemento_ayuda:
        elemento_ayuda = elemento_ayuda[0]

        parsear_enviar_xml(chat_id, elemento_ayuda)


def parsear_xml_object(xml_object):
    if not xml_object: return

    result = {"text": "", "botones": []}

    for sub_elemento in list(xml_object):
        if sub_elemento.tag == "text":
            result["text"] += sub_elemento.text
        elif sub_elemento.tag == "button":
            result["botones"].append([sub_elemento.attrib])  # De esta forma quedan uno debajo del otro

    return result


# Parsea un xml object y lo envia en formato de la API de Telegram
def parsear_enviar_xml(chat_id, xml_object):
    result = parsear_xml_object(xml_object)
    if not result: return
    mark_keyboard = {}

    if result["botones"]:
        mark_keyboard = {"inline_keyboard": result["botones"]}

    enviar_mensaje_usuario(chat_id, result["text"], mark_keyboard)


# Si no existe la imagen en el servidor
# la guarda en la ruta especificada
def guardar_imagen(imagen):
    if not exists(imagen.ruta_imagen):
        resp = requests.get(imagen.url_imagen, stream=True)

        with open(imagen.ruta_imagen, 'wb') as archivo_img:
            shutil.copyfileobj(resp.raw, archivo_img)

def obtener_upper_lower_text(texto):

    mensajes = texto.split("-")

    upper_text = ""
    lower_text = ""

    if len(mensajes) == 1:
        lower_text = mensajes[0]
    else:
        upper_text = mensajes[0]
        lower_text = mensajes[1]

    return upper_text, lower_text

def escribir_enviar_meme(chat_id, upper_text , lower_text, color, ruta_imagen, mark_keyboard= None):
    imagen_pil = Image.open(ruta_imagen)
    draw_pil = ImageDraw.Draw(imagen_pil)

    dibujar_texto_sobre_imagen(upper_text, draw_pil, imagen_pil, (lambda td, sz: sz[0] // 12), color)
    dibujar_texto_sobre_imagen(lower_text, draw_pil, imagen_pil, (lambda td, sz: sz[1] - td[1] - td[1] // 2), color)

    ruta_tu = splitext(ruta_imagen)
    ruta_guardar = ruta_tu[0] + str(random())[2:] + ".PNG"

    imagen_pil.save(ruta_guardar, quality=100)
    enviar_mensaje_imagen(chat_id, ruta_guardar, reply_markup=mark_keyboard)


def dibujar_texto_sobre_imagen(texto, image_draw, image, fposiciony, color):
    if texto == "": return

    shadowcolor = "black"
    ancho_imagen, alto_imagen = image.size

    fuente = ImageFont.truetype(FUENTE, alto_imagen // 7)

    # Calculamos el ancho de la fuente para que sea adecuada a la imagen
    ancho_texto, alto_texto = image_draw.textsize(texto, font=fuente)
    while ancho_texto + image.size[0] // 2 - ancho_texto // 2 > image.size[0]:
        del fuente
        alto_imagen -= 2
        fuente = ImageFont.truetype(FUENTE, alto_imagen)
        ancho_texto, alto_texto = image_draw.textsize(texto, font=fuente)

    x = ancho_imagen // 2 - ancho_texto // 2
    y = fposiciony((ancho_texto, alto_texto), image.size)
    p = 2

    # thin border
    image_draw.text((x - p, y), texto, font=fuente, fill=shadowcolor)
    image_draw.text((x + p, y), texto, font=fuente, fill=shadowcolor)
    image_draw.text((x, y - p), texto, font=fuente, fill=shadowcolor)
    image_draw.text((x, y + p), texto, font=fuente, fill=shadowcolor)

    # thicker border
    image_draw.text((x - p, y - p), texto, font=fuente, fill=shadowcolor)
    image_draw.text((x + p, y - p), texto, font=fuente, fill=shadowcolor)
    image_draw.text((x - p, y + p), texto, font=fuente, fill=shadowcolor)
    image_draw.text((x + p, y + p), texto, font=fuente, fill=shadowcolor)

    # now we image_draw the text over it
    image_draw.text((x, y), texto, font=fuente, fill=color)


def guardar_imagen_enviada(datetime_unix, usuario_m, image):
    if datetime_unix:
        datetime_d = datetime.datetime.utcfromtimestamp(int(datetime_unix))
    else:
        datetime_d = datetime.datetime.now()

    # creamos la respuesta
    respuesta = RespuestaServidor(
        fecha=timezone.make_aware(
            datetime_d,
            timezone.get_default_timezone()
        ),
        usuario_t=usuario_m,
        imagen_enviada=image
    )

    # Actualizamos el usuario
    if usuario_m.ultima_respuesta:
        usuario_m.ultima_respuesta.delete()

    respuesta.save()  # Guardamos en la BD

    usuario_m.ultima_respuesta = respuesta
    usuario_m.save()

# coding=utf-8
from os.path import exists
from os.path import splitext
from random import random
from BotTelegram.models import Usuario, Imagen
from time import sleep
from django.utils import timezone
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
import requests
import logging
import datetime
import json
import shutil

# Fuente usada para escribir sobre los memes
FUENTE = "staticfiles/ufonts.com_impact.ttf"

# Codigo del BOT dado por el API de Telegram -- Token
CODE_BOT = "119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg"

# URL para acceder al API de Telegram
URL_TG_API = "https://api.telegram.org/bot" + CODE_BOT + "/"

logger = logging.getLogger("BotTelegram.request_api_tg.error_request")
logger_xml = logging.getLogger("BotTelegram.error_xml")


def responder_callback_query(query_id,text = "",show_alert = False):

    params = {'callback_query_id': query_id,"show_alert":show_alert}

    if text:
        params["text"] = text

    return requests.get(URL_TG_API + 'answerCallbackQuery', params=params)


def obtener_info_webhook():
    return requests.get(URL_TG_API + 'getWebhookInfo')


def obtener_info_me():
    return requests.get(URL_TG_API + 'getMe')


def request_get_api_telegram(url, params):
    respuesta = requests.get(url, params=params)

    if respuesta.status_code != 200:
        logear_error(url,params,respuesta.text)


def enviar_mensaje_usuario(chat_id, mensaje, reply_markup=None):
    params = {'chat_id': chat_id, 'text': mensaje}

    if reply_markup:
        params["reply_markup"] = json.dumps(reply_markup)

    request_get_api_telegram(URL_TG_API + 'sendChatAction', {'chat_id': chat_id, 'action': "typing"})
    request_get_api_telegram(URL_TG_API + 'sendMessage', params)


# Envia un mensaje a todos los usuarios del bot
def enviar_mensaje_usuarios(mensaje):
    usuarios = Usuario.objects.all()

    for usuario in usuarios:
        if usuario.is_suscrito_actu:
            enviar_mensaje_usuario(usuario.pk, mensaje)
            sleep(5)


def logear_error(url, parametros, text):
    datos_error = "Request :" + url + "\n" + \
                  "con los parametros:" + str(parametros) + "\n" + \
                  "Respuesta:" + text

    logger.error(datos_error)

    if settings.DEBUG:
        ## Notar que es para forzar que falle un caso de prueba
        raise Exception("Error en request a telegram: \n" + datos_error)


# envia una imagen a un chat
# notar que primero se debe guardar la imagen localmente
def enviar_imagen(chat_id, imagen, reply_markup=None):
    # Colocamos el estado en el bot "subiendo foto"

    request_get_api_telegram(URL_TG_API + 'sendChatAction',{'chat_id': chat_id, 'action': 'upload_photo'})
    guardar_imagen(imagen)
    return enviar_mensaje_imagen(chat_id, imagen.ruta_imagen, imagen.title, reply_markup)


def enviar_mensaje_imagen(chat_id, ruta_foto, caption="", reply_markup=None):
    #print "e.1 ruta_foto: " + ruta_foto
    files = {'photo': open(ruta_foto, 'rb')}

    #print "e.2"
    data_message = {'chat_id': chat_id}

    if reply_markup:
        data_message["reply_markup"] = json.dumps(reply_markup)

    if caption:
        data_message["caption"] = caption

    #print "e.3"
    request_get_api_telegram(URL_TG_API + 'sendChatAction',  {'chat_id': chat_id, 'action': 'upload_photo'})

    #print "e.4"
    url = URL_TG_API + 'sendPhoto'
    r = requests.post(
        URL_TG_API + "sendPhoto",
        data=data_message,
        files=files
    )
    #print "e.5"

    if r.status_code != 200:
        logear_error(url, "", r.text)
        return -1
    #print "e.6"

    respuesta = json.loads(r.text)
    if not respuesta["ok"]:
        logear_error(url,"", r.text)
        return 1
    #print "e.7"

    return 0

def obtener_xml_objeto(tag,xml_string):
    objeto_xml_texto = xml_string.find(tag)

    if objeto_xml_texto is None:
        logger_xml.error("No se encontró TEXTO para " + tag)

        if settings.DEBUG:
            # Forzamos el error
            raise Exception("Error XML")

    return objeto_xml_texto

## El bot puede quedarse esperando la respuesta de un usuario a un comando
# o una iteraccion de el.
# Esta funcion, debe resetear el estado del usuario al inicial cuando comenzo por primera vez el bot.
def borrar_cache_espera(usuario):

    usuario.esta_creando_meme = False
    usuario.comando_en_espera = "None"
    usuario.save()

# Parsea un xml object y lo envia en formato de la API de Telegram
def parsear_enviar_xml(chat_id, xml_object):
    result = parsear_xml_object(xml_object)

    if result is None: return False

    mark_keyboard = {}

    if result["botones"]:
        mark_keyboard = {"inline_keyboard": result["botones"]}

    enviar_mensaje_usuario(chat_id, result["text"], mark_keyboard)

# Parsea el string guardado en el archivo xml strings.xml
# construyendo el mensaje en un formato entendible por la api de TG
def enviar_mensaje_ayuda_comando(chat_id, comando, xml_string):
    elemento_ayuda = xml_string.findall("help[@comando='{0}']".format(comando))

    if elemento_ayuda:
        elemento_ayuda = elemento_ayuda[0]

        parsear_enviar_xml(chat_id, elemento_ayuda)

    else:
        parsear_enviar_xml(chat_id, xml_string.find("no_hay_ayuda_para_ese_tema"))


def parsear_xml_object(xml_object):
    if xml_object is None: return

    result = {"text": "", "botones": []}

    for sub_elemento in list(xml_object):
        if sub_elemento.tag == "text":
            result["text"] += sub_elemento.text
        elif sub_elemento.tag == "button":
            result["botones"].append([sub_elemento.attrib])  # De esta forma quedan uno debajo del otro

    if result["text"] == "":
        logger_xml.warning("Objeto " + str(xml_object) + " no tiene texto")

    return result





def guardar_url_archivo(url_archivo,ruta_guardar):
    resp = requests.get(url_archivo, stream=True)

    import os
    print os.path.dirname(os.path.abspath(__file__))
    with open(ruta_guardar, 'wb') as archivo:
        shutil.copyfileobj(resp.raw, archivo)

# Si no existe la imagen en el servidor
# la guarda en la ruta especificada
def guardar_imagen(imagen):
    if not exists(imagen.ruta_imagen):
        guardar_url_archivo(imagen.url_imagen,imagen.ruta_imagen)


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


def escribir_enviar_meme(chat_id, upper_text, lower_text, color, ruta_imagen, mark_keyboard=None):
    #print "es.1"

    imagen_pil = Image.open(ruta_imagen)
    #print "es.2"
    draw_pil = ImageDraw.Draw(imagen_pil)
    #print "es.3"

    dibujar_texto_sobre_imagen(upper_text, draw_pil, imagen_pil, (lambda td, sz: sz[0] // 12), color)
    #print "es.4"
    dibujar_texto_sobre_imagen(lower_text, draw_pil, imagen_pil, (lambda td, sz: sz[1] - td[1] - td[1] // 2), color)
    #print "es.5"

    #print "es.6"
    ruta_tu = splitext(ruta_imagen)
    #print "es.7"
    ruta_guardar = ruta_tu[0] + str(random())[2:] + ".PNG"
    #print "es.8"

    #print "es.9"
    imagen_pil.save(ruta_guardar, quality=100)
    #print "es.10"
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


def guardar_imagen_respuesta_servidor(datetime_unix, usuario_m, image,guardar_usuario = True):
    if datetime_unix:
        datetime_d = datetime.datetime.utcfromtimestamp(int(datetime_unix))
    else:
        datetime_d = datetime.datetime.now()

    #print "g.3"

    usuario_m.imagen_actual = image
    usuario_m.fecha_ultima_respuesta = timezone.make_aware(
            datetime_d,
            timezone.get_default_timezone()
        )
    #print "g.6"

    if guardar_usuario:
        usuario_m.save()

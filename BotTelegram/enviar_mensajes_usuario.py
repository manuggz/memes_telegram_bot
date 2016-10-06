import json
import shutil
from os.path import exists
from os.path import splitext
from random import random

import datetime

from BotTelegram.models import Usuario, RespuestaServidor
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


def enviar_mensaje_usuario(chat_id, mensaje):
    requests.get(URL_TG_API + 'sendChatAction', params={'chat_id': chat_id, 'action': 'typing'})
    requests.get(URL_TG_API + 'sendMessage', params={'chat_id': chat_id, 'text': mensaje})


# Envia un mensaje a todos los usuarios del bot
def enviar_mensaje_usuarios(mensaje):
    usuarios = Usuario.objects.all()

    for usuario in usuarios:
        if usuario.suscrito_actu:
            enviar_mensaje_usuario(usuario.pk, mensaje)


# envia una imagen a un chat
# notar que primero se debe guardar la imagen localmente
def enviar_imagen(chat_id, imagen, reply_markup=None):
    guardar_imagen(imagen)
    return enviar_mensaje_imagen(chat_id, imagen.ruta_imagen, reply_markup)


def enviar_mensaje_imagen(chat_id, ruta_foto, reply_markup=None):
    files = {'photo': open(ruta_foto, 'rb')}

    data_message = {'chat_id': chat_id}

    if reply_markup:
        data_message["reply_markup"] = json.dumps(reply_markup)

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


# Envia una cadena de texto asociada a un comando
def enviar_mensaje_ayuda_comando(comando, chat_id, xml_string):
    for help_m in xml_string.iter("help"):
        if help_m.attrib.get("comando", "") == comando:
            enviar_mensaje_usuario(chat_id, help_m.text)
            return


# Si no existe la imagen en el servidor
# la guarda en la ruta especificada
def guardar_imagen(imagen):
    if not exists(imagen.ruta_imagen):
        resp = requests.get(imagen.url_imagen, stream=True)

        with open(imagen.ruta_imagen, 'wb') as archivo_img:
            shutil.copyfileobj(resp.raw, archivo_img)


def escribir_enviar_meme(comandos, imagen, chat_id, usuario_m):
    guardar_imagen(imagen)

    imagen_pil = Image.open(imagen.ruta_imagen)
    draw_pil = ImageDraw.Draw(imagen_pil)

    mensajes = comandos[1].split("-")
    tup = ""
    tdown = ""
    if len(mensajes) == 1:
        tdown = mensajes[0]
    else:
        tup = mensajes[0]
        tdown = mensajes[1]

    try:
        color = comandos[2]
    except IndexError:
        color = "red"

    dibujar_texto_sobre_imagen(tup, draw_pil, imagen_pil, (lambda td, sz: sz[0] // 12), color)
    dibujar_texto_sobre_imagen(tdown, draw_pil, imagen_pil, (lambda td, sz: sz[1] - td[1] - td[1] // 2), color)
    ruta_tu = splitext(imagen.ruta_imagen)
    ruta_guardar = ruta_tu[0] + str(usuario_m.pk) + str(random()) + \
                   ".PNG"

    imagen_pil.save(ruta_guardar, quality=95)
    enviar_mensaje_imagen(chat_id, ruta_guardar)


def dibujar_texto_sobre_imagen(texto, draw, image, fposiciony, color):
    if texto == "": return

    tam = image.size[1] // 9
    fuente = ImageFont.truetype(FUENTE, tam)

    tam_d = draw.textsize(texto, font=fuente)

    while tam_d[0] + image.size[0] // 2 - tam_d[0] // 2 > image.size[0]:
        del fuente
        tam -= 2
        fuente = ImageFont.truetype(FUENTE, tam)
        tam_d = draw.textsize(texto, font=fuente)

    try:
        draw.text((image.size[0] // 2 - tam_d[0] // 2, fposiciony(tam_d, image.size)), texto, font=fuente, fill=color)
    except ValueError:
        draw.text((image.size[0] // 2 - tam_d[0] // 2, fposiciony(tam_d, image.size)), texto, font=fuente, fill="red")


def guardar_imagen_enviada(message_id, datetime_unix, usuario_m, image):
    # creamos la respuesta
    respuesta = RespuestaServidor(
        id_mensaje=message_id,
        fecha=timezone.make_aware(
            datetime.datetime.utcfromtimestamp(int(datetime_unix)),
            timezone.get_default_timezone()
        ),
        usuario_t=usuario_m,
        imagen_enviada=image
    )

    respuesta.save()  # Guardamos en la BD

    # Actualizamos el usuario
    if usuario_m.ultima_respuesta:
        usuario_m.ultima_respuesta.delete()

    usuario_m.ultima_respuesta = respuesta
    usuario_m.save()

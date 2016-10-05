#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
import requests
import shutil
import json
from HTMLParser import HTMLParser
from os.path import join, exists, basename, splitext

from BotTelegram.update_tg import UpdateTG
from MemesTelegramDjango.settings import BASE_DIR
from models import Usuario, Imagen, RespuestaServidor
from random import random, choice
import django.utils.timezone as timezone
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont
import datetime
from time import sleep

# Codigo del BOT dado por el API de Telegram -- Token
CODE_BOT = "119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg"
# URL para acceder al API de Telegram
URL_TG_API = "https://api.telegram.org/bot" + CODE_BOT + "/"
# URL de la pagina usada para buscar los memes
PAGINA_MEMES = 'http://imgflip.com/memesearch'
# Fuente usada para escribir sobre los memes
FUENTE = "staticfiles/Montserrat-ExtraBold.otf"

root_xml_string = None

class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


import sys

sys.stdout = Unbuffered(sys.stdout)


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


def enviar_mensaje_usuario(chat_id, mensaje):
    requests.get(URL_TG_API + 'sendChatAction', params={'chat_id': chat_id, 'action': 'typing'})
    sleep(2)
    requests.get(URL_TG_API + 'sendMessage', params={'chat_id': chat_id, 'text': mensaje})


def enviar_mensaje_imagen(chat_id, ruta_foto):
    files = {'photo': open(ruta_foto, 'rb')}
    try:
        requests.get(URL_TG_API + 'sendChatAction', params={'chat_id': chat_id, 'action': 'upload_photo'})
        r = requests.post(URL_TG_API + "sendPhoto", data={'chat_id': chat_id}, files=files)
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


# Si no existe la imagen en el servidor
# la guarda en la ruta especificada
def guardar_imagen(imagen):
    if not exists(imagen.ruta_imagen):
        resp = requests.get(imagen.url_imagen, stream=True)

        with open(imagen.ruta_imagen, 'wb') as archivo_img:
            shutil.copyfileobj(resp.raw, archivo_img)


# envia una imagen a un chat
# notar que primero se debe guardar la imagen localmente
def enviar_imagen(imagen, chat_id):
    guardar_imagen(imagen)
    return enviar_mensaje_imagen(chat_id, imagen.ruta_imagen)


class parseadorHTML(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.rutas_imagenes = []

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            self.rutas_imagenes.append(dict(attrs))


# Busca TODAS las imagenes en la pagina web PAGINA_MEMES
# va guardando TODAS las rutas url en una lista y las regresa
def buscar_imagenes(memeConsultado):
    try:
        peticion = requests.get(PAGINA_MEMES, params={'q': memeConsultado})
    except:
        return None

    if peticion.status_code != 200:
        return None
    parser = parseadorHTML()
    parser.feed(peticion.text)
    return parser.rutas_imagenes

#Envia un mensaje a todos los usuarios del bot
def enviar_mensaje_usuarios(mensaje):
    usuarios = Usuario.objects.all()

    for usuario in usuarios:
        if usuario.suscrito_actu:
            enviar_mensaje_usuario(usuario.pk, mensaje)

#De las imagenes referenciadas en la BD obtiene una aleatoria
def obtener_imagen_random():
    return choice(Imagen.objects.all())

# Envia una cadena de texto asociada a un comando
def enviar_mensaje_ayuda_comando(comando,chat_id):
    for help_m in root_xml_string.iter("help"):
        if help_m.attrib.get("comando", "") == comando:
            enviar_mensaje_usuario(chat_id, help_m.text)
            return


# construye todos los objetos Imagen de la BD dada una lista de URL hacia las imagenes
def construir_imagenes(rutas_imagenes, txt_bu):
    for i in range(len(rutas_imagenes) - 1, -1, -1):
        url_ima = "http:" + rutas_imagenes[i]['src']
        path_archivo = join('staticfiles', basename(url_ima))  # Ruta en el servidor

        imagendb = Imagen(id_lista=i,
                          url_imagen=url_ima,
                          ruta_imagen=path_archivo,
                          textobuscado=txt_bu)
        imagendb.save()

    return imagendb


# Obtiene la primera imagen asociada a un texto buscado por el usuario
# si ya alguien lo ha buscado antes se regresa la referencia al primer objeto Imagen de la lista
# sino, se buscan todas-> se construyen en la BD y se regresa el primer objeto Imagen
def buscar_primera_imagen(texto, chat_id, nombre):
    primera_imagen = None
    try:
        primera_imagen = Imagen.objects.get(id_lista=0, textobuscado=texto)
    except ObjectDoesNotExist:

        imagenes = buscar_imagenes(texto)
        if imagenes == []:
            enviar_mensaje_usuario(chat_id, root_xml_string.find("no_recuerda_meme").text)
        elif imagenes == None:
            enviar_mensaje_usuario(chat_id, root_xml_string.find("problema_buscando_meme").text)

        else:
            primera_imagen = construir_imagenes(imagenes, texto)

    return primera_imagen


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

#start help

## Atiende el mensaje del usuario
def atender_consulta_mensaje_tg(dict_update):
    global root_xml_string

    update_tg = UpdateTG(dict_update)  # Convertimos el dict a una manejable Python Class

    tree = ET.parse(join("BotTelegram","languages", "en_US", 'strings.xml'))
    root_xml_string = tree.getroot()

    # Someone was boring and atacked
    if update_tg.message.text == "/This_group_is_hacked_by_FATA_Leave_it_or_you_will_face_the_consequences":
        return

    # Por ahora solo grupos "normales" y chats privados

    if update_tg.message.chat.type not in ("group", "private"): return

    try:
        usuario_m = Usuario.objects.get(id_u=update_tg.message.user_from.id)
    except Usuario.DoesNotExist:
        usuario_m = Usuario.create(
            id_u=update_tg.message.user_from.id,
            nombreusuario=update_tg.message.user_from.username[:200],
            nombre=update_tg.message.user_from.first_name[:200],
            apellido=update_tg.message.user_from.last_name[:200]
        )

    try:
        RespuestaServidor.objects.get(id_mensaje=update_tg.message.message_id)
        return  # Mensaje ya respondido
    except ObjectDoesNotExist:
        pass

    if not update_tg.message.text:
        if update_tg.message.new_chat_member:
            if update_tg.message.new_chat_member.username == 'MemesBot':
                enviar_mensaje_ayuda_comando("help", update_tg.message.chat.id)

    elif update_tg.message.text[0:6] == "/start":
        enviar_mensaje_ayuda_comando("start",update_tg.message.chat.id)

    elif update_tg.message.text[0:5] == "/help":
        if update_tg.message.chat.type == "group":
            comando = update_tg.message.text[14:].strip()
        elif update_tg.message.chat.type == "private":
            comando = update_tg.message.text[5:].strip()

        if not comando:
            comando = "help"
        enviar_mensaje_ayuda_comando(comando, update_tg.message.chat.id)

    elif update_tg.message.text[0:7] == "/random":

        im_ale = obtener_imagen_random() #Se obtiene la imagen aleatoria
        enviar_imagen(im_ale, update_tg.message.chat.id) # Se envia al chat
        respuesta = RespuestaServidor(id_mensaje=dict_update['message']['message_id'],
                                 fecha=timezone.make_aware(
                                     datetime.datetime.utcfromtimestamp(int(update_tg.message.date)),
                                     timezone.get_default_timezone()),
                                 usuario=usuario_m,
                                 imagen_enviada=im_ale)
        respuesta.save()

    elif update_tg.message.text[0:5] == "/stop":

        if usuario_m.suscrito_actu:
            usuario_m.suscrito_actu = False
            usuario_m.save() #Actualizamos el usuario en la BD
            enviar_mensaje_usuario(update_tg.message.chat.id,root_xml_string.find("stop").text)
        else:
            enviar_mensaje_usuario(update_tg.message.chat.id, root_xml_string.find("stop_twice").text)

    elif update_tg.message.text[0:17] == "/wannaknowupdates":
        if not usuario_m.suscrito_actu:
            usuario_m.suscrito_actu = True
            usuario_m.save()
            enviar_mensaje_usuario(update_tg.message.chat.id,root_xml_string.find("wannaknowupdates").text)
        else:
            enviar_mensaje_usuario(update_tg.message.chat.id,root_xml_string.find("wannaknowupdates_twice").text)

    elif update_tg.message.text[0:7] == "/create":

        comandos = ""

        if update_tg.message.chat.type == "private":
            comandos = update_tg.message.text[8:].strip()
        elif update_tg.message.chat.type == "group":
            comandos = update_tg.message.text[17:].strip() #Saltamos @MemesBot

        if not comandos:
            enviar_mensaje_usuario(update_tg.message.chat.id,root_xml_string.find("create_sin_comandos").text)
        else:
            comandos = [i.strip() for i in comandos.split(',') if i]

            ulti_m_con_ima = RespuestaServidor.objects.filter(usuario=usuario_m).last()

            if ulti_m_con_ima:
                try:
                    comandos = ("", comandos[0], comandos[1])
                except IndexError:
                    comandos = ("", comandos[0])
                escribir_enviar_meme(comandos, ulti_m_con_ima.imagen_enviada, update_tg.message.chat.id, usuario_m)
            else:
                enviar_mensaje_usuario(update_tg.message.chat.id,root_xml_string.find("create_sin_imagen_reciente").text)

    elif update_tg.message.text[0:7] == "/sendme":

        comandos = ""

        if update_tg.message.chat.type == "private":
            comandos = update_tg.message.text[8:].strip()
        elif update_tg.message.chat.type == "group":
            comandos = update_tg.message.text[17:].strip()

        if not comandos:
            enviar_mensaje_usuario(update_tg.message.chat.id,root_xml_string.find("sendme_sin_comandos").text)
        else:

            comandos = [i.strip() for i in comandos.split(',') if i]

            imagen = buscar_primera_imagen(comandos[0].strip(), update_tg.message.chat.id,
                                           update_tg.message.user_from.first_name)

            if imagen:  # Si se encontro una imagen con exito
                if len(comandos) > 1:  # si el usuario quiere un texto sobre la imagen
                    escribir_enviar_meme(comandos, imagen, update_tg.message.chat.id, usuario_m)
                else:  # si solo quiere la imagen cruda

                    enviar_imagen(imagen, update_tg.message.chat.id)  # Le enviamos la imagen

                    # Notar que guardamos en el servidor la respuesta, esto es usable por /create y /another
                    respuesta = RespuestaServidor(id_mensaje=dict_update['message']['message_id'],
                                                  fecha=timezone.make_aware(
                                                      datetime.datetime.utcfromtimestamp(int(update_tg.message.date)),
                                                      timezone.get_default_timezone()),
                                                  usuario=usuario_m,
                                                  imagen_enviada=imagen)
                    respuesta.save()

    elif update_tg.message.text[0:8] == "/another":
        ulti_m_con_ima = RespuestaServidor.objects.filter(usuario=usuario_m).order_by('id_mensaje')

        if ulti_m_con_ima:
            ulti_m_con_ima = ulti_m_con_ima[len(ulti_m_con_ima) - 1]

            try:
                imagen_siguiente = Imagen.objects.get(id_lista=ulti_m_con_ima.imagen_enviada.id_lista + 1,
                                                      textobuscado=ulti_m_con_ima.imagen_enviada.textobuscado)

                requests.get(URL_TG_API + 'sendChatAction',
                             params={'chat_id': update_tg.message.chat.id, 'action': 'upload_photo'})
                if enviar_imagen(imagen_siguiente, update_tg.message.chat.id) != 0:
                    enviar_mensaje_usuario(update_tg.message.chat.id, root_xml_string.find("error_1").text)
                else:
                    # Guardamos en el servidor la respuesta, esto es usable por /create y /another
                    respuesta = RespuestaServidor(id_mensaje=dict_update['message']['message_id'],
                                                  fecha=timezone.make_aware(
                                                      datetime.datetime.utcfromtimestamp(int(update_tg.message.date)),
                                                      timezone.get_default_timezone()),
                                                  usuario=usuario_m,
                                                  imagen_enviada=imagen_siguiente)
                    respuesta.save()
            except ObjectDoesNotExist:
                enviar_mensaje_usuario(update_tg.message.chat.id, root_xml_string.find("sin_mas_imagenes_another").text)

        else:
            enviar_mensaje_usuario(update_tg.message.chat.id, root_xml_string.find("another_sin_imagen").text)
    else:
        if update_tg.message.chat.type == "private":
            imagen = buscar_primera_imagen(update_tg.message.text.strip(), update_tg.message.chat.id,
                                           update_tg.message.user_from.username)

            if imagen:
                enviar_imagen(imagen, update_tg.message.chat.id)
                # Guardamos en el servidor la respuesta, esto es usable por /create y /another
                respuesta = RespuestaServidor(id_mensaje=dict_update['message']['message_id'],
                                              fecha=timezone.make_aware(
                                                  datetime.datetime.utcfromtimestamp(int(update_tg.message.date)),
                                                  timezone.get_default_timezone()),
                                              usuario=usuario_m,
                                              imagen_enviada=imagen)
                respuesta.save()

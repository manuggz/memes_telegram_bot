# coding=utf-8
import json

import requests
import sys
from django.core.exceptions import ObjectDoesNotExist
from os.path import exists, basename, join

from BotTelegram.construir_callback_buttons import construir_callback_buttons, construir_callbackbuttons_create
from BotTelegram.enviar_mensajes_usuario import enviar_mensaje_usuario, enviar_imagen, enviar_mensaje_ayuda_comando, \
    URL_TG_API, escribir_enviar_meme, guardar_imagen_respuesta_servidor, parsear_enviar_xml, borrar_cache_espera, \
    obtener_upper_lower_text, guardar_imagen, CODE_BOT
from BotTelegram.models import Imagen, Usuario
from PIL import ImageColor
from django.conf import settings

# Procesa el comando "/start" mandado por el usuario
# Recordar que /start envia un mensaje de inicio al usuario


import logging

logger_xml = logging.getLogger("'BotTelegram.error_xml'")

from BotTelegram.obtener_memes_web import obtener_imagen_random, buscar_imagenes_web, construir_imagenes


def start_tg(chat_id, is_debug, xml_string):
    if is_debug:  # Mensage de DEBUG
        enviar_mensaje_usuario(chat_id, "Respuesta /start")


    enviar_mensaje_ayuda_comando(chat_id, "start", xml_string)


# Procesa el comando help del usuario
# Recordar que /help envia un mensaje de ayuda al usuario
# Ejemplos de uso: /help o /help search
def help_tg(chat_id, tema_ayuda, is_debug, xml_string):

    if not tema_ayuda:
        tema_ayuda = "help"

    if is_debug:  # Mensage de DEBUG
        enviar_mensaje_usuario(chat_id, "Respuesta /help : " + tema_ayuda)

    enviar_mensaje_ayuda_comando(chat_id,tema_ayuda, xml_string)


# Procesa el comando /random del usuario
# Recordar que /random envia una imagen aleatoria al usuario
def random_tg(chat_id, is_debug):
    if is_debug:  # Mensage de DEBUG
        enviar_mensaje_usuario(chat_id, "Respuesta /random")

    imagen_aleatoria = obtener_imagen_random()  # Se obtiene la imagen aleatoria
    if imagen_aleatoria:
        enviar_imagen(
            chat_id, imagen_aleatoria,
            construir_callback_buttons(imagen_aleatoria)
        )
    return imagen_aleatoria


# Procesa el comando /stop del usuario
# Recordar que /stop detiene al bot de enviar mensajes de aviso al usuario
# --- Mensajes que se envian desde la web
def stop_tg(chat_id, usuario, is_debug, xml_string):
    if is_debug:  # Mensage de DEBUG
        enviar_mensaje_usuario(chat_id, "Respuesta /stop")

    if usuario.is_suscrito_actu:
        usuario.is_suscrito_actu = False
        usuario.save()  # Actualizamos el usuario en la BD
        parsear_enviar_xml(chat_id,xml_string.find("stop"))
    else:
        parsear_enviar_xml(chat_id,xml_string.find("stop_twice"))


# Procesa el comando /wannaknowupdates del usuario
# recordar que /wannaknowupdates habilita al usuario para recibir los mensajes del bot de nuevo
def wannaknowupdates_tg(chat_id, usuario, is_debug, xml_string):
    if is_debug:  # Mensage de DEBUG
        enviar_mensaje_usuario(chat_id, "Respuesta /wannaknowupdates")

    if not usuario.is_suscrito_actu:
        usuario.is_suscrito_actu = True
        usuario.save()
        parsear_enviar_xml(chat_id,xml_string.find("wannaknowupdates"))
    else:
        parsear_enviar_xml(chat_id, xml_string.find("wannaknowupdates_twice"))


# Procesa el comando /create del usuario
# Recordar que /create escribe sobre la ultima imagen enviada por el usuario
# resto_mensaje es el texto que le sigue al comando /create , tal como el mensaje y el color
def create_tg(chat_id, usuario, resto_mensaje, is_debug, xml_string):

    #print "c.1"
    if is_debug:  # Mensage de DEBUG
        enviar_mensaje_usuario(chat_id, "Respuesta /create comando " + resto_mensaje)

    #print "c.2"
    if not usuario.imagen_actual:  # Si no se ha enviado una imagen al usuario
        #print "c.3"
        parsear_enviar_xml(chat_id, obtener_xml_objeto("create_sin_imagen_reciente",xml_string))
        return

    #print "c.4"
    #if usuario.datos_imagen_borrador:
        #print "c.5"
        #usuario.datos_imagen_borrador.delete()
        #usuario.datos_imagen_borrador.save()
        #usuario.save()
    #print "c.6"

    #datos_imagen_borrador_nuevo = DatosImagenBorrador()
    #print "c.7"
    #datos_imagen_borrador_nuevo.save()

    #print "c.8"
    #usuario.datos_imagen_borrador = datos_imagen_borrador_nuevo
    #print "c.9"
    usuario.esta_creando_meme = True
    usuario.upper_text = "Upper TEXT"
    usuario.lower_text = "Lower TEXT"
    #usuario.save()

    #print "c.10"
    if not resto_mensaje:  # Si el usuario solo nos envio "/create"
        #print "c.11"
        guardar_imagen(usuario.imagen_actual)

        #print "c.12"
        escribir_enviar_meme(
            chat_id,
            usuario.upper_text,
            usuario.lower_text,
            usuario.color,
            usuario.imagen_actual.ruta_imagen,
            mark_keyboard=construir_callbackbuttons_create(xml_string)
        )
        return


    #print "c.13"
    # Divide resto_mensaje en el TEXTO y el COLOR del mensaje
    # Ejemplo : "TEXTO 1- TEXTO 2, RED" ----------> ["TEXTO 1- TEXTO 2","RED"]
    # Ejemplo : "TEXTO 1" ----------> ["TEXTO 1"]
    mensajes = [mensaje_dibujar.strip() for mensaje_dibujar in resto_mensaje.split(',')]

    try:
        texto,color = mensajes[0], mensajes[1]
    except IndexError:
        texto , color  = mensajes[0],"white"

    try:
        ImageColor.getrgb(color)
    except ValueError:
        parsear_enviar_xml(chat_id, obtener_xml_objeto("error_mal_color",xml_string))
        color = "white"

    upper_text , lower_text = obtener_upper_lower_text(texto)

    usuario.upper_text = upper_text
    usuario.lower_text = lower_text
    usuario.color = color
    usuario.save()

    guardar_imagen(usuario.imagen_actual)

    escribir_enviar_meme(
        chat_id,
        upper_text,
        lower_text,
        color,
        usuario.imagen_actual.ruta_imagen,
        mark_keyboard=construir_callbackbuttons_create(xml_string)
    )


def obtener_xml_objeto(tag,xml_string):
    objeto_xml_texto = xml_string.find(tag)

    if objeto_xml_texto is None:
        logger_xml.error("No se encontró TEXTO para " + tag)

        if settings.DEBUG:
            # Forzamos el error
            raise Exception("Error XML")

    return objeto_xml_texto


# Procesa el comando /search del usuario
# Recordar que /search busca el meme MEME NAME
# El formato es /search MEME NAME
def search_tg(chat_id, usuario, resto_mensaje, is_debug, xml_string):

    if is_debug:  # Mensage de DEBUG
        enviar_mensaje_usuario(chat_id, "Respuesta /search " + resto_mensaje)

    if not resto_mensaje:  # si el usuario envia /search sin el resto del formato
        parsear_enviar_xml(chat_id, obtener_xml_objeto("search_sin_comandos",xml_string))
        return None

    imagen = buscar_primera_imagen(chat_id,resto_mensaje.strip(), xml_string)

    if not imagen: return None  # Si no se encontro una imagen con exito

    enviar_imagen(chat_id, imagen,construir_callback_buttons(imagen))
    return imagen  # regresamos la imagen enviada para que el usuario la pueda usar despues con comandos tales
    # como /create o /next


# Procesa el comando /next del usuario
# recordar que /next envia la siguiente imagen de la anterior enviada
# El usuario puede usar /next despues de los siguientes casos:
# Despues de /random , /search meme name, meme name, anterior /next
def next_image_tg(chat_id, usuario, is_debug, xml_string):

    if is_debug:  # Mensage de DEBUG
        enviar_mensaje_usuario(chat_id, "Respuesta /next")


    if not usuario.imagen_actual:  # En caso de que no exista una imagen anterior
        parsear_enviar_xml(chat_id, xml_string.find("next_sin_imagen"))
        return None

    try:  # Intentamos obtener la siguiente
        imagen_siguiente = Imagen.objects.get(
            id_lista=usuario.imagen_actual.id_lista + 1,
            textobuscado=usuario.imagen_actual.textobuscado
        )

        # Enviamos la imagen
        if enviar_imagen(chat_id, imagen_siguiente,construir_callback_buttons(imagen_siguiente)) != 0:  # si no es exitoso
            parsear_enviar_xml(chat_id, xml_string.find("error_1"))
            return None

        return imagen_siguiente
    except ObjectDoesNotExist:  # No existe una imagen siguiente
        parsear_enviar_xml(chat_id, xml_string.find("sin_mas_imagenes_next"))

    return None


# Procesa cuando el usuario solo envia el nombre del meme
# Ejemplo : Solo envia "yao ming"
def buscar_meme_tg(chat_id, meme_name, tipo_chat, is_debug, xml_strings):
    if is_debug:  # Mensage de DEBUG
        enviar_mensaje_usuario(chat_id, "Respuesta mensage sin comando: " + meme_name)

    if tipo_chat != "private": return None  # Debido a la forma del comando solo funciona "bien" cuando es un chat privado

    imagen = buscar_primera_imagen(chat_id, meme_name.strip(), xml_strings)

    if imagen:
        enviar_imagen(chat_id, imagen,construir_callback_buttons(imagen))

    return imagen


## Atiende el mensaje del usuario
def procesar_mensaje_texto(mensaje, xml_strings, is_debug):

    #Obtenemos la referencia al usuario o lo creamos
    try:
        usuario = Usuario.objects.get(id_u=mensaje.user_from.id)
    except ObjectDoesNotExist:

        usuario = Usuario(
            id_u=mensaje.user_from.id,
            nombreusuario=mensaje.user_from.username[:200],
            nombre=mensaje.user_from.first_name[:200],
            apellido=mensaje.user_from.last_name[:200]
        )
        usuario.save()

    ## Dividimos el mensaje del usuario en: comando | Texto
    comando , resto_mensaje = extraer_comando(mensaje.text)

    # Posible imagen enviada como respuesta al mensaje del usuario
    imagen_enviada = None

    if comando == "/start":
        borrar_cache_espera(usuario)
        start_tg(
            mensaje.user_from.id,
            is_debug,
            xml_strings
        )
    elif comando == "/help":
        help_tg(
            mensaje.user_from.id,
            resto_mensaje,
            is_debug,
            xml_strings
        )
    elif comando == "/random":
        borrar_cache_espera(usuario)

        imagen_enviada = random_tg(
            mensaje.user_from.id,
            is_debug
        )
    elif comando == "/stop":
        stop_tg(
            mensaje.user_from.id,
            usuario,
            is_debug,
            xml_strings
        )
    elif comando == "/wannaknowupdates":
        wannaknowupdates_tg(
            mensaje.user_from.id,
            usuario,
            is_debug,
            xml_strings
        )
    elif comando == "/create":
        create_tg(
            mensaje.user_from.id,
            usuario,
            resto_mensaje,
            is_debug,
            xml_strings
        )
    elif comando == "/search":

        imagen_enviada = search_tg(
            mensaje.user_from.id,
            usuario,
            resto_mensaje,
            is_debug,
            xml_strings
        )

        if imagen_enviada is not None:
            borrar_cache_espera(usuario)

    elif comando == "/next":
        borrar_cache_espera(usuario)
        imagen_enviada = next_image_tg(
            mensaje.user_from.id,
            usuario,
            is_debug,
            xml_strings
        )
    else:
        if usuario.comando_en_espera != "None":
            if usuario.esta_creando_meme:

                cambio_algo = False
                if usuario.comando_en_espera == "SetUpperText":
                    if comando == "/none":
                        usuario.upper_text = ""
                        parsear_enviar_xml(mensaje.user_from.id, xml_strings.find("changed_upper_text_none"))
                    else:
                        usuario.upper_text = comando[:200]
                        parsear_enviar_xml(mensaje.user_from.id, xml_strings.find("changed_upper_text"))
                    cambio_algo = True

                elif usuario.comando_en_espera == "SetLowerText":

                    if comando == "/none":
                        usuario.lower_text = ""
                        parsear_enviar_xml(mensaje.user_from.id, xml_strings.find("changed_lower_text_none"))
                    else:
                        usuario.lower_text = comando[:200]
                        parsear_enviar_xml(mensaje.user_from.id, xml_strings.find("changed_lower_text"))

                    usuario.save()
                    cambio_algo = True

                elif usuario.comando_en_espera == "SetColor":

                    if comando == "/none":
                        nuevo_color = "white"
                        parsear_enviar_xml(mensaje.user_from.id, xml_strings.find("changed_color_text_none"))
                    else:
                        #usuario.datos_imagen_borrador.lower_text = comando[:200]
                        nuevo_color = comando[:200]

                    color_rgb = None

                    try:
                        color_rgb = ImageColor.getrgb(nuevo_color)
                    except ValueError:
                        parsear_enviar_xml(mensaje.user_from.id,xml_strings.find("error_mal_color"))

                    if color_rgb:
                        usuario.color = nuevo_color
                        parsear_enviar_xml(mensaje.user_from.id, xml_strings.find("changed_color_text"))
                        cambio_algo = True

                if cambio_algo:
                    usuario.save()
                    guardar_imagen(usuario.imagen_actual)

                    escribir_enviar_meme(
                        mensaje.user_from.id,
                        usuario.upper_text,
                        usuario.lower_text,
                        usuario.color,
                        usuario.imagen_actual.ruta_imagen,
                        mark_keyboard=construir_callbackbuttons_create(xml_strings)
                    )
                    usuario.comando_en_espera = "None"

            else:
                parsear_enviar_xml(mensaje.user_from.id,xml_strings.find("sin_imagen_borrador"))
        else:
            borrar_cache_espera(usuario)
            imagen_enviada = buscar_meme_tg(
                mensaje.user_from.id,
                comando,
                mensaje.chat.type,
                is_debug,
                xml_strings
            )

    if imagen_enviada:
        guardar_imagen_respuesta_servidor(
            mensaje.datetime,
            usuario,
            imagen_enviada
        )


# Obtiene la primera imagen asociada a un texto buscado por el usuario
# si ya alguien lo ha buscado antes se regresa la referencia al primer objeto Imagen de la lista
# sino, se buscan todas-> se construyen en la BD y se regresa el primer objeto Imagen
def buscar_primera_imagen(chat_id, meme_name, xml_strings):
    primera_imagen = None
    try:
        primera_imagen = Imagen.objects.get(id_lista=0, textobuscado=meme_name)
    except ObjectDoesNotExist:

        imagenes = buscar_imagenes_web(meme_name)

        if imagenes == []:
            parsear_enviar_xml(chat_id, xml_strings.find("no_recuerda_meme"))
        elif imagenes == None:
            parsear_enviar_xml(chat_id, xml_strings.find("problema_buscando_meme"))
        else:
            primera_imagen = construir_imagenes(imagenes, meme_name)

    return primera_imagen

## Se encarga de manejar las fotos que el usuario envia
def procesar_mensaje_foto(mensaje, xml_strings, is_debug):

    try:
        usuario = Usuario.objects.get(id_u=mensaje.user_from.id)
    except ObjectDoesNotExist:

        usuario = Usuario(
            id_u=mensaje.user_from.id,
            nombreusuario=mensaje.user_from.username[:200],
            nombre=mensaje.user_from.first_name[:200],
            apellido=mensaje.user_from.last_name[:200]
        )
        usuario.save()

    photo_size = mensaje.photo.maximo_tam()

    if photo_size:
        r = requests.get(URL_TG_API + 'getFile',
                         params={"file_id": photo_size.file_id})
        respuesta = json.loads(r.text)

        if respuesta["ok"]:

            file_path_tg = respuesta["result"]["file_path"]
            file_path_servidor = join('staticfiles', basename(file_path_tg))
            photo_size.file_id = respuesta["result"]["file_id"]
            photo_size.file_size = respuesta["result"]["file_size"]

            try:  # si ya el usuario subio una imagen anterior la borramos
                imagenes = Imagen.objects.filter(textobuscado=mensaje.user_from.id,
                                            id_lista=-1)
                imagenes.delete()
            except ObjectDoesNotExist:
                pass

            ## Creamos una nueva imagen en la bd
            imagen = Imagen(
                id_lista=-1,  ## dice que es del usuario
                url_imagen="https://api.telegram.org/file/bot" + CODE_BOT + "/" + file_path_tg,
                ruta_imagen=file_path_servidor,
                textobuscado=usuario.pk,
                title=mensaje.caption
            )
            imagen.save()

            guardar_imagen(imagen)

            if exists(file_path_servidor):
                usuario.comando_en_espera = "None"

                print "guardar imagen"
                guardar_imagen_respuesta_servidor(mensaje.datetime, usuario, imagen,guardar_usuario = False)

                print "create"
                create_tg(mensaje.user_from.id,usuario,"",is_debug,xml_strings)

    usuario.save()

# Separa el texto enviado por el usuario en la forma "comando resto"
# Ejemplo:
# "/comando ASDASd"
# regresa ("comando","ASDASd")
#
# "/comando@MemesBot Test - Test , Red"
# regresa ("comando","Test - Test , Red")
#
# "yao ming"
# regresa ("yao ming","")
def extraer_comando(text):
    if not text: return ("","")

    text = text.strip()
    comando = ""

    for i in range(0, len(text)):

        if (text[0] == "/" and text[i] == ' '): return (comando, text[i + 1:])

        if text[i] == '@' and text[i:i + len("MemesBot")]:
            return (comando, text[i + len("MemesBot") + 1:])

        comando += text[i]

    return (comando, "")

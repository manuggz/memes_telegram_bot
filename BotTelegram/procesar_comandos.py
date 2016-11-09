# coding=utf-8

import logging
from django.core.exceptions import ObjectDoesNotExist

from BotTelegram.construir_callback_buttons import construir_callback_buttons, construir_callbackbuttons_create
from BotTelegram.enviar_mensajes_usuario import enviar_mensaje_usuario, enviar_imagen, enviar_mensaje_ayuda_comando, \
    escribir_enviar_meme, parsear_enviar_xml, \
    obtener_upper_lower_text, guardar_imagen, obtener_xml_objeto
from BotTelegram.obtener_memes import obtener_imagen_random, buscar_memes_web, construir_imagenes, \
    buscar_primera_imagen
from BotTelegram.models import Imagen
from PIL import ImageColor


logger_xml = logging.getLogger("'BotTelegram.error_xml'")


# Procesa el comando "/start" mandado por el usuario
# Recordar que /start envia un mensaje de inicio al usuario
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

    if is_debug:  # Mensage de DEBUG
        enviar_mensaje_usuario(chat_id, "Respuesta /create comando " + resto_mensaje)

    if not usuario.imagen_actual:  # Si no se ha enviado una imagen al usuario
        parsear_enviar_xml(chat_id, obtener_xml_objeto("create_sin_imagen_reciente",xml_string))
        return

    usuario.esta_creando_meme = True
    usuario.upper_text = "Upper TEXT"
    usuario.lower_text = "Lower TEXT"

    if not resto_mensaje:  # Si el usuario solo nos envio "/create"
        guardar_imagen(usuario.imagen_actual)

        escribir_enviar_meme(
            chat_id,
            usuario.upper_text,
            usuario.lower_text,
            usuario.color,
            usuario.imagen_actual.ruta_imagen,
            mark_keyboard=construir_callbackbuttons_create(xml_string)
        )
        return


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



# Procesa el comando /search del usuario
# Recordar que /search busca el meme MEME NAME
# El formato es /search MEME NAME
def search_tg(chat_id, usuario, resto_mensaje, is_debug, xml_string):

    if is_debug:  # Mensage de DEBUG
        enviar_mensaje_usuario(chat_id, "Respuesta /search " + resto_mensaje)

    if not resto_mensaje:  # si el usuario envia /search sin el resto del formato
        parsear_enviar_xml(chat_id, obtener_xml_objeto("search_sin_comandos",xml_string))
        usuario.comando_en_espera = "/search"
        usuario.save()
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


    if not usuario.imagen_actual:  # En caso de que el usuario no tenga una imagen actual
        parsear_enviar_xml(chat_id, xml_string.find("next_sin_imagen"))
        return None

    try:  # Intentamos obtener la siguiente
        imagen_siguiente = Imagen.objects.get(
            id_lista=usuario.imagen_actual.id_lista + 1,
            textobuscado=usuario.imagen_actual.textobuscado
        )
    except ObjectDoesNotExist:  # No existe una imagen siguiente
        parsear_enviar_xml(chat_id, xml_string.find("sin_mas_imagenes_next"))
        return None

    # Enviamos la imagen
    if enviar_imagen(chat_id, imagen_siguiente,
                     construir_callback_buttons(imagen_siguiente)) != 0:  # si no es exitoso
        parsear_enviar_xml(chat_id, xml_string.find("error_1"))
        return None

    return imagen_siguiente


# Procesa cuando el usuario solo envia el nombre del meme
# Ejemplo : Solo envia "yao ming"
def buscar_meme_tg(chat_id, meme_name, is_debug, xml_strings):
    if is_debug:  # Mensage de DEBUG
        enviar_mensaje_usuario(chat_id, "Respuesta mensage sin comando: " + meme_name)

    imagen = buscar_primera_imagen(chat_id, meme_name.strip(), xml_strings)

    if imagen:
        enviar_imagen(chat_id, imagen,construir_callback_buttons(imagen))

    return imagen



# coding=utf-8

import requests
import sys
from django.core.exceptions import ObjectDoesNotExist

from BotTelegram.enviar_mensajes_usuario import enviar_mensaje_usuario, enviar_imagen, enviar_mensaje_ayuda_comando, \
    URL_TG_API, escribir_enviar_meme, guardar_imagen_enviada, parsear_enviar_xml
from BotTelegram.models import Imagen

# Procesa el comando "/start" mandado por el usuario
# Recordar que /start envia un mensaje de inicio al usuario
from BotTelegram.obtener_memes_web import obtener_imagen_random, buscar_imagenes, construir_imagenes


def start_tg(chat_id, is_debug, xml_string):
    if is_debug:  # Mensage de DEBUG
        enviar_mensaje_usuario(chat_id, "Respuesta /start")


    enviar_mensaje_ayuda_comando(chat_id, "start", xml_string)


# Procesa el comando help del usuario
# Recordar que /help envia un mensaje de ayuda al usuario
# Ejemplos de uso: /help o /help sendme
def help_tg(chat_id, tema_ayuda, is_debug, xml_string):
    if not tema_ayuda:
        tema_ayuda = "help"

    if is_debug:  # Mensage de DEBUG
        enviar_mensaje_usuario(chat_id, "Respuesta /help : " + tema_ayuda)

    enviar_mensaje_ayuda_comando(chat_id,tema_ayuda, xml_string)


# Construye los botones que se muestran debajo de una imagen aleatoria
def construir_callback_buttons(imagen):
    data_another = imagen.textobuscado + "," + str(imagen.id_lista)

    if sys.getsizeof(data_another) > 64:
        data_another = imagen.textobuscado
        if sys.getsizeof(data_another) > 64:
            data_another = data_another[:63]

    mark_keyboard = {
        "inline_keyboard":
            [
                [
                    {"text": "Random", "callback_data": "random"}
                ]#,
                #[
                #    {
                #        "text": "Another",
                #        "callback_data": data_another
                #    }
                #]
            ]
    }

    return mark_keyboard


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
        enviar_mensaje_usuario(chat_id, "Respuesta /create")

    if not resto_mensaje:  # Si el usuario solo nos envio "/create"
        parsear_enviar_xml(chat_id, xml_string.find("create_sin_comandos"))
        return

    if not usuario.ultima_respuesta:  # Si no se ha enviado una imagen al usuario
        parsear_enviar_xml(chat_id, xml_string.find("create_sin_imagen_reciente"))
        return

    # Divide resto_mensaje en el TEXTO y el COLOR del mensaje
    # Ejemplo : "TEXTO 1- TEXTO 2, RED" ----------> ["TEXTO 1- TEXTO 2","RED"]
    # Ejemplo : "TEXTO 1" ----------> ["TEXTO 1"]
    mensajes = [mensaje_dibujar.strip() for mensaje_dibujar in resto_mensaje.split(',')]

    if usuario.ultima_respuesta:
        try:
            mensajes = ("", mensajes[0], mensajes[1])
        except IndexError:
            mensajes = ("", mensajes[0])
        escribir_enviar_meme(mensajes, usuario.ultima_respuesta.imagen_enviada, chat_id, usuario)


# Procesa el comando /sendme del usuario
# Recordar que /sendme busca el meme MEME NAME y escribe sobre él
# El formato es /sendme MEME NAME , UPPER TEXT - LOWER TEXT , Color
def sendme_tg(chat_id, usuario, resto_mensaje, is_debug, xml_string):
    if is_debug:  # Mensage de DEBUG
        enviar_mensaje_usuario(chat_id, "Respuesta /sendme")

    if not resto_mensaje:  # si el usuario envia /sendme sin el resto del formato
        parsear_enviar_xml(chat_id, xml_string.find("sendme_sin_comandos"))
        return None

    # Divide resto_mensaje en el MEME NAME , TEXTO y COLOR del mensaje
    # Ejemplo : "MEME NAME , TEXTO 1- TEXTO 2, RED" ----------> ["MEME NAME","TEXTO 1- TEXTO 2","RED"]
    # Ejemplo : "MEME NAME" ----------> ["MEME NAME"]
    formato = [mensaje_dibujar.strip() for mensaje_dibujar in resto_mensaje.split(',')]

    imagen = buscar_primera_imagen(formato[0].strip(), chat_id, xml_string)

    if not imagen: return None  # Si no se encontro una imagen con exito

    if len(formato) == 1:  # si solo quiere la imagen "cruda" ejemplo: solo envia /sendme yao ming
        enviar_imagen(chat_id, imagen)  # Le enviamos la imagen de yao ming
        return imagen  # regresamos la imagen enviada para que el usuario la pueda usar despues con comandos tales
        # como /create o /another

    # si el usuario quiere un texto sobre la imagen
    escribir_enviar_meme(formato, imagen, chat_id, usuario)
    return None


# Procesa el comando /another del usuario
# recordar que /another envia la siguiente imagen de la anterior enviada
# El usuario puede usar /another despues de los siguientes casos:
# Despues de /random , /sendme meme name, meme name, anterior /another
def another_tg(chat_id, usuario, is_debug, xml_string):
    if is_debug:  # Mensage de DEBUG
        enviar_mensaje_usuario(chat_id, "Respuesta /another")

    if not usuario.ultima_respuesta:  # En caso de que no exista una imagen anterior
        parsear_enviar_xml(chat_id, xml_string.find("another_sin_imagen"))
        return None

    try:  # Intentamos obtener la siguiente
        imagen_siguiente = Imagen.objects.get(
            id_lista=usuario.ultima_respuesta.imagen_enviada.id_lista + 1,
            textobuscado=usuario.ultima_respuesta.imagen_enviada.textobuscado
        )

        # Colocamos el estado en el bot "subiendo foto"
        requests.get(URL_TG_API + 'sendChatAction', params={'chat_id': chat_id, 'action': 'upload_photo'})

        # Enviamos la imagen
        if enviar_imagen(chat_id, imagen_siguiente) != 0:  # si no es exitoso
            parsear_enviar_xml(chat_id, xml_string.find("error_1"))
            return None

        return imagen_siguiente
    except ObjectDoesNotExist:  # No existe una imagen siguiente
        parsear_enviar_xml(chat_id, xml_string.find("sin_mas_imagenes_another"))

    return None


# Procesa cuando el usuario solo envia el nombre del meme
# Ejemplo : Solo envia "yao ming"
def buscar_meme_tg(chat_id, meme_name, tipo_chat, is_debug, xml_strings):
    if is_debug:  # Mensage de DEBUG
        enviar_mensaje_usuario(chat_id, "Respuesta mensage sin comando")

    if tipo_chat != "private": return None  # Debido a la forma del comando solo funciona "bien" cuando es un chat privado

    imagen = buscar_primera_imagen(chat_id, meme_name.strip(), xml_strings)

    if imagen:
        enviar_imagen(chat_id, imagen)

    return imagen


## Atiende el mensaje del usuario
def procesar_comando(chat_id, is_debug, tipo_chat, fecha_hora, usuario, xml_strings, message_id,comando, resto_mensaje):
    imagen_enviada = None

    if comando == "/start":
        start_tg(
            chat_id,
            is_debug,
            xml_strings
        )
    elif comando == "/help":
        help_tg(
            chat_id,
            resto_mensaje,
            is_debug,
            xml_strings
        )
    elif comando == "/random":
        imagen_enviada = random_tg(
            chat_id,
            is_debug
        )
    elif comando == "/stop":
        stop_tg(
            chat_id,
            usuario,
            is_debug,
            xml_strings
        )
    elif comando == "/wannaknowupdates":
        wannaknowupdates_tg(
            chat_id,
            usuario,
            is_debug,
            xml_strings
        )
    elif comando == "/create":
        create_tg(
            chat_id,
            usuario,
            resto_mensaje,
            is_debug,
            xml_strings
        )
    elif comando == "/sendme":
        imagen_enviada = sendme_tg(
            chat_id,
            usuario,
            resto_mensaje,
            is_debug,
            xml_strings
        )
    elif comando == "/another":
        imagen_enviada = another_tg(
            chat_id,
            usuario,
            is_debug,
            xml_strings
        )
    else:
        imagen_enviada = buscar_meme_tg(
            chat_id,
            comando,
            tipo_chat,
            is_debug,
            xml_strings
        )

    if imagen_enviada:
        guardar_imagen_enviada(
            message_id,
            fecha_hora,
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

        imagenes = buscar_imagenes(meme_name)
        if imagenes == []:
            parsear_enviar_xml(chat_id, xml_strings.find("no_recuerda_meme"))
        elif imagenes == None:
            parsear_enviar_xml(chat_id, xml_strings.find("problema_buscando_meme"))

        else:
            primera_imagen = construir_imagenes(imagenes, meme_name)

    return primera_imagen


# Separa el texto del usuario en las partes importantes
# Ejemplo:
# "/comando ASDASd"
# regresa ("comando","ASDASd",False)
#
# "/comando@MemesBot Test - Test , Red"
# regresa ("comando","Test - Test , Red",True)
#
# "yao ming"
# regresa ("yao ming","",False)
def extraer_comando(text):
    if not text: return ""

    comando = ""

    for i in range(0, len(text)):

        if (text[0] == "/" and text[i] == ' '): return (comando, text[i + 1:])

        if text[i] == '@' and text[i:i + len("MemesBot")]:
            return (comando, text[i + len("MemesBot") + 1:])

        comando += text[i]

    return (comando, "")

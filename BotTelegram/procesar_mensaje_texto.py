# coding=utf-8
## Atiende el mensaje del usuario
from PIL import ImageColor

from BotTelegram.construir_callback_buttons import construir_callbackbuttons_create, SET_UPPER_TEXT, SET_LOWER_TEXT, \
    SET_COLOR_TEXT
from BotTelegram.enviar_mensajes_usuario import borrar_cache_espera, parsear_enviar_xml, guardar_imagen, \
    guardar_imagen_respuesta_servidor, escribir_enviar_meme
from BotTelegram.models import Usuario
from BotTelegram.procesar_comandos import help_tg, random_tg, stop_tg, wannaknowupdates_tg, create_tg, search_tg, \
    next_image_tg, buscar_meme_tg
from BotTelegram.procesar_comandos import start_tg
from BotTelegram.util import extraer_comando


def procesar_mensaje_texto(mensaje, lenguaje_xml, is_debug):
    # Obtenemos la referencia al usuario o lo creamos
    usuario = Usuario.objects.create(
        id_u=mensaje.user_from.id,
        nombreusuario=mensaje.user_from.username[:200],
        nombre=mensaje.user_from.first_name[:200],
        apellido=mensaje.user_from.last_name[:200]
    )

    ## Dividimos el mensaje del usuario en: comando | Texto
    comando, resto_mensaje = extraer_comando(mensaje.text)

    # Posible imagen enviada como respuesta al mensaje del usuario
    img_enviada = None

    if comando == "/start":
        start_tg(mensaje.user_from.id, is_debug, lenguaje_xml)
    elif comando == "/help":
        help_tg(mensaje.user_from.id, resto_mensaje, is_debug, lenguaje_xml)
    elif comando == "/random":
        img_enviada = random_tg(mensaje.user_from.id, is_debug)
    elif comando == "/stop":
        stop_tg(mensaje.user_from.id, usuario, is_debug, lenguaje_xml)
    elif comando == "/wannaknowupdates":
        wannaknowupdates_tg(mensaje.user_from.id, usuario, is_debug, lenguaje_xml)
    elif comando == "/create":
        create_tg(mensaje.user_from.id, usuario, resto_mensaje, is_debug, lenguaje_xml)
    elif comando == "/search":
        img_enviada = search_tg(mensaje.user_from.id, usuario, resto_mensaje, is_debug, lenguaje_xml)
    elif comando == "/next":
        img_enviada = next_image_tg(mensaje.user_from.id, usuario, is_debug, lenguaje_xml)
    else:
        if usuario.comando_en_espera != "None":  # Si se espera la respuesta a algun comando
            img_enviada = atender_comando_en_espera(usuario, mensaje.user_from.id, comando, is_debug,lenguaje_xml)
        else:  # Sino, entonces es una solicitud de busqueda de un meme
            img_enviada = buscar_meme_tg(mensaje.user_from.id, comando, is_debug, lenguaje_xml)

    if img_enviada is not None:
        borrar_cache_espera(usuario)
        guardar_imagen_respuesta_servidor(mensaje.datetime, usuario, img_enviada)


# Atiende la respuesta enviada al usuario a un comando que espera
# Ejemplo: Cuando el usuario presiona el boton [SetColorText] el bot espera
# que el usuario envie el nuevo color. El cual se envia como "red" por ejemplo.
# Dado que "red" no posee comando se establece comando_en_espera a "SetColorText" y cuando el usuario
# introduce un nuevo texto éste nuevo texto debe estar enlazado al comando_en_espera y realizar
# la accion adecuada.
def atender_comando_en_espera(usuario, chat_id, comando, is_debug, lenguaje_xml):

    if usuario.esta_creando_meme:
        cambio_algo = False
        if usuario.comando_en_espera == SET_UPPER_TEXT:
            if comando == "/none":
                usuario.upper_text = ""
                parsear_enviar_xml(chat_id, lenguaje_xml.find("changed_upper_text_none"))
            else:
                usuario.upper_text = comando[:200]
                parsear_enviar_xml(chat_id, lenguaje_xml.find("changed_upper_text"))
            cambio_algo = True

        elif usuario.comando_en_espera == SET_LOWER_TEXT:

            if comando == "/none":
                usuario.lower_text = ""
                parsear_enviar_xml(chat_id, lenguaje_xml.find("changed_lower_text_none"))
            else:
                usuario.lower_text = comando[:200]
                parsear_enviar_xml(chat_id, lenguaje_xml.find("changed_lower_text"))

            cambio_algo = True

        elif usuario.comando_en_espera == SET_COLOR_TEXT:

            if comando == "/none":
                nuevo_color = "white"
                parsear_enviar_xml(chat_id, lenguaje_xml.find("changed_color_text_none"))
            else:
                # usuario.datos_imagen_borrador.lower_text = comando[:200]
                nuevo_color = comando[:200]

            color_rgb = None

            try:
                color_rgb = ImageColor.getrgb(nuevo_color)
            except ValueError:
                parsear_enviar_xml(chat_id, lenguaje_xml.find("error_mal_color"))

            if color_rgb:
                usuario.color = nuevo_color
                parsear_enviar_xml(chat_id, lenguaje_xml.find("changed_color_text"))
                cambio_algo = True

        if cambio_algo:
            guardar_imagen(usuario.imagen_actual)

            escribir_enviar_meme(
                chat_id,
                usuario.upper_text,
                usuario.lower_text,
                usuario.color,
                usuario.imagen_actual.ruta_imagen,
                mark_keyboard=construir_callbackbuttons_create(lenguaje_xml)
            )
            usuario.comando_en_espera = "None"
            usuario.save()

    else:
        if usuario.comando_en_espera == "/search":
            usuario.comando_en_espera = "None"
            usuario.save()
            return buscar_meme_tg(chat_id, comando, is_debug, lenguaje_xml)
    return None

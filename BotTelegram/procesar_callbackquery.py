# coding=utf-8
# Procesa el callback generado por los botones en el bot
import sys
from django.core.exceptions import ObjectDoesNotExist

from BotTelegram.construir_callback_buttons import construir_callbackbuttons_create
from BotTelegram.enviar_mensajes_usuario import responder_callback_query, enviar_mensaje_usuario, \
    guardar_imagen_respuesta_servidor, parsear_enviar_xml, escribir_enviar_meme, parsear_xml_object, \
    enviar_imagen, borrar_cache_espera, guardar_imagen
from BotTelegram.models import Usuario, Imagen
from BotTelegram.procesar_comandos import procesar_mensaje_texto, construir_callback_buttons, random_tg


def procesar_callback_query(update_tg, xml_strings):

    try:
        usuario_m = Usuario.objects.get(id_u=update_tg.callback_query.user_from.id)
    except ObjectDoesNotExist:

        usuario_m = Usuario.objects.create(
            id_u=update_tg.callback_query.user_from.id,
            nombreusuario=update_tg.callback_query.user_from.username[:200],
            nombre=update_tg.callback_query.user_from.first_name[:200],
            apellido=update_tg.callback_query.user_from.last_name[:200]
        )

    #Avisa al chat de tg que se esta respondiendo la peticion
    # Visualmente, quita el simbolo de <cargando> en el boton que el usuario presionó
    responder_callback_query(update_tg.callback_query.id)

    formato = update_tg.callback_query.data.split(",")

    imagen_enviada = None

    if formato[0] == "Random":
        # Notar que no se esta usando chat_instance arreglar

        borrar_cache_espera(usuario_m)
        imagen_enviada = random_tg(
            update_tg.callback_query.user_from.id,
            update_tg.is_message_debug
        )

    elif formato[0] == "Next":

        borrar_cache_espera(usuario_m)

        imagen_enviada = next_image_tg_callback(
            update_tg.callback_query.user_from.id,
            formato,
            update_tg.is_message_debug,
            xml_strings
        )
    elif formato[0] == "Create":

        imagen_enviada = create_tg_callback(
            update_tg.callback_query.user_from.id,
            usuario_m,
            formato,
            update_tg.is_message_debug,
            xml_strings
        )

    elif formato[0] == "SetUpperText":

        if usuario_m.esta_creando_meme:
            parsear_enviar_xml(update_tg.callback_query.user_from.id, xml_strings.find("dame_upper_text"))
            usuario_m.comando_en_espera = formato[0]
            usuario_m.save()
        else:
            parsear_enviar_xml(update_tg.callback_query.user_from.id, xml_strings.find("sin_imagen_borrador"))

    elif formato[0] == "SetLowerText":
        if usuario_m.esta_creando_meme:
            parsear_enviar_xml(update_tg.callback_query.user_from.id, xml_strings.find("dame_lower_text"))
            usuario_m.comando_en_espera = formato[0]
            usuario_m.save()
        else:
            parsear_enviar_xml(update_tg.callback_query.user_from.id, xml_strings.find("sin_imagen_borrador"))

    elif formato[0] == "SetColor":
        if usuario_m.esta_creando_meme:
            parsear_enviar_xml(update_tg.callback_query.user_from.id, xml_strings.find("dame_color_text"))
            usuario_m.comando_en_espera = formato[0]
            usuario_m.save()
        else:
            parsear_enviar_xml(update_tg.callback_query.user_from.id, xml_strings.find("sin_imagen_borrador"))


    if imagen_enviada:
        guardar_imagen_respuesta_servidor(
            None,
            usuario_m,
            imagen_enviada
        )


def create_tg_callback(chat_id, usuario_m, formato, is_debug, xml_string):
    if is_debug:  # Mensage de DEBUG
        enviar_mensaje_usuario(chat_id, "Respuesta /create callback")

    try:  # Intentamos obtener la imagen
        imagen_seleccionada = Imagen.objects.get(pk=formato[1])
    except ObjectDoesNotExist:  # No existe una imagen siguiente
        parsear_enviar_xml(chat_id, xml_string.find("imagen_muy_vieja_borrada"))
        return None

    borrar_cache_espera(usuario_m)

    # guardar_imagen_enviada(None,usuario_m,imagen_seleccionada)

    usuario_m.esta_creando_meme = True
    usuario_m.upper_text = "Upper TEXT"
    usuario_m.lower_text = "Lower TEXT"
    usuario_m.save()

    guardar_imagen(imagen_seleccionada)

    escribir_enviar_meme(
        chat_id,
        usuario_m.upper_text,
        usuario_m.lower_text,
        usuario_m.color,
        imagen_seleccionada.ruta_imagen,
        mark_keyboard=construir_callbackbuttons_create(xml_string)
    )

    return imagen_seleccionada


def next_image_tg_callback(chat_id, formato, is_debug, xml_string):
    if is_debug:  # Mensage de DEBUG
        enviar_mensaje_usuario(chat_id, "Respuesta /next callback")

    try:  # Intentamos obtener la siguiente
        imagen_seleccionada = Imagen.objects.get(pk=formato[1])
    except ObjectDoesNotExist:  # No existe una imagen siguiente
        parsear_enviar_xml(chat_id, xml_string.find("imagen_muy_vieja_borrada"))
        return None

    try:  # Intentamos obtener la siguiente
        imagen_siguiente = Imagen.objects.get(
            id_lista=imagen_seleccionada.id_lista + 1,
            textobuscado=imagen_seleccionada.textobuscado
        )

        # Enviamos la imagen
        if enviar_imagen(chat_id, imagen_siguiente,
                         construir_callback_buttons(imagen_siguiente)) != 0:  # si no es exitoso
            parsear_enviar_xml(chat_id, xml_string.find("error_1"))
            return None

        return imagen_siguiente
    except ObjectDoesNotExist:  # No existe una imagen siguiente
        parsear_enviar_xml(chat_id, xml_string.find("sin_mas_imagenes_next"))

    return None

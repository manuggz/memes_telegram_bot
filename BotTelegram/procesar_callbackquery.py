# Procesa el callback generado por los botones en el bot
import sys
from django.core.exceptions import ObjectDoesNotExist

from BotTelegram.construir_callback_buttons import construir_callbackbuttons_create
from BotTelegram.enviar_mensajes_usuario import responder_callback_query, enviar_mensaje_usuario, \
    guardar_imagen_enviada, parsear_enviar_xml, escribir_enviar_meme, parsear_xml_object, \
    enviar_imagen, borrar_cache_espera
from BotTelegram.models import Usuario, Imagen, DatosImagenBorrador
from BotTelegram.procesar_comandos import procesar_comando, construir_callback_buttons


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

    responder_callback_query(update_tg.callback_query.id)

    formato = update_tg.callback_query.data.split(",")

    imagen_enviada = None

    if formato[0] == "Random":
        # Notar que no se esta usando chat_instance arreglar

        procesar_comando(
            update_tg.callback_query.user_from.id,
            update_tg.is_message_debug,
            "private",
            update_tg.message.datetime if update_tg.message else None,
            usuario_m,
            xml_strings,
            "/random",
            ""
        )
        return

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

        if usuario_m.datos_imagen_borrador:
            parsear_enviar_xml(update_tg.callback_query.user_from.id, xml_strings.find("dame_upper_text"))
            usuario_m.comando_en_espera = formato[0]
            usuario_m.save()
        else:
            parsear_enviar_xml(update_tg.callback_query.user_from.id, xml_strings.find("sin_imagen_borrador"))
        return
    elif formato[0] == "SetLowerText":
        if usuario_m.datos_imagen_borrador:
            parsear_enviar_xml(update_tg.callback_query.user_from.id, xml_strings.find("dame_lower_text"))
            usuario_m.comando_en_espera = formato[0]
            usuario_m.save()
        else:
            parsear_enviar_xml(update_tg.callback_query.user_from.id, xml_strings.find("sin_imagen_borrador"))
        return
    elif formato[0] == "SetColor":
        if usuario_m.datos_imagen_borrador:
            parsear_enviar_xml(update_tg.callback_query.user_from.id, xml_strings.find("dame_color_text"))
            usuario_m.comando_en_espera = formato[0]
            usuario_m.save()
        else:
            parsear_enviar_xml(update_tg.callback_query.user_from.id, xml_strings.find("sin_imagen_borrador"))
        return

    if imagen_enviada:
        guardar_imagen_enviada(
            None,
            usuario_m,
            imagen_enviada
        )


def create_tg_callback(chat_id, usuario_m, formato, is_debug, xml_string):
    if is_debug:  # Mensage de DEBUG
        enviar_mensaje_usuario(chat_id, "Respuesta /create callback")

    try:  # Intentamos obtener la siguiente
        imagen_seleccionada = Imagen.objects.get(pk=formato[1])
    except ObjectDoesNotExist:  # No existe una imagen siguiente
        parsear_enviar_xml(chat_id, xml_string.find("imagen_muy_vieja_borrada"))
        return None

    borrar_cache_espera(usuario_m)

    # guardar_imagen_enviada(None,usuario_m,imagen_seleccionada)

    datos_imagen_borrador_nuevo = DatosImagenBorrador()
    datos_imagen_borrador_nuevo.save()

    usuario_m.datos_imagen_borrador = datos_imagen_borrador_nuevo
    usuario_m.save()

    escribir_enviar_meme(
        chat_id,
        datos_imagen_borrador_nuevo.upper_text + "-" + datos_imagen_borrador_nuevo.lower_text,
        datos_imagen_borrador_nuevo.color,
        imagen_seleccionada.ruta_imagen,
        mark_keyboard=construir_callbackbuttons_create(datos_imagen_borrador_nuevo, xml_string)
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

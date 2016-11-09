# coding=utf-8
from django.core.exceptions import ObjectDoesNotExist

from BotTelegram.construir_callback_buttons import construir_callbackbuttons_create
from BotTelegram.enviar_mensajes_usuario import responder_callback_query, enviar_mensaje_usuario, \
    guardar_imagen_respuesta_servidor, parsear_enviar_xml, escribir_enviar_meme, \
    enviar_imagen, borrar_cache_espera, guardar_imagen
from BotTelegram.models import Usuario, Imagen
from BotTelegram.procesar_comandos import construir_callback_buttons, random_tg


# Procesa el callback generado por los botones en el bot
def procesar_callback_query(callback_query, lenguaje_xml, es_debug):
    usuario = Usuario.objects.create(
        id_u=callback_query.user_from.id,
        nombreusuario=callback_query.user_from.username[:200],
        nombre=callback_query.user_from.first_name[:200],
        apellido=callback_query.user_from.last_name[:200]
    )

    # Avisa al chat de tg que se esta respondiendo la peticion
    # Visualmente, quita el simbolo de <cargando> en el boton que el usuario presionó
    responder_callback_query(callback_query.id)

    formato = callback_query.data.split(",")

    imagen_enviada = None

    if formato[0] == "Random":  # Boton <Random>
        # Notar que no se esta usando chat_instance arreglar

        borrar_cache_espera(usuario)
        imagen_enviada = random_tg(
            callback_query.user_from.id,
            es_debug
        )

    elif formato[0] == "Next":  # Boton <Next>

        borrar_cache_espera(usuario)
        imagen_enviada = next_image_tg_callback(
            callback_query.user_from.id,
            formato,
            es_debug,
            lenguaje_xml
        )
    elif formato[0] == "Create":  # Boton <Create>

        borrar_cache_espera(usuario)
        imagen_enviada = create_tg_callback(
            callback_query.user_from.id,
            usuario,
            formato,
            es_debug,
            lenguaje_xml
        )

    elif formato[0][:3] == "Set":  # Boton [SetUpperText] , [SetLowerText] , [SetColorText]

        if usuario.esta_creando_meme:
            parsear_enviar_xml(callback_query.user_from.id, lenguaje_xml.find("dame_" + formato[0]))
            usuario.comando_en_espera = formato[0]
            usuario.save()
        else:
            parsear_enviar_xml(callback_query.user_from.id, lenguaje_xml.find("sin_imagen_borrador"))

    if imagen_enviada:
        guardar_imagen_respuesta_servidor(
            None,
            usuario,
            imagen_enviada
        )


## Responde al usuario cuando él presiona el boton <Create>
# Recordar que el boton <Create> asociado a una imagen,
# envia la misma imagen al usuario junto a controles de edicion del meme
# Regresa la imagen enviada al usuario
# notar que regresar la imagen enviada al usuario es importante, porque el usuario pudiera
# tener otra imagen seleccionada(reciente) y presionar el boton [Create] lo que produciria
# errores cuando el usuario envie /create ya que /create tomaria la imagen seleccionada no a la que
# el usuario
# le presiono [Create]. Cuando se regresa en esta funcion se espera que se guarde como imagen
# seleccionada
def create_tg_callback(chat_id, usuario_m, formato, is_debug, xml_string):
    if is_debug:  # Mensage de DEBUG
        enviar_mensaje_usuario(chat_id, "Respuesta /create callback")

    try:  # Intentamos obtener la imagen
        imagen_seleccionada = Imagen.objects.get(pk=formato[1])
    except ObjectDoesNotExist:  # No existe una imagen siguiente
        parsear_enviar_xml(chat_id, xml_string.find("imagen_muy_vieja_borrada"))
        return None

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


## Responde al usuario cuando él presiona el boton <Next>
# Recordar que el boton <Next> asociado a una imagen, envia la siguiente en la lista
# Regresa la imagen enviada al usuario
def next_image_tg_callback(chat_id, formato, is_debug, lenguaje_xml):
    if is_debug:  # Mensage de DEBUG
        enviar_mensaje_usuario(chat_id, "Respuesta /next:callback")

    try:  # Intentamos obtener la imagen de la cual se va a consultar la siguiente
        imagen_seleccionada = Imagen.objects.get(pk=formato[1])
    except ObjectDoesNotExist:  # No existe una imagen siguiente
        parsear_enviar_xml(chat_id, lenguaje_xml.find("imagen_muy_vieja_borrada"))
        return None

    try:  # Intentamos obtener la siguiente
        imagen_siguiente = Imagen.objects.get(
            id_lista=imagen_seleccionada.id_lista + 1,
            textobuscado=imagen_seleccionada.textobuscado
        )
    except ObjectDoesNotExist:  # No existe una imagen siguiente
        parsear_enviar_xml(chat_id, lenguaje_xml.find("sin_mas_imagenes_next"))
        return None

    # Enviamos la imagen
    if enviar_imagen(chat_id, imagen_siguiente,
                     construir_callback_buttons(imagen_siguiente)) != 0:  # si no es exitoso
        parsear_enviar_xml(chat_id, lenguaje_xml.find("error_1"))
        return None

    return imagen_siguiente

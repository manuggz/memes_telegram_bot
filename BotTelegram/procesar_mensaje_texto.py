
## Atiende el mensaje del usuario
from PIL import ImageColor

from BotTelegram.construir_callback_buttons import construir_callbackbuttons_create
from BotTelegram.enviar_mensajes_usuario import borrar_cache_espera, parsear_enviar_xml, guardar_imagen, \
    guardar_imagen_respuesta_servidor, escribir_enviar_meme
from BotTelegram.models import Usuario
from BotTelegram.procesar_comandos import help_tg, random_tg, stop_tg, wannaknowupdates_tg, create_tg, search_tg, \
    next_image_tg, buscar_meme_tg
from BotTelegram.procesar_comandos import start_tg
from BotTelegram.util import extraer_comando


def procesar_mensaje_texto(mensaje, xml_strings, is_debug):

    #Obtenemos la referencia al usuario o lo creamos
    try:
        usuario = Usuario.objects.get(id_u=mensaje.user_from.id)
    except Usuario.ObjectDoesNotExist:

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

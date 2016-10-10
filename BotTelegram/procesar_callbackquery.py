
# Procesa el callback generado por los botones en el bot
from django.core.exceptions import ObjectDoesNotExist

from BotTelegram.enviar_mensajes_usuario import responder_callback_query
from BotTelegram.models import Usuario
from BotTelegram.procesar_comandos import procesar_comando


def procesar_callback_query(update_tg,xml_strings):

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

    if  formato[0]== "Random":
        #Notar que no se esta usando chat_instance arreglar

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

    elif formato[0] == "Another":
        print formato
        return
    elif formato[0] == "Create":
        procesar_comando(
            update_tg.callback_query.user_from.id,
            update_tg.is_message_debug,
            "private",
            update_tg.message.datetime if update_tg.message else None,
            usuario_m,
            xml_strings,
            "/create",
            ""
        )
        return




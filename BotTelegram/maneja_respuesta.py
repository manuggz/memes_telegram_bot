#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import xml.etree.ElementTree as ElementTree
from os.path import join

from BotTelegram.ClasesTG.update_tg import UpdateTG
from BotTelegram.procesar_callbackquery import procesar_callback_query
from BotTelegram.procesar_mensaje_foto import procesar_mensaje_foto
from BotTelegram.procesar_mensaje_texto import procesar_mensaje_texto

## Atiende las peticiones del usuario
def atender_consulta_mensaje_tg(dict_update):

    update_tg = UpdateTG(dict_update)  # Convertimos el dict a una manejable Python Class

    # Cargamos los textos a usar
    lenguaje_xml = ElementTree.parse(
        join(
            os.path.dirname(os.path.abspath(__file__)),
            "languages",
            "en_US",
            'strings.xml'
        )
    )

    # Por ahora solo atiende dos tipos de mensajes "mensaje" y "callback_query"
    if update_tg.message:

        # Por ahora solo chats privados
        if update_tg.message.chat.type not in ("private"): return

        if update_tg.message.text:
            procesar_mensaje_texto(update_tg.message, lenguaje_xml, update_tg.is_message_debug)
        elif update_tg.message.photo:
            procesar_mensaje_foto(update_tg.message, lenguaje_xml, update_tg.is_message_debug)

    elif update_tg.callback_query:
        procesar_callback_query(update_tg.callback_query,lenguaje_xml,update_tg.is_message_debug)


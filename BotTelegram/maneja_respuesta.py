#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import shutil
import xml.etree.ElementTree as ET
from os.path import join, exists, basename

#from BotTelegram.ClasesTG import UpdateTG
from BotTelegram.ClasesTG.update_tg import UpdateTG
from BotTelegram.enviar_mensajes_usuario import CODE_BOT, guardar_url_archivo, enviar_mensaje_imagen
from BotTelegram.procesar_callbackquery import procesar_callback_query
from procesar_comandos import *


## Atiende las peticiones del usuario
def atender_consulta_mensaje_tg(dict_update):

    update_tg = UpdateTG(dict_update)  # Convertimos el dict a una manejable Python Class

    # Cargamos los textos a usar
    root_xml_string = ET.parse(
        join(
            os.path.dirname(os.path.abspath(__file__)),
            "languages",
            "en_US",
            'strings.xml'
        )
    )

    if update_tg.message:

        # Por ahora solo chats privados
        if update_tg.message.chat.type not in ("private"): return

        if update_tg.message.text:
            procesar_mensaje_texto(update_tg.message, root_xml_string, update_tg.is_message_debug)
        elif update_tg.message.photo:
            procesar_mensaje_foto(update_tg.message, root_xml_string, update_tg.is_message_debug)

    elif update_tg.callback_query:
        procesar_callback_query(update_tg,root_xml_string)


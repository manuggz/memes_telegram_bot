#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from os.path import join

from BotTelegram.procesar_callbackquery import procesar_callback_query
from procesar_comandos import *
from BotTelegram.update_tg import UpdateTG
from models import Usuario
import xml.etree.ElementTree as ET
import sys



def atender_consulta_mensaje_tg(dict_update):
    # global root_xml_string,update_tg,usuario_m

    update_tg = UpdateTG(dict_update)  # Convertimos el dict a una manejable Python Class

    # Cargamos los textos a usar
    root_xml_string = ET.parse(join(os.path.dirname(os.path.abspath(__file__)),"languages", "en_US", 'strings.xml'))

    if update_tg.edited_message: return # No manejamos ediciones a mensajes enviados

    # Por ahora solo chats privados
    if update_tg.message and update_tg.message.chat.type not in ("private"): return


    if update_tg.callback_query:
        procesar_callback_query(update_tg,root_xml_string)
        return

    try:
        usuario_m = Usuario.objects.get(id_u=update_tg.message.user_from.id)
    except ObjectDoesNotExist:

        usuario_m = Usuario(
            id_u=update_tg.message.user_from.id,
            nombreusuario=update_tg.message.user_from.username[:200],
            nombre=update_tg.message.user_from.first_name[:200],
            apellido=update_tg.message.user_from.last_name[:200]
        )
        usuario_m.save()

    procesar_comando(
        update_tg.message.chat.id,
        update_tg.is_message_debug,
        update_tg.message.chat.type,
        update_tg.message.datetime,
        usuario_m,
        root_xml_string,
        *extraer_comando(update_tg.message.text)
    )

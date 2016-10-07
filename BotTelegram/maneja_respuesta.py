#!/usr/bin/python
# -*- coding: utf-8 -*-
from os.path import join

from BotTelegram.procesar_callbackquery import procesar_callback_query
from procesar_comandos import *
from BotTelegram.update_tg import UpdateTG
from models import Usuario
import xml.etree.ElementTree as ET
import sys


class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


sys.stdout = Unbuffered(sys.stdout)


def atender_consulta_mensaje_tg(dict_update):
    # global root_xml_string,update_tg,usuario_m

    update_tg = UpdateTG(dict_update)  # Convertimos el dict a una manejable Python Class

    root_xml_string = ET.parse(join("BotTelegram", "languages", "en_US", 'strings.xml'))

    # Por ahora solo grupos "normales" y chats privados
    if update_tg.message and update_tg.message.chat.type not in ("group", "private"): return



    if update_tg.callback_query:
        procesar_callback_query(update_tg,root_xml_string)
        return

    try:
        usuario_m = Usuario.objects.get(id_u=update_tg.message.user_from.id)
    except ObjectDoesNotExist:

        usuario_m = Usuario.objects.create(
            id_u=update_tg.message.user_from.id,
            nombreusuario=update_tg.message.user_from.username[:200],
            nombre=update_tg.message.user_from.first_name[:200],
            apellido=update_tg.message.user_from.last_name[:200]
        )

    if not update_tg.message.text:
        if update_tg.message.new_chat_member:
            if update_tg.message.new_chat_member.username == 'MemesBot':
                # Deberia haber un mensaje de ayuda para un Grupo y para un Chat privado
                enviar_mensaje_ayuda_comando(update_tg.message.chat.id,"help", root_xml_string)

    else:
        procesar_comando(
            update_tg.message.chat.id,
            update_tg.is_message_debug,
            update_tg.message.chat.type,
            update_tg.message.datetime,
            usuario_m,
            root_xml_string,
            *extraer_comando(update_tg.message.text)
        )

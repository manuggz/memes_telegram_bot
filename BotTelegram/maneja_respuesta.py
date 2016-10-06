#!/usr/bin/python
# -*- coding: utf-8 -*-
from os.path import join

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

    if not update_tg.message: return

    tree = ET.parse(join("BotTelegram", "languages", "en_US", 'strings.xml'))
    root_xml_string = tree.getroot()

    # Por ahora solo grupos "normales" y chats privados
    if update_tg.message.chat.type not in ("group", "private"): return

    usuario_m, _ = Usuario.objects.get_or_create(
        id_u=update_tg.message.user_from.id,
        nombreusuario=update_tg.message.user_from.username[:200],
        nombre=update_tg.message.user_from.first_name[:200],
        apellido=update_tg.message.user_from.last_name[:200]
    )

    if not update_tg.message.text:
        if update_tg.message.new_chat_member:
            if update_tg.message.new_chat_member.username == 'MemesBot':
                # Deberia haber un mensaje de ayuda para un Grupo y para un Chat privado
                enviar_mensaje_ayuda_comando("help", update_tg.message.chat.id, root_xml_string)

    else:
        procesar_comandos(update_tg, usuario_m, root_xml_string, *extraer_comando(update_tg.message.text))

# {u'callback_query': {u'message': {u'from': {u'first_name': u'Memes', u'username': u'MemesBot', u'id': 119646075}, u'photo': [{u'height': 67, u'width': 90, u'file_size': 1453, u'file_id': u'AgADAQAD4AABMht7pyEHvLzPzdHlZ-sijOcvAASaBl6bBpvUBVqkAQABAg'}, {u'height': 238, u'width': 320, u'file_size': 15927, u'file_id': u'AgADAQAD4AABMht7pyEHvLzPzdHlZ-sijOcvAAShXaf2995n21ukAQABAg'}, {u'height': 461, u'width': 620, u'file_size': 32026, u'file_id': u'AgADAQAD4AABMht7pyEHvLzPzdHlZ-sijOcvAAQazB8p7xjcdlmkAQABAg'}], u'caption': u'Prueba', u'chat': {u'last_name': u'Gonzalez', u'first_name': u'Manuel', u'username': u'manuggz', u'id': 109518141, u'type': u'private'}, u'date': 1475628904, u'message_id': 106249}, u'data': u'ASD', u'chat_instance': u'-3266157052870893227', u'id': u'470376834033505255', u'from': {u'last_name': u'Gonzalez', u'first_name': u'Manuel', u'username': u'manuggz', u'id': 109518141}}, u'update_id': 25257083}

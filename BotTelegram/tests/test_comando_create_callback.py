# coding=utf-8
from django.test import TestCase
import json


# Create your tests here.
from django.test import override_settings


@override_settings(DEBUG=True)
class TestCreateCallBackRandom(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.user_from = {}
        cls.user_from["first_name"] = "Manuel"
        cls.user_from["last_name"] = "Gonzalez"
        cls.user_from["username"] = "manuggz"
        cls.user_from["id"] = "109518141"

        cls.chat = {}
        cls.chat["first_name"] = "Manuel"
        cls.chat["last_name"] = "Gonzalez"
        cls.chat["username"] = "manuggz"
        cls.chat["type"] = "private"
        cls.chat["id"] = "109518141"

        cls.consulta = {u'message': {u'text': "", u'from': cls.user_from, u'chat': cls.chat, u'message_id': 905475,
                                     u'date': 1475391962}, u'update_id': 25256647, u'debug': True}




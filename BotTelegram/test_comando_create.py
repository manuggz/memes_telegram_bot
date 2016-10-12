# coding=utf-8
from django.test import TestCase
import json


# Create your tests here.
from django.test import override_settings


@override_settings(DEBUG=True)
class TestSimpleCreate(TestCase):
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

    def test_create_sin_imagen_anterior(self):
        self.consulta[u'message'][u'text'] = u"/create"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_create_space(self):
        self.consulta[u'message'][u'text'] = u"/create "
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_space_create(self):
        self.consulta[u'message'][u'text'] = u" /create"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_space_create_space(self):
        self.consulta[u'message'][u'text'] = u" /create "
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_spacex100_create_spacex100(self):
        self.consulta[u'message'][u'text'] = " " * 100 + u"/create " + " " * 100
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_spacex100_create_spacex100_create(self):
        self.consulta[u'message'][u'text'] = " " * 100 + u"/create " + " " * 100 + " create"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_spacex100_create_spacex100_create_space(self):
        self.consulta[u'message'][u'text'] = " " * 100 + u"/create " + " " * 100 + " create "
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_spacex100_create_spacex100_yao_spacex100(self):
        self.consulta[u'message'][u'text'] = " " * 100 + u"/create " + " " * 100 + " yao " + " " * 100
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_spacex100_create_spacex100_create_spacex100_create(self):
        self.consulta[u'message'][u'text'] = " " * 100 + u"/create " + " " * 100 + " create " + " " * 100 + " create"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_create_forever_alone(self):
        self.consulta[u'message'][u'text'] = u"/create Forever Alone"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_create_no_existe(self):
        self.consulta[u'message'][u'text'] = u"/create 123123123123189876761009123781238712989912992"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_double_create(self):
        self.consulta[u'message'][u'text'] = u"/create /create"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    # ---------- Todos los anteriores no utilizan imagen anterior

    def test_simple_create_im_alone(self):
        self.consulta[u'message'][u'text'] = u"forever alone"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.consulta[u'message'][u'text'] = u"/create Im alone"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_create_with_anterior(self):
        self.consulta[u'message'][u'text'] = u"forever alone"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.consulta[u'message'][u'text'] = u"/create"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_create_im_alone_but_with_my_dog(self):
        self.consulta[u'message'][u'text'] = u"forever alone"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.consulta[u'message'][u'text'] = u"/create Im alone - but with my dog"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_create_im_alone_but_with_my_dog_separated(self):
        self.consulta[u'message'][u'text'] = u"forever alone"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.consulta[u'message'][u'text'] = u"/create Im alone"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.consulta[u'message'][u'text'] = u"/create Im alone - but with my dog"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_create_im_alone_but_with_my_dog_separated_but_with_my_dog_separated_(self):
        self.consulta[u'message'][u'text'] = u"forever alone"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.consulta[u'message'][u'text'] = u"/create Im alone"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.consulta[u'message'][u'text'] = u"/create Im alone - but with my dog - but with my dog"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_create_im_alone_(self):
        self.consulta[u'message'][u'text'] = u"forever alone"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.consulta[u'message'][u'text'] = u"/create Im alone-"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_create__im_alone(self):
        self.consulta[u'message'][u'text'] = u"forever alone"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.consulta[u'message'][u'text'] = u"/create -Im alone"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_create__im_alone_(self):
        self.consulta[u'message'][u'text'] = u"forever alone"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.consulta[u'message'][u'text'] = u"/create -Im alone-"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_create__especiales(self):
        self.consulta[u'message'][u'text'] = u"forever alone"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.consulta[u'message'][u'text'] = u"/create @!#$%&/(()~¨--.,ñ{ñ{ñ@@!-!AQW@ł@ł"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_create_im_alone_black(self):
        self.consulta[u'message'][u'text'] = u"forever alone"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.consulta[u'message'][u'text'] = u"/create Im Alone, Black"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_create_im_alone_mal_color(self):
        self.consulta[u'message'][u'text'] = u"forever alone"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.consulta[u'message'][u'text'] = u"/create Im Alone, PsyCongree"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_create_im_alone__mal_color(self):
        self.consulta[u'message'][u'text'] = u"forever alone"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.consulta[u'message'][u'text'] = u"/create Im Alone-, PsyCongree"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_create__im_alone__mal_color(self):
        self.consulta[u'message'][u'text'] = u"forever alone"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.consulta[u'message'][u'text'] = u"/create -Im Alone-, PsyCongree"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_create__im_alone_mal_color(self):
        self.consulta[u'message'][u'text'] = u"forever alone"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.consulta[u'message'][u'text'] = u"/create -Im Alone, PsyCongree"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_create_im_alone__buen_color(self):
        self.consulta[u'message'][u'text'] = u"forever alone"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.consulta[u'message'][u'text'] = u"/create Im Alone-, Red"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_create__im_alone__buen_color(self):
        self.consulta[u'message'][u'text'] = u"forever alone"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.consulta[u'message'][u'text'] = u"/create -Im Alone-, Red"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_create__im_alone_buen_color(self):
        self.consulta[u'message'][u'text'] = u"forever alone"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.consulta[u'message'][u'text'] = u"/create -Im Alone, Red"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_create__im_alone_but_buen_color(self):
        self.consulta[u'message'][u'text'] = u"forever alone"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.consulta[u'message'][u'text'] = u"/create -Im Alone-but, Red"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_create__im_alone__but_buen_color(self):
        self.consulta[u'message'][u'text'] = u"forever alone"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.consulta[u'message'][u'text'] = u"/create -Im Alone--but, Red"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_create__buen_color(self):
        self.consulta[u'message'][u'text'] = u"forever alone"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.consulta[u'message'][u'text'] = u"/create -, Red"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_create___buen_color(self):
        self.consulta[u'message'][u'text'] = u"forever alone"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.consulta[u'message'][u'text'] = u"/create --, Red"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_create____buen_color(self):
        self.consulta[u'message'][u'text'] = u"forever alone"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.consulta[u'message'][u'text'] = u"/create ---, Red"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_creaate____buen_color(self):
        self.consulta[u'message'][u'text'] = u"forever alone"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.consulta[u'message'][u'text'] = u"/creaate ---, Red"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_create__im_alone_but_mal_color(self):
        self.consulta[u'message'][u'text'] = u"forever alone"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.consulta[u'message'][u'text'] = u"/create -Im Alone-but, Redaa"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_create__im_alone__but_mal_color(self):
        self.consulta[u'message'][u'text'] = u"forever alone"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.consulta[u'message'][u'text'] = u"/create -Im Alone--but, Redaaa"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_create__mal_color(self):
        self.consulta[u'message'][u'text'] = u"forever alone"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.consulta[u'message'][u'text'] = u"/create -, Redaaa"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_create___mal_color(self):
        self.consulta[u'message'][u'text'] = u"forever alone"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.consulta[u'message'][u'text'] = u"/create --, Redaaa"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_create____mal_color(self):
        self.consulta[u'message'][u'text'] = u"forever alone"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.consulta[u'message'][u'text'] = u"/create ---, Redaaa"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_creaate____mal_color(self):
        self.consulta[u'message'][u'text'] = u"forever alone"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.consulta[u'message'][u'text'] = u"/creaate ---, Red"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)



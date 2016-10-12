from django.test import TestCase
import json


# Create your tests here.
from django.test import override_settings


@override_settings(DEBUG=True)
class TestSearch(TestCase):

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

    def test_search_sin_comandos(self):
        self.consulta[u'message'][u'text'] = u"/search"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_search_space(self):
        self.consulta[u'message'][u'text'] = u"/search "
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta),content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_space_search(self):
        self.consulta[u'message'][u'text'] = u" /search"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta),content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_space_search_space(self):
        self.consulta[u'message'][u'text'] = u" /search "
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta),content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_spacex100_search_spacex100(self):
        self.consulta[u'message'][u'text'] = " "*100 + u"/search " +" "*100
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta),content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_spacex100_search_spacex100_create(self):
        self.consulta[u'message'][u'text'] = " "*100 + u"/search " +" "*100 + " create"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta),content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_spacex100_search_spacex100_create_space(self):
        self.consulta[u'message'][u'text'] = " "*100 + u"/search " +" "*100 + " create "
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta),content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_spacex100_search_spacex100_yao_spacex100(self):
        self.consulta[u'message'][u'text'] = " "*100 + u"/search " +" "*100 + " yao " + " "*100
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta),content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_spacex100_search_spacex100_create_spacex100_search(self):
        self.consulta[u'message'][u'text'] = " "*100 + u"/search " +" "*100 + " create " + " "*100 + " search"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta),content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_search_forever_alone(self):
        self.consulta[u'message'][u'text'] = u"/search Forever Alone"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)


    def test_search_no_existe(self):
        self.consulta[u'message'][u'text'] = u"/search 123123123123189876761009123781238712989912992"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)


    def test_double_search(self):
        self.consulta[u'message'][u'text'] = u"/search /search"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)





from django.test import TestCase
import json


# Create your tests here.
from django.test import override_settings


@override_settings(DEBUG=True)
class TestHelp(TestCase):

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

    def test_simple_help(self):
        self.consulta[u'message'][u'text'] = u"/help"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta),content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_help_space(self):
        self.consulta[u'message'][u'text'] = u"/help "
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta),content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_space_help(self):
        self.consulta[u'message'][u'text'] = u" /help"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta),content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_space_help_space(self):
        self.consulta[u'message'][u'text'] = u" /help "
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta),content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_spacex100_help_spacex100(self):
        self.consulta[u'message'][u'text'] = " "*100 + u"/help " +" "*100
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta),content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_spacex100_help_spacex100_create(self):
        self.consulta[u'message'][u'text'] = " "*100 + u"/help " +" "*100 + " create"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta),content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_spacex100_help_spacex100_create_space(self):
        self.consulta[u'message'][u'text'] = " "*100 + u"/help " +" "*100 + " create "
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta),content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_spacex100_help_spacex100_create_spacex100(self):
        self.consulta[u'message'][u'text'] = " "*100 + u"/help " +" "*100 + " create " + " "*100
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta),content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_simple_spacex100_help_spacex100_create_spacex100_help(self):
        self.consulta[u'message'][u'text'] = " "*100 + u"/help " +" "*100 + " create " + " "*100 + " help"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta),content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)


    def test_help_search(self):
        self.consulta[u'message'][u'text'] = u"/help search"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_help_create(self):
        self.consulta[u'message'][u'text'] = u"/help create"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_help_random(self):
        self.consulta[u'message'][u'text'] = u"/help random"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_help_next(self):
        self.consulta[u'message'][u'text'] = u"/help next"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_help_potatoe(self):
        "No tema de ayuda"

        self.consulta[u'message'][u'text'] = u"/help potatoe"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)


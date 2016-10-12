from django.test import TestCase
import json
# Create your tests here.

class TestBot(TestCase):

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

        cls.consulta = {u'message':{u'text': "",u'from': cls.user_from,u'chat': cls.chat,u'message_id': 905475,
                         u'date': 1475391962}, u'update_id': 25256647,u'debug':True}


    # def test_start(self):
    #     self.consulta[u'message'][u'text'] = u"/start"
    #     response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
    #                                 json.dumps(self.consulta),content_type="text/json",secure=True)
    #
    #     # Check that the response is 200 OK.
    #     self.assertEqual(response.status_code, 200)
    #
    #
    #
    # def test_search_sin_comandos(self):
    #     self.consulta[u'message'][u'text'] = u"/search"
    #     response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
    #                                 json.dumps(self.consulta), content_type="text/json", secure=True)
    #
    #     # Check that the response is 200 OK.
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_search_forever_alone(self):
    #     self.consulta[u'message'][u'text'] = u"/search Forever Alone"
    #     response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
    #                                 json.dumps(self.consulta), content_type="text/json", secure=True)
    #
    #     # Check that the response is 200 OK.
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_random(self):
    #
    #     self.consulta[u'message'][u'text'] = u"forever alone"
    #     response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
    #                                 json.dumps(self.consulta), content_type="text/json", secure=True)
    #
    #     # Check that the response is 200 OK.
    #     self.assertEqual(response.status_code, 200)
    #
    #     self.consulta[u'message'][u'text'] = u"/random"
    #     response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
    #                                 json.dumps(self.consulta), content_type="text/json", secure=True)
    #
    #     # Check that the response is 200 OK.
    #     self.assertEqual(response.status_code, 200)
    #
    #     self.consulta[u'message'][u'text'] = u"/next"
    #     response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
    #                                 json.dumps(self.consulta), content_type="text/json", secure=True)
    #
    #     # Check that the response is 200 OK.
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_boton_random(self):
    #     self.consulta[u'message'][u'text'] = u"forever alone"
    #     response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
    #                                 json.dumps(self.consulta), content_type="text/json", secure=True)
    #
    #     # Check that the response is 200 OK.
    #     self.assertEqual(response.status_code, 200)
    #
    #     response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
    #                                 json.dumps({u'callback_query': {u'id': u'470376835803901570', u'from': {u'id': 109518141, u'last_name': u'Gonzalez', u'first_name': u'Manuel', u'username': u'manuggz'}, u'chat_instance': u'-3266157052870893227', u'data': u'Random', u'message': {u'from': {u'id': 119646075, u'username': u'MemesBot', u'first_name': u'Memes'}, u'entities': [{u'type': u'bot_command', u'offset': 213, u'length': 5}], u'date': 1475867414, u'text': u"Hey. I can send you memes. Just tell me which one typing its name and if I can remember it\nI'll send you a picture.\n\nExample: Send me yao ming . If you do, i'll send you yao ming's meme.\n\nwanna know more? Send me /help", u'chat': {u'id': 109518141, u'last_name': u'Gonzalez', u'type': u'private', u'first_name': u'Manuel', u'username': u'manuggz'}, u'message_id': 107694}}, u'update_id': 25257687})
    #                                 , content_type="text/json", secure=True)
    #
    #     # Check that the response is 200 OK.
    #     self.assertEqual(response.status_code, 200)
    #
    #     response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
    #                                 json.dumps({u'callback_query': {u'id': u'470376835803901570',
    #                                                                 u'from': {u'id': 109518141, u'last_name': u'Gonzalez',
    #                                                                           u'first_name': u'Manuel',
    #                                                                           u'username': u'manuggz'},
    #                                                                 u'chat_instance': u'-3266157052870893227',
    #                                                                 u'data': u'Next,2', u'message': {
    #                                         u'from': {u'id': 119646075, u'username': u'MemesBot', u'first_name': u'Memes'},
    #                                         u'entities': [{u'type': u'bot_command', u'offset': 213, u'length': 5}],
    #                                         u'date': 1475867414,
    #                                         u'text': u"asd",
    #                                         u'chat': {u'id': 109518141, u'last_name': u'Gonzalez', u'type': u'private',
    #                                                   u'first_name': u'Manuel', u'username': u'manuggz'},
    #                                         u'message_id': 107694}}, u'update_id': 25257687})
    #                                 , content_type="text/json", secure=True)
    #
    #     # Check that the response is 200 OK.
    #     self.assertEqual(response.status_code, 200)
    #

    # def test_simple_create_im_alone(self):
    #
    #     self.consulta[u'message'][u'text'] = u"forever alone"
    #     response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
    #                                 json.dumps(self.consulta), content_type="text/json", secure=True)
    #
    #     # Check that the response is 200 OK.
    #     self.assertEqual(response.status_code, 200)
    #
    #     self.consulta[u'message'][u'text'] = u"/create Im alone"
    #     response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
    #                                 json.dumps(self.consulta), content_type="text/json", secure=True)
    #
    #     # Check that the response is 200 OK.
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_simple_create_im_alone_but_with_my_dog(self):
    #     self.consulta[u'message'][u'text'] = u"forever alone"
    #     response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
    #                                 json.dumps(self.consulta), content_type="text/json", secure=True)
    #
    #     # Check that the response is 200 OK.
    #     self.assertEqual(response.status_code, 200)
    #
    #     self.consulta[u'message'][u'text'] = u"/create Im alone - but with my dog"
    #     response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
    #                                 json.dumps(self.consulta), content_type="text/json", secure=True)
    #
    #     # Check that the response is 200 OK.
    #     self.assertEqual(response.status_code, 200)

    # def test_simple_create_im_alone_but_with_my_dog_separated(self):
    #     self.consulta[u'message'][u'text'] = u"forever alone"
    #     response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
    #                                 json.dumps(self.consulta), content_type="text/json", secure=True)
    #
    #     # Check that the response is 200 OK.
    #     self.assertEqual(response.status_code, 200)
    #
    #     self.consulta[u'message'][u'text'] = u"/create Im alone"
    #     response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
    #                                 json.dumps(self.consulta), content_type="text/json", secure=True)
    #
    #     # Check that the response is 200 OK.
    #     self.assertEqual(response.status_code, 200)
    #
    #     self.consulta[u'message'][u'text'] = u"/create Im alone - but with my dog"
    #     response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
    #                                 json.dumps(self.consulta), content_type="text/json", secure=True)
    #
    #     # Check that the response is 200 OK.
    #     self.assertEqual(response.status_code, 200)

    def test_search_forever_alone_example(self):
        self.consulta[u'message'][u'text'] = u"forever alone"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)


        self.consulta[u'message'][u'text'] = u"/next"
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

        self.consulta[u'message'][u'text'] = u"/create Im alone - but with my dog , black"
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
                                    json.dumps(self.consulta), content_type="text/json", secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    #
    # def test_create_callback(self):
    #
    #
    #     self.consulta[u'message'][u'text'] = u"forever alone"
    #     response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
    #                                 json.dumps(self.consulta), content_type="text/json", secure=True)
    #
    #     # Check that the response is 200 OK.
    #     self.assertEqual(response.status_code, 200)
    #
    #
    #     response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
    #                                 json.dumps({u'callback_query': {u'id': u'470376835803901570',
    #                                                                 u'from': {u'id': 109518141, u'last_name': u'Gonzalez',
    #                                                                           u'first_name': u'Manuel',
    #                                                                           u'username': u'manuggz'},
    #                                                                 u'chat_instance': u'-3266157052870893227',
    #                                                                 u'data': u'Create,1', u'message': {
    #                                         u'from': {u'id': 119646075, u'username': u'MemesBot', u'first_name': u'Memes'},
    #                                         u'entities': [{u'type': u'bot_command', u'offset': 213, u'length': 5}],
    #                                         u'date': 1475867414,
    #                                         u'text': u"asd",
    #                                         u'chat': {u'id': 109518141, u'last_name': u'Gonzalez', u'type': u'private',
    #                                                   u'first_name': u'Manuel', u'username': u'manuggz'},
    #                                         u'message_id': 107694}}, u'update_id': 25257687})
    #                                 , content_type="text/json", secure=True)
    #
    #     # Check that the response is 200 OK.
    #     self.assertEqual(response.status_code, 200)
    #
    #     response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
    #                                 json.dumps({u'callback_query': {u'id': u'470376835803901570',
    #                                                                 u'from': {u'id': 109518141,
    #                                                                           u'last_name': u'Gonzalez',
    #                                                                           u'first_name': u'Manuel',
    #                                                                           u'username': u'manuggz'},
    #                                                                 u'chat_instance': u'-3266157052870893227',
    #                                                                 u'data': u'SetUpperText', u'message': {
    #                                         u'from': {u'id': 119646075, u'username': u'MemesBot',
    #                                                   u'first_name': u'Memes'},
    #                                         u'entities': [{u'type': u'bot_command', u'offset': 213, u'length': 5}],
    #                                         u'date': 1475867414,
    #                                         u'text': u"asd",
    #                                         u'chat': {u'id': 109518141, u'last_name': u'Gonzalez', u'type': u'private',
    #                                                   u'first_name': u'Manuel', u'username': u'manuggz'},
    #                                         u'message_id': 107694}}, u'update_id': 25257687})
    #                                 , content_type="text/json", secure=True)
    #
    #     # Check that the response is 200 OK.
    #     self.assertEqual(response.status_code, 200)
    #
    #     self.consulta[u'message'][u'text'] = u"YO UPPER!"
    #     response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
    #                                 json.dumps(self.consulta), content_type="text/json", secure=True)
    #
    #     # Check that the response is 200 OK.
    #     self.assertEqual(response.status_code, 200)
    #
    #
    #     self.consulta[u'message'][u'text'] = u"/none"
    #     response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
    #                                 json.dumps(self.consulta), content_type="text/json", secure=True)
    #
    #     # Check that the response is 200 OK.
    #     self.assertEqual(response.status_code, 200)
    #
    #     response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
    #                                 json.dumps({u'callback_query': {u'id': u'470376835803901570',
    #                                                                 u'from': {u'id': 109518141,
    #                                                                           u'last_name': u'Gonzalez',
    #                                                                           u'first_name': u'Manuel',
    #                                                                           u'username': u'manuggz'},
    #                                                                 u'chat_instance': u'-3266157052870893227',
    #                                                                 u'data': u'SetLowerText', u'message': {
    #                                         u'from': {u'id': 119646075, u'username': u'MemesBot',
    #                                                   u'first_name': u'Memes'},
    #                                         u'entities': [{u'type': u'bot_command', u'offset': 213, u'length': 5}],
    #                                         u'date': 1475867414,
    #                                         u'text': u"asd",
    #                                         u'chat': {u'id': 109518141, u'last_name': u'Gonzalez', u'type': u'private',
    #                                                   u'first_name': u'Manuel', u'username': u'manuggz'},
    #                                         u'message_id': 107694}}, u'update_id': 25257687})
    #                                 , content_type="text/json", secure=True)
    #
    #     # Check that the response is 200 OK.
    #     self.assertEqual(response.status_code, 200)
    #
    #     self.consulta[u'message'][u'text'] = u"YO LOWER!"
    #     response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
    #                                 json.dumps(self.consulta), content_type="text/json", secure=True)
    #
    #     # Check that the response is 200 OK.
    #     self.assertEqual(response.status_code, 200)
    #
    #     self.consulta[u'message'][u'text'] = u"/none"
    #     response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
    #                                 json.dumps(self.consulta), content_type="text/json", secure=True)
    #
    #     # Check that the response is 200 OK.
    #     self.assertEqual(response.status_code, 200)
    #
    #     self.consulta[u'message'][u'text'] = u"YO LOWER 2!"
    #     response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
    #                                 json.dumps(self.consulta), content_type="text/json", secure=True)
    #
    #     # Check that the response is 200 OK.
    #     self.assertEqual(response.status_code, 200)
    #
    #     response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
    #                                 json.dumps({u'callback_query': {u'id': u'470376835803901570',
    #                                                                 u'from': {u'id': 109518141,
    #                                                                           u'last_name': u'Gonzalez',
    #                                                                           u'first_name': u'Manuel',
    #                                                                           u'username': u'manuggz'},
    #                                                                 u'chat_instance': u'-3266157052870893227',
    #                                                                 u'data': u'SetColor', u'message': {
    #                                         u'from': {u'id': 119646075, u'username': u'MemesBot',u'first_name': u'Memes'},
    #                                         u'entities': [{u'type': u'bot_command', u'offset': 213, u'length': 5}],
    #                                         u'date': 1475867414,
    #                                         u'text': u"asd",
    #                                         u'chat': {u'id': 109518141, u'last_name': u'Gonzalez', u'type': u'private',
    #                                                   u'first_name': u'Manuel', u'username': u'manuggz'},
    #                                         u'message_id': 107694}}, u'update_id': 25257687})
    #                                 , content_type="text/json", secure=True)
    #
    #     # Check that the response is 200 OK.
    #     self.assertEqual(response.status_code, 200)
    #
    #     self.consulta[u'message'][u'text'] = u"Red"
    #     response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
    #                                 json.dumps(self.consulta), content_type="text/json", secure=True)
    #
    #     # Check that the response is 200 OK.
    #     self.assertEqual(response.status_code, 200)
    #
    #     self.consulta[u'message'][u'text'] = u"Black2"
    #     response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',
    #                                 json.dumps(self.consulta), content_type="text/json", secure=True)
    #
    #     # Check that the response is 200 OK.
    #     self.assertEqual(response.status_code, 200)
    #
    #

from django.test import TestCase

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

    def test_start(self):
        mensaje = u"/start"
        consulta = {u'message':
                        {u'text': mensaje,u'from': self.user_from,u'chat': self.chat,u'message_id': 905475,
                         u'date': 1475391962}, u'update_id': 25256647}
        print consulta
        response = self.client.post('/BotTelegram/119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/',str(consulta),content_type="text/json",secure=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

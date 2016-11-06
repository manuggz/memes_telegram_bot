# type : CallbackQuery
# This object represents an incoming callback query from a callback button in an inline keyboard.
# If the button that originated the query was attached to a message sent by the bot, the field message will be present.
# If the button was attached to a message sent via the bot (in inline mode), the field inline_message_id will be present.
#  Exactly one of the fields data or game_short_name will be present.
from BotTelegram.ClasesTG.message_tg import MessageTG
from BotTelegram.ClasesTG.user_tg import UserTG


class CallbackQueryTG:

    def __init__(self,dict_callbackquery):

        # type:String
        # Unique identifier for this query
        self.id = dict_callbackquery["id"]

        # type: User
        # Sender
        self.user_from = dict_callbackquery["from"]
        self.user_from = UserTG(self.user_from)

        # type: Message
        # Optional. Message with the callback button that originated the query.
        # Note that message content and message date will not be available if the message is too old
        self.message = dict_callbackquery.get("message","")
        if self.message:
            self.message = MessageTG(self.message)

        # type: String
        # Optional. Identifier of the message sent via the bot in inline mode, that originated the query.
        self.inline_message_id = dict_callbackquery.get("inline_message_id","")

        # type: String
        # Identifier, uniquely corresponding to the chat to which the message with the callback button was sent.
        # Useful for high scores in games.
        self.chat_instance = dict_callbackquery["chat_instance"]

        # type: String
        # Optional. Data associated with the callback button.
        # Be aware that a bad client can send arbitrary data in this field.
        self.data = dict_callbackquery.get("data","")


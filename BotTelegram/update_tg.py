# coding=utf-8
from BotTelegram.message_tg import MessageTG


class UpdateTG:

    def __init__(self,dict_update):

        # type: Integer
        # The update‘s unique identifier.
        # Update identifiers start from a certain positive number and increase sequentially.
        # This ID becomes especially handy if you’re using Webhooks, since it allows you to ignore repeated updates or
        # to restore the correct update sequence, should they get out of order.
        self.update_id = dict_update["update_id"]

        # type: Messaje
        # Optional. New incoming message of any kind — text, photo, sticker, etc.
        self.message = dict_update.get("message","")
        if self.message:
            self.message = MessageTG(self.message)



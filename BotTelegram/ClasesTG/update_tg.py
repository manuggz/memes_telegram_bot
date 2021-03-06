# coding=utf-8


# This object represents an incoming update.
# Only one of the optional parameters can be present in any given update.
from BotTelegram.ClasesTG.callbackquery_tg import CallbackQueryTG
from BotTelegram.ClasesTG.message_tg import MessageTG


class UpdateTG:

    def __init__(self,dict_update):

        # type: Integer
        # The update‘s unique identifier.
        # Update identifiers start from a certain positive number and increase sequentially.
        # This ID becomes especially handy if you’re using Webhooks, since it allows you to ignore repeated
        # updates or to restore the correct update sequence, should they get out of order.
        self.update_id = dict_update["update_id"]

        # type: Messaje
        # Optional. New incoming message of any kind — text, photo, sticker, etc.
        self.message = dict_update.get("message","")
        if self.message:
            self.message = MessageTG(self.message)

        # type: Messaje
        # Optional. Optional. New version of a message that is known to the bot and was edited
        self.edited_message = dict_update.get("edited_message","")
        #if self.edited_message:
        #    self.edited_message = MessageTG(self.edited_message)

        # type: CallbackQuery
        # Optional. New incoming callback query
        self.callback_query = dict_update.get("callback_query","")
        if self.callback_query:
            self.callback_query = CallbackQueryTG(self.callback_query)

        self.is_message_debug = dict_update.get("debug", False)





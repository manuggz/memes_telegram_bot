import datetime


class WebhookTG:

    def __init__(self,dict_webhook):

        # String 	Webhook URL, may be empty if webhook is not set up
        self.url = dict_webhook["url"]

        # Boolean 	True, if a custom certificate was provided for webhook certificate checks
        self.has_custom_certificate = dict_webhook["has_custom_certificate"]

        # Integer 	Number of updates awaiting delivery
        self.pending_update_count = dict_webhook["pending_update_count"]

        # Integer
        # Optional. Unix time for the most recent error that happened w
        # hen trying to deliver an update via webhook
        self.last_error_date = dict_webhook.get("last_error_date",0)
        if self.last_error_date:
            self.last_error_date = datetime.datetime.utcfromtimestamp(int(self.last_error_date))

        #String
        # Optional. Error message in human-readable format for the most recent error
        # that happened when trying to deliver an update via webhook
        self.last_error_message = dict_webhook.get("last_error_message","")


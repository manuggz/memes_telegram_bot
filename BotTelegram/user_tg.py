# coding=utf-8


class UserTG:
    def __init__(self, dict_user):
        # Type: Integer
        # Unique identifier for this user or bot
        self.id = dict_user["id"]

        # Type: String
        # User‘s or bot’s first name
        self.first_name = dict_user["first_name"]

        # Type: String
        # User‘s or bot’s last name
        self.last_name = dict_user.get("last_name", None)

        # Type: String
        # User‘s or bot’s username
        self.username = dict_user.get("username", None)

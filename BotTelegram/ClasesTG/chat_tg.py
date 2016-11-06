# coding=utf-8


class ChatTG:
    def __init__(self,dict_chat):

        # Type: Integer
        # Unique identifier for this chat.
        # This number may be greater than 32 bits and some programming languages may have
        # difficulty/silent defects in interpreting it. But it smaller than 52 bits,
        # so a signed 64 bit integer or double-precision float type are safe for storing this identifier.
        self.id = dict_chat["id"]

        # Type: String
        # Type of chat, can be either “private”, “group”, “supergroup” or “channel”
        self.type = dict_chat["type"]

        # Type: String
        # Optional. Title, for supergroups, channels and group chats
        self.title = dict_chat.get("title","")

        # Type: String
        # Optional. Username, for private chats, supergroups and channels if available
        self.username = dict_chat.get("username","")

        # Type: String
        # Optional. First name of the other party in a private chat
        self.first_name = dict_chat.get("first_name","")

        # Type: String
        # Optional. Last name of the other party in a private chat
        self.last_name = dict_chat.get("last_name","")

        # Type: String
        # Optional. True if a group has ‘All Members Are Admins’ enabled.
        self.all_members_are_administrators = dict_chat.get("all_members_are_administrators","")
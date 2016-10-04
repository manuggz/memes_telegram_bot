# coding=utf-8
from user_tg import UserTG
from chat_tg import ChatTG

class MessajeTG:

    def __int__(self, dict_message):

        # type:Integer
        # Unique message identifier
        self.message_id = dict_message["message_id"]

        # type:User
        # Optional. Sender, can be empty for messages sent to channels
        self.user_from = dict_message.get("from", None)
        if self.user_from:
            self.user_from = UserTG(self.user_from)

        # type:Integer
        # Date the message was sent in Unix time
        self.date = dict_message["date"]

        # Type: Chat
        # Conversation the message belongs to
        self.chat = dict_message["chat"]
        self.chat = ChatTG(self.chat)

        # Type: String
        # Optional. For text messages, the actual UTF-8 text of the message, 0-4096 characters.
        self.text = dict_message.get("text", None)

        # Type: Array of MessageEntity
        # Optional. For text messages, special entities like usernames, URLs, bot commands, etc.
        # that appear in the text
        self.entities = dict_message.get("entities", None)

        # Type:Array of PhotoSize
        # Optional. Message is a photo, available sizes of the photo
        self.photo = dict_message.get("photo", None)

        # Type: String, Optional. Caption for the document, photo or video, 0-200 characters
        self.caption = dict_message.get("caption", None)

        # Type: User
        # Optional. A new member was added to the group, information about them
        # (this member may be the bot itself)
        self.new_chat_member = dict_message.get("new_chat_member", None)
        if self.new_chat_member:
            self.new_chat_member = UserTG(self.new_chat_member)

        # Type: User
        # Optional. A new member was removed from the group, information about them
        # (this member may be the bot itself)
        self.left_chat_member = dict_message.get("left_chat_member", None)
        if self.left_chat_member:
            self.left_chat_member = UserTG(self.left_chat_member)



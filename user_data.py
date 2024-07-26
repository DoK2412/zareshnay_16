"""Файл предназначен для реализации класса пользователя"""


class User:
    user = dict()

    def __init__(self, chat_id, first_name, last_name, username):

        self.id_chat = chat_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.id_user = None
        self.rights = None
        self.date = None
        self.apartment = None


    @classmethod
    def get_user(cls,chat_id, first_name, last_name, username):
        if chat_id in cls.user.keys():
            return cls.user[chat_id]
        else:
            return cls.add_user(chat_id, first_name, last_name, username)

    @classmethod
    def add_user(cls, chat_id, first_name, last_name, username):
        cls.user[chat_id] = User(chat_id, first_name, last_name, username)
        return cls.user[chat_id]
    
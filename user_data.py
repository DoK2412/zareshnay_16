"""Файл предназначен для реализации класса пользователя"""


class Users:
    user = dict()

    def __init__(self, chat_id, first_name, last_name, username):

        self.id_chat = chat_id         # id чата *
        self.id_user = None
        self.first_name = first_name               # имя пользователя *
        self.last_name = last_name
        self.username = username            # фамилия пользователя *
        self.telophone = None          # номер телефона
        self.arrival_date = None
        self.login = None
        self.password = None
        self.room = None
        self.user_name_ad = None
        self.first_name_ad = None
        self.last_name_ad = None
        self.id_archive = None

    @classmethod
    def get_user(cls,chat_id, first_name, last_name, username):
        if chat_id in cls.user.keys():
            return cls.user[chat_id]
        else:
            return cls.add_user(chat_id, first_name, last_name, username)

    @classmethod
    def add_user(cls, chat_id, first_name, last_name, username):
        cls.user[chat_id] = Users(chat_id, first_name, last_name, username)
        return cls.user[chat_id]
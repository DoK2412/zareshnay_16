import datetime
import os
import telebot  # подключение бота
from telebot import types  # тип данных для кнопок
import user_data  # подключение класса пользователей
from auth import token
import logging.config  # подключение файла конфигурации
from logger import logger_config  # импорт логгера

from telegram_bot_calendar import DetailedTelegramCalendar

import emoji


import queries_database as qd
from sqlmodel import Session
import sqlbase as cbd


from datetime import date
logging.config.dictConfig(logger_config)  # подключение файла логеров
log_error = logging.getLogger('app_error')  # создание сборщика ошибок
log_info = logging.getLogger('app_info')  # создание сборщика неверных вводов


token = token
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def startBotWorck(message):
    try:
        user = user_data.Users.get_user(message.chat.id,
                                        message.from_user.first_name,
                                        message.from_user.last_name,
                                        message.from_user.username)

        with Session(cbd.engin) as session:
            user_id = session.execute(qd.ID_USER_DB.format(f"{message.from_user.id}")).all()
            print(user_id)
            if user_id:
                if user_id[0].user_type == 'user':
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    buttom1 = types.KeyboardButton(emoji.emojize('\U0001F4F9 Получение доступа'))
                    buttom2 = types.KeyboardButton(emoji.emojize('\U0001F510 Проверка доступа'))
                    buttom3 = types.KeyboardButton( emoji.emojize('\U0001F4C3 Справочная информация'))
                    buttom4 = types.KeyboardButton(emoji.emojize('\U0001F5A5 Запрос записи из архива'))
                    markup.add(buttom1, buttom2, buttom3, buttom4)

                    bot.send_message(message.chat.id, emoji.emojize(f'Доброго времени суток {message.from_user.first_name}. \U0001F44B  '
                                                      f'\n\nДанный бот предназначен для информирования жителей дома'
                                                      f' о работе видеонаблюдения \U0001F3A5, а так же получения информации о'
                                                      f' предоставлении доступа к системе видеонаблюдения и проверки активности доступа собственников.\U0001F512'), reply_markup=markup)
                elif user_id[0].user_type == 'admin':
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    buttom1 = types.KeyboardButton(emoji.emojize('\U0001F4F9 Получение доступа'))
                    buttom2 = types.KeyboardButton(emoji.emojize('\U0001F510 Проверка доступа'))
                    buttom3 = types.KeyboardButton(emoji.emojize('\U0001F4C3 Справочная информация'))
                    buttom4 = types.KeyboardButton(emoji.emojize('\U0001F5A5 Запрос записи из архива'))
                    buttom5 = types.KeyboardButton(emoji.emojize('\U0001F4D6 Запрос сведений о собственнике'))
                    buttom6 = types.KeyboardButton(emoji.emojize('\U0001F4F2 Запрос сведений о запросах архива'))
                    buttom7 = types.KeyboardButton(emoji.emojize('\U0001F4DD Добавить в базу'))
                    markup.add(buttom1, buttom2, buttom3, buttom4, buttom5)
                    markup.add(buttom6, buttom7)

                    bot.send_message(message.chat.id,
                                     emoji.emojize(f'Доброго времени суток {message.from_user.first_name}. \U0001F44B  '
                                                   f'\n\nДанный бот предназначен для информирования жителей дома'
                                                   f' о работе видеонаблюдения \U0001F3A5, а так же получения информации о'
                                                   f' предоставлении доступа к системе видеонаблюдения и проверки активности доступа собственников.\U0001F512'),
                                     reply_markup=markup)
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                buttom1 = types.KeyboardButton(emoji.emojize('\U0001F50F Авторизоваться'))
                markup.add(buttom1)

                bot.send_message(message.chat.id,
                                 emoji.emojize(f'Доброго времени суток {message.from_user.first_name}. \U0001F44B  '
                                               f'\n\nДанный бот предназначен для информирования жителей дома'
                                               f' о работе видеонаблюдения \U0001F3A5, а так же получения информации о'
                                               f' предоставлении доступа к системе видеонаблюдения и проверки активности доступа собственников.\U0001F512'),
                                 reply_markup=markup)
    except Exception as ex:
        bot.send_message(message.chat.id, 'При выполении запроса возникла ошибка.\nПопробуйде повторно произвести запрос.')
        log_error.error(
            f'Пользователь {message.from_user.id} {message.from_user.username} ошибка при выполнении {ex}.')
        raise ex


@bot.message_handler(content_types=['text'])
def bot_messag(message):
    try:
        user = user_data.Users.get_user(message.chat.id,
                                        message.from_user.first_name,
                                        message.from_user.last_name,
                                        message.from_user.username)
        if message.chat.type == 'private':
            if message.text == '\U0001F4F9 Получение доступа':
                log_info.info(f'Пользователь {message.from_user.id} {message.from_user.username} запросил информацию о предоставлении доступа')
                bot.send_message(message.chat.id, 'Для получения доступа к системе видеонаблюдения Вам необходимо написать заявление '
                                                  'на предоставление доступа и передать его Дмитрию либо положить в 71 почтовый ящик '
                                                  '(наилучший выбор). \nОповестить Дмитрия в телеграмм.')
                markup = types.InlineKeyboardMarkup()
                switch_button_1 = types.InlineKeyboardButton(text='Перейти в чат',
                                                             url='https://t.me/DoK2412')
                markup.add(switch_button_1)

                bot.send_message(message.chat.id, 'Дмитрий Уранов', reply_markup=markup)

                bot.send_photo(message.chat.id, (open(os.path.join('photo_2023-05-10_13-15-40.jpg'), "rb")), timeout=30)
            elif message.text == '\U0001F4C3 Справочная информация':
                log_info.info(f'Пользователь {message.from_user.id} {message.from_user.username} запросил справочную информацию.')
                bot.send_message(message.chat.id, 'Доступ к камерам:\n\n'
                                                  '     Доступ собственникам предоставляется к камерам по периметру дома, а так же к камерам внутреннего наблюдения кроме камер в лифтах.\n'
                                                  '     Это связано с тем что камеры в лифтах пишут звук, а так же через них возможно просматривать личную информацию жителей на их мобильных устройствах.\n'
                                                  '     Из за возможного факта вмешательства в частную жизнь граждан (137 статья УК РФ нарушение неприкосновенности частной жизни) было принято решение эти камеры ограничить.\n\n'
                                                  'Записи из архива:\n\n'
                                                  '     У каждого собственника есть право запросить видео из архива сообщив необходимую дату и примерное время.\n'
                                                  '     Эту процедуру можно провести нескилькими способами:\n\n'
                                                  '     1. Написать заявление во Fryazino.net и ожидать их ответа,\n'
                                                  '     2. Оставить заявку в чат боте и в свободное от работы время Дмитрий (@DoK2412) поднимет архив и сделает вырезку из него.\n'
                                                  '     3. Срок хранения архива составляет 2 недели (14 дней);\n\n'
                                                  'Проверка доступа:\n\n'
                                                  '     Проверить получение доступа к онлайн просмотру вы можете посмотреть в разделе "Проверка доступа" \nТолько информирование о статусе заявки.\n'
                                                  '')
            elif message.text == '\U0001F5A5 Запрос записи из архива':
                log_info.info(f'Пользователь {message.from_user.id} {message.from_user.username} запросил запись архива')
                arrival_date(message)
            elif message.text == '\U0001F50F Авторизоваться':
                authorization(message)
            elif message.text == '\U0001F510 Проверка доступа':
                access_check(message)
            elif message.text == '\U0001F4D6 Запрос сведений о собственнике':
                log_info.info(
                    f'Пользователь {message.from_user.id} {message.from_user.username} запросил информацию о собственнике квартиры.')
                get_owner(message)
            elif message.text == '\U0001F4F2 Запрос сведений о запросах архива':
                get_archive(message)
            elif message.text == '\U0001F4DD Добавить в базу':
                markup = types.InlineKeyboardMarkup()
                switch_button_1 = types.InlineKeyboardButton(text='Добавить пользователя', callback_data='Добавить пользователя')
                switch_button_2 = types.InlineKeyboardButton(text='Добавить учетные данные', callback_data='Добавить учетку')
                switch_button_3 = types.InlineKeyboardButton(text='Удалить', callback_data='Удалить')
                switch_button_4 = types.InlineKeyboardButton(text='Подтвердить', callback_data='Подтвердить')
                switch_button_5 = types.InlineKeyboardButton(text='Смена прав доступа', callback_data='Смена')
                switch_button_6 = types.InlineKeyboardButton(text='Закрыть запрос архива', callback_data='Исполнение')



                markup.add(switch_button_1)
                markup.add(switch_button_2)
                markup.add(switch_button_3)
                markup.add(switch_button_4)
                markup.add(switch_button_5)
                markup.add(switch_button_6)



                bot.send_message(message.chat.id, "Укажите команду", reply_markup=markup)
    except Exception as ex:
        bot.send_message(message.chat.id,
                         'При выполении запроса возникла ошибка.\nПопробуйде повторно произвести запрос.')
        log_error.error(
            f'Пользователь {message.from_user.id} {message.from_user.username} ошибка при выполнении {ex}.')
        raise ex



def arrival_date(message):
    """
    Функция для обработки даты заезда от пользователя
    состоящая из функций:
    arrival_date() - формирующуя запроса на вывод календаря для
                     ввода даты
    cal() - получает данные от пользователя, формирует их в дату,
            сверяет с текущей датой и по результатам проверки
            сохраняет результат и продолжает следующий вызов
            на ввод даты выезда. Либо повторяет запрос даты если
            она не соответстует требованиям.
    """
    try:
        user = user_data.Users.get_user(message.chat.id,
                                        message.from_user.first_name,
                                        message.from_user.last_name,
                                        message.from_user.username)
        calendar, step = DetailedTelegramCalendar(calendar_id=1,
                                                  locale='ru').build()
        bot.send_message(message.chat.id,
                         'Выберите необходимую дату.',
                         reply_markup=calendar)
    except Exception as ex:
        bot.send_message(message.chat.id,
                         'При выполении запроса возникла ошибка.\nПопробуйде повторно произвести запрос.')
        log_error.error(
            f'Пользователь {message.from_user.id} {message.from_user.username} ошибка при выполнении {ex}.')
        raise ex


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
def cal(call):
    try:
        """Функция запроса необходимой даты"""
        user = user_data.Users.get_user(call.message.chat.id,
                                        call.message.from_user.first_name,
                                        call.message.from_user.last_name,
                                        call.message.from_user.username)
        result, key, step = DetailedTelegramCalendar(calendar_id=1, locale='ru').process(call.data)
        if not result and key:
            bot.edit_message_text('Выберите необходимую дату.',
                                  call.message.chat.id,
                                  call.message.message_id,
                                  reply_markup=key)
        elif result:
            if (date.today() - result).days > 14:
                # log_info.info(f'{user.name} {user.surname} ввел неверную'
                #               f' дату срок хранения архива 14 дней.{result}')
                bot.edit_message_text('Введенная вами дата не должна '
                                      'превышать срок хранения архива (14 дней).'
                                      '\nПовторите выбор.',
                                      call.message.chat.id,
                                      call.message.message_id)
                log_info.info(f'Пользователь {call.message.from_user.id} {call.message.from_user.username} ввел разрыв больше даты сохранности архива. Введенная дата {result}')
                arrival_date(call.message)  # повторный запрос при неверном вводе
            elif result > date.today():
                bot.edit_message_text('Введенная вами дата не должна '
                                      'превышать нынешнюю дату.'
                                      '\nПовторите выбор.',
                                      call.message.chat.id,
                                      call.message.message_id)
                log_info.info(f'Пользователь {call.message.from_user.id} {call.message.from_user.username} ввел дату больше нынешней. Введенная дата {result}')
                arrival_date(call.message)
            else:
                # определение времени в случае успешного ввода
                user.arrival_date = result
                bot.edit_message_text(f"Выбрана дата: {result}",
                                      call.message.chat.id,
                                      call.message.message_id)
                log_info.info(f'Пользователь {call.message.from_user.id} {call.message.from_user.username} ввел дату {result}')
                time_user(call.message)  # переход к следующему действию
    except Exception as ex:
        bot.send_message(call.message.chat.id,
                         'При выполении запроса возникла ошибка.\nПопробуйде повторно произвести запрос.')
        log_error.error(
            f'Пользователь {call.message.from_user.id} {call.message.from_user.username} ошибка при выполнении {ex}.')
        raise ex

def time_user(message):
    "Функция запроса диапазона времени необходимой записи"
    try:
        user = user_data.Users.get_user(message.chat.id,
                                        message.from_user.first_name,
                                        message.from_user.last_name,
                                        message.from_user.username)

        bot.edit_message_text('Введите примерный диапазон необходимого времени:\n Например: с 10.00 до 13.00',
                              message.chat.id,
                              message.message_id)
        bot.register_next_step_handler(message, examination_time)
    except Exception as ex:
        bot.send_message(message.chat.id,
                         'При выполении запроса возникла ошибка.\nПопробуйде повторно произвести запрос.')
        log_error.error(
            f'Пользователь {message.from_user.id} {message.from_user.username} ошибка при выполнении {ex}.')
        raise ex

def examination_time(message):
    try:
        user = user_data.Users.get_user(message.chat.id,
                                        message.from_user.first_name,
                                        message.from_user.last_name,
                                        message.from_user.username)
        with Session(cbd.engin) as session:
            user_id = session.execute(qd.ID_USER_DB.format(f"{message.from_user.id}")).all()
            session.exec(qd.ENTRY_DATABASE.format(user_id[0][0], f"'{user.arrival_date}'", f"'{message.text}'"))
            session.commit()
        log_info.info(f'Пользователь {message.from_user.id} {message.from_user.username} ввел  время {message.text}')
        log_info.info(f'Дата и время пользователя  {message.from_user.id} {message.from_user.username} записаны в базу.')
        bot.send_message(message.chat.id, 'Дата и время записаны в запрос.' )
    except Exception as ex:
        bot.send_message(message.chat.id,
                         'При выполении запроса возникла ошибка.\nПопробуйде повторно произвести запрос.')
        log_error.error(
            f'Пользователь {message.from_user.id} {message.from_user.username} ошибка при выполнении {ex}.')
        raise ex

def authorization(message):
    try:
        """Функция авторизации в боте"""
        user = user_data.Users.get_user(message.chat.id,
                                        message.from_user.first_name,
                                        message.from_user.last_name,
                                        message.from_user.username)
        bot.send_message(message.chat.id, 'Введите номер вашей квартиры (цифрами):' )
        bot.register_next_step_handler(message, authorization_room)
    except Exception as ex:
        bot.send_message(message.chat.id,
                         'При выполении запроса возникла ошибка.\nПопробуйде повторно произвести запрос.')
        log_error.error(
            f'Пользователь {message.from_user.id} {message.from_user.username} ошибка при выполнении {ex}.')
        raise ex

def authorization_room(message):
    try:
        user = user_data.Users.get_user(message.chat.id,
                                        message.from_user.first_name,
                                        message.from_user.last_name,
                                        message.from_user.username)

        if message.text.isnumeric() == True:
            with Session(cbd.engin) as session:
                room_id = session.execute(qd.ID_ROOM_DB.format(message.text)).all()
                if room_id:
                    bot.send_message(message.chat.id, 'Данная квартира уже зарегистрирована в системе.\nПовторите ввод')
                    log_info.info(f'Пользователь {message.from_user.id} {message.from_user.username} ввел номер существующий номер квартиры {message.text}.')
                    authorization(message)
                else:
                    dat = str(date.today()).replace('-', '.')
                    session.exec(qd.NEW_USER.format(int(message.text), True, 139, f"'{dat}'", f"'{message.from_user.username}'", message.from_user.id, False, False, "'user'"))
                    session.commit()
                    bot.send_message(message.chat.id, 'Пользователь записан в базу данных.')
                    log_info.info(f'Пользователь {message.from_user.id} {message.from_user.username} авторизовался и записан в базу данных.')
                    startBotWorck(message)
        else:
            bot.send_message(message.chat.id, 'Номер квартиры должен быть числом.\nПовторите ввод')
            log_info.info(f'Пользователь {message.from_user.id} {message.from_user.username} ввел номер не соответствующий типу {message.text}.')

            authorization(message)
    except Exception as ex:
        bot.send_message(message.chat.id,
                         'При выполении запроса возникла ошибка.\nПопробуйде повторно произвести запрос.')
        log_error.error(
            f'Пользователь {message.from_user.id} {message.from_user.username} ошибка при выполнении {ex}.')
        raise ex


def access_check(message):
    try:
        """Функция проверки доступа к просмотру онлайна"""
        user = user_data.Users.get_user(message.chat.id,
                                        message.from_user.first_name,
                                        message.from_user.last_name,
                                        message.from_user.username)

        with Session(cbd.engin) as session:
            user_id = session.execute(qd.USER_ACCESS_DB.format(f"{message.from_user.id}")).all()
            if user_id[0][0] != None:
                log_info.info(f'Пользователь {message.from_user.id} {message.from_user.username} проверил допуск к онлайн просмотру. Статус:  {user_id[0][0]}.')
                bot.send_message(message.chat.id, 'Доступ предоставлен.')
            else:
                log_info.info(f'Пользователь {message.from_user.id} {message.from_user.username} проверил допуск к онлайн просмотру. Статус:  {user_id[0][0]}.')
                bot.send_message(message.chat.id, 'Доступ не предоставлен.')
    except Exception as ex:
        bot.send_message(message.chat.id,
                         'При выполении запроса возникла ошибка.\nПопробуйде повторно произвести запрос.')
        log_error.error(
            f'Пользователь {message.from_user.id} {message.from_user.username} ошибка при выполнении {ex}.')
        raise ex

def get_owner(message):
    """Функция возврата данных о собственнике"""
    try:
        user = user_data.Users.get_user(message.chat.id,
                                        message.from_user.first_name,
                                        message.from_user.last_name,
                                        message.from_user.username)

        bot.send_message(message.chat.id, 'Введите номер необходимой квартиры.')
        bot.register_next_step_handler(message, get_number_room)
    except Exception as ex:
        bot.send_message(message.chat.id,
                         'При выполении запроса возникла ошибка.\nПопробуйде повторно произвести запрос.')
        log_error.error(
            f'Пользователь {message.from_user.id} {message.from_user.username} ошибка при выполнении {ex}.')
        raise ex

def get_number_room(message):
    try:
        user = user_data.Users.get_user(message.chat.id,
                                        message.from_user.first_name,
                                        message.from_user.last_name,
                                        message.from_user.username)
        try:
            if int(message.text):
                with Session(cbd.engin) as session:
                    room_owner = session.execute(qd.USER_DATA.format(message.text)).all()
                    if room_owner:
                        if room_owner[0].onlain:
                            onlain = "Доступ предоставлен"
                        else:
                            onlain = "Доступ не предоставлен"
                        if room_owner[0].blocking:
                            blocking = 'Доступ запрещен'
                        else:
                            blocking = 'Доступ разрешен'


                        bot.send_message(message.chat.id, f'Номер квартиры: {room_owner[0].room},\n'
                                                          f'Фамилия: {room_owner[0].surname},\n'
                                                          f'Имя: {room_owner[0].name},\n'
                                                          f'Отчество: {room_owner[0].surname_end},\n'
                                                          f'Тип пользователя: {room_owner[0].user_type},\n'
                                                          f'Доступ к онлайну: {onlain},\n'
                                                          f'Блокировка: {blocking},\n'
                                                          f'Номер телефона {room_owner[0].number},\n' 
                                                          f'Логин: {room_owner[0].login},\n' 
                                                          f'Пароль: {room_owner[0].password}.\n')
                    else:
                        bot.send_message(message.chat.id, 'Собственнника с данным номером квартиры не найдено в базе.')

        except Exception as ex:
            bot.send_message(message.chat.id, 'Не верный ввод квартиры.\nПовторите ввод.')
            log_error.error(
                f'Пользователь {message.from_user.id} {message.from_user.username} ошибка при выполнении {ex}.')
            get_owner(message)
    except Exception as ex:
        bot.send_message(message.chat.id,
                         'При выполении запроса возникла ошибка.\nПопробуйде повторно произвести запрос.')
        log_error.error(
            f'Пользователь {message.from_user.id} {message.from_user.username} ошибка при выполнении {ex}.')
        raise ex


def get_archive(message):
    try:
        user = user_data.Users.get_user(message.chat.id,
                                        message.from_user.first_name,
                                        message.from_user.last_name,
                                        message.from_user.username)

        with Session(cbd.engin) as session:
            archive_all = session.execute(qd.USER_ARCHIVE).all()
            if len(archive_all) == 0:
                bot.send_message(message.chat.id,
                                 'В архиве нет заявок.')
            for i_archive_all in archive_all:
                bot.send_message(message.chat.id, f'Пользователь: {i_archive_all.surname} {i_archive_all.name} {i_archive_all.surname_end},\n'
                                                  f'Номер запроса в базе: {i_archive_all.id_video},\n'
                                                  f'Номер квартиры: {i_archive_all.room},\n'
                                                  f'Необходимая дата: {i_archive_all.date},\n'
                                                  f'Необходимое время: {i_archive_all.time}.')
    except Exception as ex:
        bot.send_message(message.chat.id,
                         'При выполении запроса возникла ошибка.\nПопробуйде повторно произвести запрос.')
        log_error.error(
            f'Пользователь {message.from_user.id} {message.from_user.username} ошибка при выполнении {ex}.')
        raise ex


@bot.callback_query_handler(func=lambda call: call.data in ['Добавить учетку'])
def add_user_login(message):
    user = user_data.Users.get_user(message.from_user.id,
                                    message.from_user.first_name,
                                    message.from_user.last_name,
                                    message.from_user.username)

    bot.send_message(message.from_user.id, 'Введите логин собственника.')
    bot.register_next_step_handler(message.message, add_user_passvord)

def add_user_passvord(message):
    user = user_data.Users.get_user(message.from_user.id,
                                    message.from_user.first_name,
                                    message.from_user.last_name,
                                    message.from_user.username)
    user.login = message.text

    bot.send_message(message.from_user.id, 'Введите пароль собственника.')
    bot.register_next_step_handler(message, add_number)

def add_number(message):
    user = user_data.Users.get_user(message.from_user.id,
                                    message.from_user.first_name,
                                    message.from_user.last_name,
                                    message.from_user.username)
    user.password = message.text

    bot.send_message(message.from_user.id, 'Введите номер квартиры собственника.')
    bot.register_next_step_handler(message, add_entry)

def add_entry(message):
    user = user_data.Users.get_user(message.from_user.id,
                                    message.from_user.first_name,
                                    message.from_user.last_name,
                                    message.from_user.username)
    user.room = message.text
    type = 'user'


    with Session(cbd.engin) as session:
        room_id = session.execute(qd.ADD_INPUT_DATA.format(int(user.room), "'62.140.252.182:8010'", f"'{user.login}'", f"'{user.password}'", f"'{datetime.datetime.now().date()}'", f"'{type}'"))
        session.commit()
        bot.send_message(message.from_user.id, 'Учетка собственника добавлена в базу данных.')


@bot.callback_query_handler(func=lambda call: call.data in ['Подтвердить'])
def add_user_login(message):
    user = user_data.Users.get_user(message.from_user.id,
                                    message.from_user.first_name,
                                    message.from_user.last_name,
                                    message.from_user.username)

    bot.send_message(message.from_user.id, 'Введите номер квартиры собственника.')
    bot.register_next_step_handler(message.message, confirmation)

def confirmation(message):
    user = user_data.Users.get_user(message.from_user.id,
                                    message.from_user.first_name,
                                    message.from_user.last_name,
                                    message.from_user.username)
    room = message.text

    with Session(cbd.engin) as session:
        room_id = session.execute(
            qd.UPDATE_USER.format(int(room), f"'{datetime.datetime.now().date()}'"))
        session.commit()
    bot.send_message(message.from_user.id, 'Передача данных собственнику зафиксирована.')


@bot.callback_query_handler(func=lambda call: call.data in ['Добавить пользователя'])
def add_user_name(message):
    user = user_data.Users.get_user(message.from_user.id,
                                    message.from_user.first_name,
                                    message.from_user.last_name,
                                    message.from_user.username)

    bot.send_message(message.from_user.id, 'Введите имя собственника.')
    bot.register_next_step_handler(message.message, add_user_first_name)

def add_user_first_name(message):
    user = user_data.Users.get_user(message.from_user.id,
                                    message.from_user.first_name,
                                    message.from_user.last_name,
                                    message.from_user.username)
    user.user_name_ad = message.text

    bot.send_message(message.from_user.id, 'Введите фамилию собственника.')
    bot.register_next_step_handler(message, add_user_name_dad)



def add_user_name_dad(message):
    user = user_data.Users.get_user(message.from_user.id,
                                    message.from_user.first_name,
                                    message.from_user.last_name,
                                    message.from_user.username)
    user.first_name_ad = message.text

    bot.send_message(message.from_user.id, 'Введите отчество собственника.')
    bot.register_next_step_handler(message, add_user_flast_name)


def add_user_flast_name(message):
    user = user_data.Users.get_user(message.from_user.id,
                                    message.from_user.first_name,
                                    message.from_user.last_name,
                                    message.from_user.username)
    user.last_name_ad = message.text

    bot.send_message(message.from_user.id, 'Введите номер квартиры собственника..')
    bot.register_next_step_handler(message, add_number_room)

def add_number_room(message):
    user = user_data.Users.get_user(message.from_user.id,
                                    message.from_user.first_name,
                                    message.from_user.last_name,
                                    message.from_user.username)
    user.room = message.text

    bot.send_message(message.from_user.id, 'Введите номер телефона собственника. формат (999) 999 99 99')
    bot.register_next_step_handler(message, add_telephone)



def add_telephone(message):
    user = user_data.Users.get_user(message.from_user.id,
                                    message.from_user.first_name,
                                    message.from_user.last_name,
                                    message.from_user.username)
    phone = message.text

    with Session(cbd.engin) as session:
        room_id = session.execute(qd.ADD_PHONE.format(f"'{phone}'", f"'{user.user_name_ad}'", f"'{user.room}'", f"'{user.first_name_ad}'", f"'{user.last_name_ad}'",))
        session.commit()
        bot.send_message(message.from_user.id, 'Собственник внесен в базу данных.')


@bot.callback_query_handler(func=lambda call: call.data in ['Удалить'])
def add_user_name(message):
    user = user_data.Users.get_user(message.from_user.id,
                                    message.from_user.first_name,
                                    message.from_user.last_name,
                                    message.from_user.username)

    bot.send_message(message.from_user.id, 'Введите номер квартиры собственника.')
    bot.register_next_step_handler(message.message, delete_user)

def delete_user(message):
    user = user_data.Users.get_user(message.from_user.id,
                                    message.from_user.first_name,
                                    message.from_user.last_name,
                                    message.from_user.username)
    id = message.text


    with Session(cbd.engin) as session:
        session.execute(qd.DELETE_TELEPHONE.format(int(id)))
        session.commit()
        session.execute(qd.DELETE_ACCESSES.format(int(id)))
        session.commit()
        session.execute(qd.DELETE_USER.format(int(id)))
        session.commit()

    bot.send_message(message.from_user.id, 'Собственник удален из базы данных.')


@bot.callback_query_handler(func=lambda call: call.data in ['Смена'])
def add_user_accesses(message):
    user = user_data.Users.get_user(message.from_user.id,
                                    message.from_user.first_name,
                                    message.from_user.last_name,
                                    message.from_user.username)

    bot.send_message(message.from_user.id, 'Введите номер квартиры собственника.')
    bot.register_next_step_handler(message.message, room_user)


def room_user(message):
    user = user_data.Users.get_user(message.from_user.id,
                                    message.from_user.first_name,
                                    message.from_user.last_name,
                                    message.from_user.username)
    user.room = message.text

    bot.send_message(message.from_user.id, 'Введите права собственника user, admin.')
    bot.register_next_step_handler(message, accesses_user)


def accesses_user(message):
    user = user_data.Users.get_user(message.from_user.id,
                                    message.from_user.first_name,
                                    message.from_user.last_name,
                                    message.from_user.username)
    accesses = message.text

    if accesses in ['user', 'admin']:
        with Session(cbd.engin) as session:
            session.execute(qd.UPDATE_USER_ACCESSES.format(int(user.room), f"'{accesses}'"))
            session.commit()
            session.execute(qd.UPDATE_USER_USERS.format(int(user.room), f"'{accesses}'"))
            session.commit()

        bot.send_message(message.from_user.id, f'Собственнику установлены права: {accesses}.')
    else:
        bot.send_message(message.from_user.id, 'Введены несуществующие права.')
        room_user(message)


@bot.callback_query_handler(func=lambda call: call.data in ['Исполнение'])
def add_user_accesses(message):
    user = user_data.Users.get_user(message.from_user.id,
                                    message.from_user.first_name,
                                    message.from_user.last_name,
                                    message.from_user.username)

    bot.send_message(message.from_user.id, 'Введите id исполненного запроса.')
    bot.register_next_step_handler(message.message, out_post)


def out_post(message):
    user = user_data.Users.get_user(message.from_user.id,
                                    message.from_user.first_name,
                                    message.from_user.last_name,
                                    message.from_user.username)
    user.id_archive = message.text

    bot.send_message(message.from_user.id, 'Введите название переданного видео.')
    bot.register_next_step_handler(message, name_video)

def name_video(message):
    user = user_data.Users.get_user(message.from_user.id,
                                    message.from_user.first_name,
                                    message.from_user.last_name,
                                    message.from_user.username)

    name_video = message.text

    with Session(cbd.engin) as session:
        session.execute(qd.FULFILLED.format(int(user.id_archive), f"'{name_video}'", True))
        session.commit()
    bot.send_message(message.from_user.id, f'Заявке #{user.id_archive} присвоен статус "исполнена".')



bot.polling(none_stop=True, interval=0)

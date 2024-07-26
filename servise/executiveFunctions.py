import os
import datetime
from user_data import User


from sqlmodel import Session, select
from database.connection_db import engin
from servise.state import Form
from loggins.logger import logger


from database.scheme_database import Users, Dostup, Video_request, All_owners

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from aiogram_calendar import SimpleCalendar


async def get_calendar(callback, min_date, max_date):
    calendar = SimpleCalendar(locale='ru_RU.utf8', show_alerts=True)
    calendar.set_dates_range(datetime.datetime.strptime(str(min_date), '%Y-%m-%d'),
                             datetime.datetime.strptime(str(max_date), '%Y-%m-%d'))
    return calendar


class Authorization(object):
    def __init__(self, callback=None, message=None, user=None):
        self.callback = callback
        self.message = message
        self.user = user

    async def getting_kratira(self, state):
        try:
            await state.set_state(Form.apartment)
            await self.callback.message.answer("Введите новер вашей квартиры.")
        except Exception as e:
            logger.exception(f"Ошибка {e}")

    async def authorization_user(self):
        try:
            date = datetime.date.today()
            with Session(engin) as session:
                add_useer = Users(apartment_number=int(self.user.apartment),
                                  owner=True,
                                  price=139,
                                  creation_date=date,
                                  nickname_telegram=self.message.from_user.username,
                                  user_id_telega=self.message.from_user.id,
                                  blocking=False,
                                  online_access=False,
                                  user_type='user',
                                  date_issue=True)
                session.add(add_useer)
                session.commit()

            return True
        except Exception as e:
            logger.exception(f"Ошибка {e}")

    async def user_session(self):
        try:
            if self.callback is not None:
                user = User.get_user(self.callback.message.chat.id,
                                      self.callback.message.from_user.first_name,
                                      self.callback.message.from_user.last_name,
                                      self.callback.message.from_user.username)
                return user
            elif self.message is not None:
                user = User.get_user(self.message.chat.id,
                                      self.message.from_user.first_name,
                                      self.message.from_user.last_name,
                                      self.message.from_user.username)
                return user
        except Exception as e:
            logger.exception(f"Ошибка {e}")


class WorcUser(object):

    def __init__(self, callback=None, message=None, user=None):
        self.callback = callback
        self.message = message
        self.user = user

    async def check_user(self):
        try:
            with Session(engin) as session:
                user_data = session.exec(select(Users).where(Users.user_id_telega == self.user.id_chat)).first()
            if user_data is None:
                self.user.rights = "not_registered"
            elif user_data.user_type == "admin":
                self.user.id_user = user_data.id
                self.user.rights = user_data.user_type
            elif user_data.user_type == "user":
                self.user.id_user = user_data.id
                self.user.rights = user_data.user_type
        except Exception as e:
            logger.exception(f"Ошибка {e}")

    async def gaining_access_cameras(self):
        try:
            await self.callback.message.answer('Для получения доступа к системе видеонаблюдения Вам необходимо написать '
                                          'заявление на предоставление доступа и передать его Дмитрию Уранову либо положить в '
                                          '71 почтовый ящик (наилучший выбор). \nОповестить Дмитрия в телеграмм.\n\n'
                                          'При наличии email адреса укажите в его в заявлении.')
            photo_path = os.path.join('wind.jpg')
            await self.callback.message.answer_photo(photo=types.FSInputFile(photo_path))
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text='Перейти в чат',
                                         url='https://t.me/DoK2412')
                ]
            ])
            await self.callback.message.answer('Дмитрий Уранов.', reply_markup=keyboard)
        except Exception as e:
            logger.exception(f"Ошибка {e}")

    async def check_access_cameras(self):
        try:
            with Session(engin) as session:
                user_data = session.exec(select(Users).where(Users.user_id_telega == self.user.id_chat)).first()
                auth_data = session.exec(select(Dostup).where(Dostup.room == user_data.apartment_number)).first()

                if auth_data.access_transfer:

                    await self.callback.message.answer(f"1. Доступ с компьютера (Windows):\n"
                                                       f"В браузере (например хром) открыть: {auth_data.ip_address}\n"
                                                       f"Ввести:\n"
                                                       f" Имя пользователя: {auth_data.login};\n"
                                                       f" Пароль: {auth_data.password};\n"
                                                       f"без ; !!\n"
                                                       f"Нажать 'Вход'.\n")
                    photo_wind_ath = os.path.join('img.png')
                    await self.callback.message.answer_photo(photo=types.FSInputFile(photo_wind_ath))

                    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                        [
                            InlineKeyboardButton(text='Google Play',
                                                 url='https://play.google.com/store/apps/details?id=com.axxonsoft.an3'),
                            InlineKeyboardButton(text='App Store',
                                                 url='https://play.google.com/store/apps/details?id=com.axxonsoft.an3')
                        ]
                    ])
                    await self.callback.message.answer('\n\n2. Доступ со сматфона:\n\n'
                                                       'Скачать приложение AxxonNet c:', reply_markup=keyboard)

                    await self.callback.message.answer(f"Создать Прямое подключение:\n"
                                                       f"  Адрес сервера: {auth_data.ip_address};\n"
                                                       f"  Имя пользователя: {auth_data.login};\n"
                                                       f"  Пароль: {auth_data.password};\n"
                                                       f"  Название: любое, например номер квартиры;\n"
                                                       f"  нажать 'Вход'\n")

                    photo_instruct_path = os.path.join('instructions.png')
                    await self.callback.message.answer_photo(photo=types.FSInputFile(photo_instruct_path))


                    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                        [
                            InlineKeyboardButton(text='Дмитрию Уранову',
                                                 url='https://t.me/DoK2412')
                        ]
                    ])
                    await self.callback.message.answer('При возникновении трудностей написать:', reply_markup=keyboard)
                else:
                    await self.callback.message.answer("Доступ к системе видеонаблюдения не предоставлен.")
        except Exception as e:
            logger.exception(f"Ошибка {e}")

    async def reference_information(self):
        try:
            await self.callback.message.answer('Доступ к камерам:\n\n'
                                                '     Доступ собственникам предоставляется к камерам по периметру дома, а так же к камерам внутреннего наблюдения кроме камер в лифтах.\n'
                                                '     Это связано с тем что камеры в лифтах пишут звук, а так же через них возможно просматривать личную информацию жителей на их мобильных устройствах.\n'
                                                '     Из за возможного факта вмешательства в частную жизнь граждан (137 статья УК РФ нарушение неприкосновенности частной жизни) было принято решение эти камеры ограничить.\n\n'
                                                'Записи из архива:\n\n'
                                                '     У каждого собственника есть право запросить видео из архива сообщив необходимую дату и примерное время.\n'
                                                '     Эту процедуру можно провести нескилькими способами:\n\n'
                                                '     1. Написать заявление во Fryazino.net и ожидать их ответа,\n'
                                                '     2. Оставить заявку в чат боте и в свободное от работы время Дмитрий Уранов (@DoK2412) поднимет архив и сделает вырезку из него.\n'
                                                '     3. Срок хранения архива составляет 2 недели (14 дней);\n\n'
                                                'Проверка доступа:\n\n'
                                                '     Проверить получение доступа к онлайн просмотру и получить входные данные вы можете посмотреть в разделе "Проверка доступа".\n')
        except Exception as e:
            logger.exception(f"Ошибка {e}")

    async def record(self, state):
        try:
            await state.set_state(Form.calendar_1)
            min_date = datetime.date.today()
            max_date = "{:%Y-%m-%d}".format(datetime.datetime.strptime('31.12.2030', '%d.%m.%Y'))
            await self.callback.message.answer('Укажите дату: ',
                                               reply_markup=await (
                                                   await get_calendar(self.callback, min_date, max_date)).start_calendar())
        except Exception as e:
            logger.exception(f"Ошибка {e}")

    async def get_day_and_month(self, callback_data, state):
        try:
            min_date = datetime.date.today() - datetime.timedelta(days=14)
            max_date = "{:%Y-%m-%d}".format(datetime.datetime.strptime('31.12.2030', '%d.%m.%Y'))
            calendar = await get_calendar(self.callback, min_date, max_date)
            selected, date = await calendar.process_selection(self.callback, callback_data)
            if selected and date:
                await state.clear()
                await self.callback.message.delete()
                date_list = [date.strftime('%d'), date.strftime('%m'), date.strftime('%Y')]
                self.user.date = f'{date_list[0]}.{date_list[1]}.{date_list[2]}'
                await state.set_state(Form.time)
                await self.callback.message.answer("Укажите примерный диапазон необходимого времени в формате 09:00-12:00.")
        except Exception as e:
            logger.exception(f"Ошибка {e}")

    async def record_db(self):
        try:
            with Session(engin) as session:
                user = session.exec(select(Users).where(Users.id == self.user.id_user)).first()

                add_useer = Video_request(room=user.apartment_number,
                                          request_date=self.user.date,
                                          time_range=self.message.text,
                                          active=True)
                session.add(add_useer)
                session.commit()
            await self.message.answer("Заявка сохранена.")
        except Exception as e:
            logger.exception(f"Ошибка {e}")


class WorcAdmin(object):

    def __init__(self, callback=None, message=None, user=None):
        self.callback = callback
        self.message = message
        self.user = user

    async def getting_kratira(self, state):
        try:
            await state.set_state(Form.informationOwner)
            await self.callback.message.answer("Введите новер необходимой квартиры.")
        except Exception as e:
            logger.exception(f"Ошибка {e}")


    async def get_owner(self, state):
        try:
            await state.clear()
            with Session(engin) as session:
                auth_data = session.exec(select(Dostup).where(Dostup.room == self.message.text)).first()
                if auth_data:
                    user = session.exec(select(Users).where(Users.apartment_number == auth_data.room)).first()
                    if user.blocking:
                        blocking = "Заблокирован"
                    else:
                        blocking = "Не заблокирован"

                    if user.online_access:
                        access = "Доступ предоставлен"
                    else:
                        access = "Доступ не предоставлен"
                    await self.message.answer(f'Номер квартиры: {auth_data.room},\n'
                      f'Фамилия: {auth_data.surname},\n'
                      f'Имя: {auth_data.name},\n'
                      f'Отчество: {auth_data.last_name},\n'
                      f'Тип пользователя: {user.user_type},\n'
                      f'Доступ к онлайну: {access},\n'
                      f'Блокировка: {blocking},\n'
                      f'Номер телефона {auth_data.number},\n'
                      f'Логин: {auth_data.login},\n'
                      f'Пароль: {auth_data.password}.\n')
                else:
                    await self.message.answer("Пользователя не найдено.")
        except Exception as e:
            logger.exception(f"Ошибка {e}")

    async def get_archive(self):
        try:
            with Session(engin) as session:
                videos = session.exec(select(Video_request).where(Video_request.active == True)).all()
                if videos:
                    for video in videos:
                        user = session.exec(select(Dostup).where(Dostup.room == video.room)).first()
                        await self.callback.message.answer(f"Пользователь: {user.surname} {user.name} {user.last_name},\n"
                                                   f"Номер запроса в базе: {video.id},\n"
                                                   f"Номер квартиры: {video.room},\n"
                                                   f"Необходимая дата: {video.request_date},\n"
                                                   f"Необходимое время: {video.time_range}.")
                else:
                    await self.callback.message.answer("Нет запросов в архиве.")
        except Exception as e:
            logger.exception(f"Ошибка {e}")

    async def owners_menu(self):
        try:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Данные собственника",
                                         callback_data="Данные_собственника")
                ],
                [
                    InlineKeyboardButton(text="Добавить собственника",
                                         callback_data="Добавить_собственника")
                ],
                [
                    InlineKeyboardButton(text="Изменить собственника",
                                         callback_data="Изменить_собственника")
                ]
            ])
            await self.callback.message.answer('Выберите действие.', reply_markup=keyboard)
        except Exception as e:
            logger.exception(f"Ошибка {e}")

    async def adding_owner_db(self):
        try:
            data_user = self.message.text.split(" ")
            with Session(engin) as session:
                user = session.exec(select(All_owners).where(All_owners.room == data_user[3])).first()
                if user is None:
                    add_useer = All_owners(l_name=data_user[0],
                                           name=data_user[1],
                                           f_name=data_user[2],
                                           room=int(data_user[3]),
                                           number=data_user[4])
                    session.add(add_useer)
                    session.commit()
                    await self.message.answer("Собственник добавлен в базу.")
                else:
                    await self.message.answer("В данной кварире проживает другой человек.")
        except Exception as e:
            logger.exception(f"Ошибка {e}")

    async def change_owner_in_db(self):
        try:
            data_user = self.message.text.split(" ")

            with Session(engin) as session:
                user = session.exec(select(All_owners).where(All_owners.room == data_user[3])).first()
                if user is None:
                    await self.message.answer("Данной квартиры нет в доме.")
                else:
                    user.l_name = data_user[0]
                    user.name = data_user[1]
                    user.f_name = data_user[2]
                    user.room = int(data_user[3])
                    user.number = data_user[4]
                    session.add(user)
                    session.commit()
                    await self.message.answer("Собственник квартиры изменен.")
        except Exception as e:
            logger.exception(f"Ошибка {e}")

    async def get_owner_in_db(self):
        try:
            with Session(engin) as session:
                user = session.exec(select(All_owners).where(All_owners.room == self.message.text)).first()
                if user is not None:
                    await self.message.answer(f"Фамилия: {user.l_name},\n"
                                                       f"Имя: {user.name},\n"
                                                       f"Отчество: {user.f_name},\n"
                                                       f"Номер квартиры: {user.room},\n"
                                                       f"Номер телефона: {user.number}.")
                else:
                    await self.message.answer("Собственник не найден.")
        except Exception as e:
            logger.exception(f"Ошибка {e}")

    async def actions_owners_menu(self):
        try:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Добавить пользователя",
                                         callback_data="Добавить_пользователя")
                ],
                [
                    InlineKeyboardButton(text="Добавить учетные данные",
                                         callback_data="Добавить_учетные_данные")
                ],
                [
                    InlineKeyboardButton(text="Удалить учетные данные",
                                         callback_data="Удалить_учетные_данные")
                ],
                [
                    InlineKeyboardButton(text="Сменить права доступа",
                                         callback_data="Сменить_права_доступа")
                ],
                [
                    InlineKeyboardButton(text="Закрыть запрос архива",
                                         callback_data="Закрыть_запрос_архива")
                ]
            ])
            await self.callback.message.answer('Выберите действие.', reply_markup=keyboard)
        except Exception as e:
            logger.exception(f"Ошибка {e}")

    async def add_cctv_user_db(self):
        try:
            data_user = self.message.text.split(" ")
            with Session(engin) as session:
                user = session.exec(select(Dostup).where(Dostup.room == data_user[3])).first()
                if user:
                    await self.message.answer("В данной квартире уже есть собственник.")
                else:
                    date = datetime.date.today()
                    add_useer = Dostup(name=data_user[1],
                                       surname=data_user[0],
                                       last_name=data_user[2],
                                       number=data_user[4],
                                       room=int(data_user[3]),
                                       date_access_transfer=date,
                                       ip_address='62.140.252.182:8010')
                    session.add(add_useer)
                    session.commit()
                    await self.message.answer("Собственник квартиры добавлен.")
        except Exception as e:
            logger.exception(f"Ошибка {e}")

    async def credentials_db(self):
        try:
            data_user = self.message.text.split(" ")
            with Session(engin) as session:
                user = session.exec(select(Dostup).where(Dostup.room == data_user[2])).first()
                if user is None:
                    await self.message.answer("Собственник квартиры не найден.")
                else:
                    user.login = data_user[0]
                    user.password = data_user[1]
                    user.access_transfer = True
                    session.add(user)
                    session.commit()
                    await self.message.answer("Учетные данные добалены.")
        except Exception as e:
            logger.exception(f"Ошибка {e}")

    async def del_credentials_db(self):
        try:
            with Session(engin) as session:
                user = session.exec(select(Dostup).where(Dostup.room == int(self.message.text))).one()
                if user is None:
                    await self.message.answer("Собственник квартиры не найден.")
                else:
                    session.delete(user)
                    session.commit()
                    await self.message.answer("Учетная запись удалена.")
        except Exception as e:
            logger.exception(f"Ошибка {e}")

    async def give_rights_user_db(self):
        try:
            data_user = self.message.text.split(" ")
            if data_user[1] in ["admin", "user"]:
                with Session(engin) as session:
                    user = session.exec(select(Users).where(Users.apartment_number == data_user[0])).first()
                    if user is None:
                        await self.message.answer("Собственник квартиры не найден.")
                    else:
                        user.user_type = data_user[1]
                        session.add(user)
                        session.commit()
                        await self.message.answer("Права собственника изменены.")
            else:
                await self.message.answer("Вы указали не верный тип прав повторите попытку.")
        except Exception as e:
            logger.exception(f"Ошибка {e}")

    async def closing_application_user_db(self):
        try:
            with Session(engin) as session:
                user = session.exec(select(Video_request).where(Video_request.id == int(self.message.text))).one()
                if user is None:
                    await self.message.answer("Заявка с таким номером не найдена.")
                else:
                    user.active = False
                    session.add(user)
                    session.commit()
                    await self.message.answer("Заявка закрыта.")
        except Exception as e:
            logger.exception(f"Ошибка {e}")

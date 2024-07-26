import asyncio

from auth import bot_token_test
from servise.executiveFunctions import WorcUser, Authorization, WorcAdmin
from servise.state import Form
from loggins.logger import logger



from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram_calendar import SimpleCalendarCallback


myBot = Dispatcher()

@myBot.message(CommandStart())
async def start_bot_worc(message: types.Message):
    try:
        await message.delete()
        user = await Authorization(message=message).user_session()

        await WorcUser(message=message, user=user).check_user()

        if user.rights == "not_registered":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Авторизация",
                                         callback_data="Авторизация")
                ]
            ])
            await message.answer('Добро пожаловать в меню бота.', reply_markup=keyboard)

        elif user.rights == "admin":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Получение доступа",
                                         callback_data="Получение"),
                    InlineKeyboardButton(text="Проверка доступа",
                                         callback_data="Проверка")
                ],
                [
                    InlineKeyboardButton(text="Справочная информация",
                                         callback_data="Справочная")
                ],
                [
                    InlineKeyboardButton(text="Сведения о собственнике",
                                         callback_data="Собственник"),
                    InlineKeyboardButton(text="Сведения о запросах архива",
                                         callback_data="Архив")
                ],
                [
                    InlineKeyboardButton(text="Добавить в базу",
                                         callback_data="Добавить"),
                    InlineKeyboardButton(text="Собственники",
                                         callback_data="Собственники")
                ],
            ])
            await message.answer('Добро пожаловать в админ меню.', reply_markup=keyboard)
        elif user.rights == "user":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Получение доступа",
                                         callback_data="Получение"),
                    InlineKeyboardButton(text="Проверка доступа",
                                         callback_data="Проверка")
                ],
                [
                    InlineKeyboardButton(text="Справочная информация",
                                         callback_data="Справочная"),
                    InlineKeyboardButton(text="Запрос записи из архива",
                                         callback_data="Запись")
                ]
            ])
            await message.answer('Добро пожаловать в меню бота.', reply_markup=keyboard)
    except Exception as e:
        logger.exception(f"Ошибка в главном меню {e}")
        await message.answer("В хоте выполнения запроса возникла ошибка. Повторите запрос.")


@myBot.callback_query(F.data == "Авторизация")
async def authorization(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
        user = await Authorization(callback=callback).user_session()
        await Authorization(callback=callback).getting_kratira(state)
    except Exception as e:
        logger.exception(f"Ошибка при регистрации {e}")
        await callback.message.answer("В хоте выполнения запроса возникла ошибка. Повторите запрос.")


@myBot.message(Form.apartment)
async def request_apartment(message, state: FSMContext):
    try:
        await state.clear()
        user = await Authorization(message=message).user_session()
        user.apartment = message.text
        end_registration = await Authorization(message=message, user=user).authorization_user()
        if end_registration:
            await start_bot_worc(message=message)
        else:
            await message.answer("Во время авторизации произошла ошибка, повторите попытку.")
    except Exception as e:
        logger.exception(f"Ошибка при вводе квартиры в регистрации {e}")
        await message.answer("В хоте выполнения запроса возникла ошибка. Повторите запрос.")


@myBot.callback_query(F.data == "Получение")
async def gaining_access(callback: types.CallbackQuery):
    try:
        await callback.message.delete()
        user = await Authorization(callback=callback).user_session()
        await WorcUser(callback=callback, user=user).gaining_access_cameras()
    except Exception as e:
        logger.exception(f"Ошибка при запросе получения доступа {e}")
        await callback.message.answer("В хоте выполнения запроса возникла ошибка. Повторите запрос.")


@myBot.callback_query(F.data == "Проверка")
async def check_access(callback: types.CallbackQuery):
    try:
        await callback.message.delete()
        user = await Authorization(callback=callback).user_session()
        await WorcUser(callback=callback, user=user).check_access_cameras()
    except Exception as e:
        logger.exception(f"Ошибка при проверке доступа {e}")
        await callback.message.answer("В хоте выполнения запроса возникла ошибка. Повторите запрос.")


@myBot.callback_query(F.data == "Справочная")
async def check_access(callback: types.CallbackQuery):
    try:
        await callback.message.delete()
        user = await Authorization(callback=callback).user_session()
        await WorcUser(callback=callback, user=user).reference_information()
    except Exception as e:
        logger.exception(f"Ошибка при получении справочной информации {e}")
        await callback.message.answer("В хоте выполнения запроса возникла ошибка. Повторите запрос.")


@myBot.callback_query(F.data == "Запись")
async def get_record(callback: types.CallbackQuery,  state: FSMContext):
    try:
        await callback.message.delete()
        user = await Authorization(callback=callback).user_session()
        await WorcUser(callback=callback, user=user).record(state)
    except Exception as e:
        logger.exception(f"Ошибка при записи в архив {e}")
        await callback.message.answer("В хоте выполнения запроса возникла ошибка. Повторите запрос.")


@myBot.callback_query(Form.calendar_1, SimpleCalendarCallback.filter())
async def process_simple_calendar(callback, callback_data, state: FSMContext):
    try:
        user = await Authorization(callback=callback).user_session()
        await WorcUser(callback=callback, user=user).get_day_and_month(callback_data, state)
    except Exception as e:
        logger.exception(f"Ошибка при вводе необходимого дня {e}")
        await callback.message.answer("В хоте выполнения запроса возникла ошибка. Повторите запрос.")


@myBot.message(Form.time)
async def request_record_db(message, state: FSMContext):
    try:
        await state.clear()
        await message.delete()
        user = await Authorization(message=message).user_session()
        await WorcUser(message=message, user=user).record_db()
    except Exception as e:
        logger.exception(f"Ошибка при вводе времени для получения записи из архива {e}")
        await message.answer("В хоте выполнения запроса возникла ошибка. Повторите запрос.")


@myBot.callback_query(F.data == "Собственник")
async def information_owner(callback: types.CallbackQuery, state: FSMContext):
    try:
        user = await Authorization(callback=callback).user_session()
        await WorcAdmin(callback=callback, user=user).getting_kratira(state)
    except Exception as e:
        logger.exception(f"Ошибка при получении информации о собственнике{e}")
        await callback.message.answer("В хоте выполнения запроса возникла ошибка. Повторите запрос.")


@myBot.message(Form.informationOwner)
async def information_owner_room(message, state: FSMContext):
    try:
        user = await Authorization(message=message).user_session()
        await WorcAdmin(message=message, user=user).get_owner(state)
    except Exception as e:
        logger.exception(f"Ошибка при вводе квартиры собственника {e}")
        await message.answer("В хоте выполнения запроса возникла ошибка. Повторите запрос.")


@myBot.callback_query(F.data == "Архив")
async def request_archive(callback: types.CallbackQuery):
    try:
        user = await Authorization(callback=callback).user_session()
        await WorcAdmin(callback=callback, user=user).get_archive()
    except Exception as e:
        logger.exception(f"Ошибка при получении списка запрошенных записей из архива {e}")
        await callback.message.answer("В хоте выполнения запроса возникла ошибка. Повторите запрос.")


@myBot.callback_query(F.data == "Собственники")
async def owners(callback: types.CallbackQuery):
    try:
        await callback.message.delete()
        user = await Authorization(callback=callback).user_session()
        await WorcAdmin(callback=callback, user=user).owners_menu()
    except Exception as e:
        logger.exception(f"Ошибка при получении меню собственников {e}")
        await callback.message.answer("В хоте выполнения запроса возникла ошибка. Повторите запрос.")


@myBot.callback_query(F.data == "Добавить_собственника")
async def owner_details(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
        user = await Authorization(callback=callback).user_session()
        await state.set_state(Form.fullName)
        await callback.message.answer("Введите через пробел Фамилию Имя Отчество, номер квартиры и номер телефона.")
    except Exception as e:
        logger.exception(f"Ошибка при запросе сведений собственника  для записи в базу {e}")
        await callback.message.answer("В хоте выполнения запроса возникла ошибка. Повторите запрос.")


@myBot.message(Form.fullName)
async def adding_owner(message, state: FSMContext):
    try:
        await state.clear()
        user = await Authorization(message=message).user_session()
        await WorcAdmin(message=message).adding_owner_db()
    except Exception as e:
        logger.exception(f"Ошибка при получении данных о собственнике при записи в базе {e}")
        await message.answer("В хоте выполнения запроса возникла ошибка. Повторите запрос.")


@myBot.callback_query(F.data == "Изменить_собственника")
async def change_owner(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
        user = await Authorization(callback=callback).user_session()
        await state.set_state(Form.changeOwner)
        await callback.message.answer("Введите через пробел Фамилию Имя Отчество, номер квартиры и номер телефона.")
    except Exception as e:
        logger.exception(f"Ошибка при запросе данных о собственнике для изменения в базе {e}")
        await callback.message.answer("В хоте выполнения запроса возникла ошибка. Повторите запрос.")


@myBot.message(Form.changeOwner)
async def change_owner_db(message, state: FSMContext):
    try:
        await state.clear()
        user = await Authorization(message=message).user_session()
        await WorcAdmin(message=message).change_owner_in_db()
    except Exception as e:
        logger.exception(f"Ошибка при получении данных о собственнике для измения в базе {e}")
        await message.answer("В хоте выполнения запроса возникла ошибка. Повторите запрос.")


@myBot.callback_query(F.data == "Данные_собственника")
async def change_owner(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
        user = await Authorization(callback=callback).user_session()
        await state.set_state(Form.getOwner)
        await callback.message.answer("Введите номер необходимой квартиры.")
    except Exception as e:
        logger.exception(f"Ошибка при вводе квартиры для получения сведений о собственнике {e}")
        await callback.message.answer("В хоте выполнения запроса возникла ошибка. Повторите запрос.")


@myBot.message(Form.getOwner)
async def change_owner_db(message, state: FSMContext):
    try:
        await state.clear()
        user = await Authorization(message=message).user_session()
        await WorcAdmin(message=message).get_owner_in_db()
    except Exception as e:
        logger.exception(f"Ошибка при выводе данных о собственнике {e}")
        await message.answer("В хоте выполнения запроса возникла ошибка. Повторите запрос.")


@myBot.callback_query(F.data == "Добавить")
async def actions_owners(callback: types.CallbackQuery):
    try:
        await callback.message.delete()
        user = await Authorization(callback=callback).user_session()
        await WorcAdmin(callback=callback, user=user).actions_owners_menu()
    except Exception as e:
        logger.exception(f"Ошибка при получении меню работы с учетными записями пользователей в видеонаблюдении {e}")
        await callback.message.answer("В хоте выполнения запроса возникла ошибка. Повторите запрос.")


@myBot.callback_query(F.data == "Добавить_пользователя")
async def cctv_user (callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
        user = await Authorization(callback=callback).user_session()
        await state.set_state(Form.cctvUser)
        await callback.message.answer("Введите через пробел Фамилию Имя Отчество, номер квартиры и номер телефона.")
    except Exception as e:
        logger.exception(f"Ошибка при получении сведений для добавлении учетной записи видеонаблюдения в базу {e}")
        await callback.message.answer("В хоте выполнения запроса возникла ошибка. Повторите запрос.")


@myBot.message(Form.cctvUser)
async def add_cctv_user(message, state: FSMContext):
    try:
        await message.delete()
        await state.clear()
        user = await Authorization(message=message).user_session()
        await WorcAdmin(message=message).add_cctv_user_db()
    except Exception as e:
        logger.exception(f"Ошибка при добавлении учетной записи видеонаблюдения в базе {e}")
        await message.answer("В хоте выполнения запроса возникла ошибка. Повторите запрос.")


@myBot.callback_query(F.data == "Добавить_учетные_данные")
async def credentials(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
        user = await Authorization(callback=callback).user_session()
        await state.set_state(Form.credentials)
        await callback.message.answer("Введите через пробел логин пароль и номер квартиры.")
    except Exception as e:
        logger.exception(f"Ошибка при запросе логина и пароля учетной записи для добавления в базу {e}")
        await callback.message.answer("В хоте выполнения запроса возникла ошибка. Повторите запрос.")


@myBot.message(Form.credentials)
async def add_credentials(message, state: FSMContext):
    try:
        await message.delete()
        await state.clear()
        user = await Authorization(message=message).user_session()
        await WorcAdmin(message=message).credentials_db()
    except Exception as e:
        logger.exception(f"Ошибка при добавлении учетных данных в базу {e}")
        await message.answer("В хоте выполнения запроса возникла ошибка. Повторите запрос.")


@myBot.callback_query(F.data == "Удалить_учетные_данные")
async def delete_credentials(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
        user = await Authorization(callback=callback).user_session()
        await state.set_state(Form.deleteCredentials)
        await callback.message.answer("Введите номер квартиры для удаления учетных данных.")
    except Exception as e:
        logger.exception(f"Ошибка при запросе квартиры собственника для удаления учетной записи видеонаблюдения из базы {e}")
        await callback.message.answer("В хоте выполнения запроса возникла ошибка. Повторите запрос.")


@myBot.message(Form.deleteCredentials)
async def del_credentials(message, state: FSMContext):
    try:
        await message.delete()
        await state.clear()
        user = await Authorization(message=message).user_session()
        await WorcAdmin(message=message).del_credentials_db()
    except Exception as e:
        logger.exception(f"Ошибка при удалении учетной записи видеонаблюдения из базы {e}")
        await message.answer("В хоте выполнения запроса возникла ошибка. Повторите запрос.")


@myBot.callback_query(F.data == "Сменить_права_доступа")
async def give_rights(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
        user = await Authorization(callback=callback).user_session()
        await state.set_state(Form.giveRights)
        await callback.message.answer("Введите номер квартиры и тип прав (admin/user).")
    except Exception as e:
        logger.exception(f"Ошибка при запросе новых прав для собственника {e}")
        await callback.message.answer("В хоте выполнения запроса возникла ошибка. Повторите запрос.")


@myBot.message(Form.giveRights)
async def give_rights_user(message, state: FSMContext):
    try:
        await message.delete()
        await state.clear()
        user = await Authorization(message=message).user_session()
        await WorcAdmin(message=message).give_rights_user_db()
    except Exception as e:
        logger.exception(f"Ошибка при смене прав собственника {e}")
        await message.answer("В хоте выполнения запроса возникла ошибка. Повторите запрос.")


@myBot.callback_query(F.data == "Закрыть_запрос_архива")
async def closing_application(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
        user = await Authorization(callback=callback).user_session()
        await state.set_state(Form.closingApplication)
        await WorcAdmin(callback=callback, user=user).get_archive()
        await callback.message.answer("Введите номер заявки необходимую закрыть.")
    except Exception as e:
        logger.exception(f"Ошибка при получении id заявки архивной записи для закрытия{e}")
        await callback.message.answer("В хоте выполнения запроса возникла ошибка. Повторите запрос.")


@myBot.message(Form.closingApplication)
async def closing_application_user(message, state: FSMContext):
    try:
        await message.delete()
        await state.clear()
        user = await Authorization(message=message).user_session()
        await WorcAdmin(message=message).closing_application_user_db()
    except Exception as e:
        logger.exception(f"Ошибка при закрытии заявки на архивную запись {e}")
        await message.answer("В хоте выполнения запроса возникла ошибка. Повторите запрос.")


async def main():
    try:
        bot = Bot(token=bot_token_test, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        await myBot.start_polling(bot)
    except Exception as e:
        logger.exception(f"Ошибка при формировании запуска бота {e}")


if __name__ == '__main__':
    asyncio.run(main())

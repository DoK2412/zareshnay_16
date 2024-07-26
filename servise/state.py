from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    calendar_1 = State()            # кадендарь записи из архива
    time = State()                  # получение времени запроса архива
    apartment = State()             # получение номера квартиры для регистрации
    informationOwner = State()      # получение польного списка сведений о пользователе
    fullName = State()              # добавить собственника в общий список жильцов
    changeOwner = State()           # изменить данные собственника в базе
    getOwner = State()              # полученить данные о собственнике квартиры
    cctvUser = State()              # добавить пользователя в список видеонаблюдения
    credentials = State()           # Ввести учетные данные пользователя
    deleteCredentials = State()     # Удаление учетных данных
    giveRights = State()            # Сменить права пользователю
    closingApplication = State()    # Закрытие заявки видео орхива

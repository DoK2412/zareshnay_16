ENTRY_DATABASE = '''
-- добавление новой записи на запрос архива
INSERT INTO video_request (id_user, request_date,  time_range, reply_date) VALUES ({0}, {1}, {2}, False);
'''

NEW_USER = '''
-- добавление нового пользователя
INSERT INTO users (apartment_number, owner, price, creation_date, nickname_telegram, user_id_telega, blocking, online_access, user_type) VALUES ({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8});
'''

OUTPUT_ALL = '''
-- вывод всех дел
SELECT id, masseg, data FROM user_notes WHERE id_user = {0} and activ = True
'''

ID_USER_DB = '''
-- получение id пользователя в базе данных
SELECT id, apartment_number, user_type FROM users WHERE user_id_telega = {0} and owner = True
'''

ID_ROOM_DB = '''
-- получение id пользователя в базе данных
SELECT id FROM users WHERE apartment_number = {0}
'''

USER_ACCESS_DB = '''
-- получение id пользователя в базе данных
SELECT date_issue 
FROM users 
INNER JOIN accesses a ON users.apartment_number = a.number_room
WHERE user_id_telega = {0} and owner = True
'''


USER_DATA = '''
--запрос данных о собственнике
SELECT t.number_room as "room", 
    a.date_issue as "onlain",
    u.blocking as "blocking",
    a.user_type as "user_type",
    t.surname_start as "surname",
    t.surname_end as "surname_end",
    t.name as "name",
    t.number as "number",
    a.login_user as "login",
    a.password_user as "password"
FROM  telephon t
LEFT JOIN users u ON t.number_room = u.apartment_number
LEFT JOIN accesses a ON t.number_room = a.number_room
WHERE t.number_room = {0}
'''

USER_ARCHIVE = '''
-- получение запросов архива
SELECT vr.request_date as "date",
    vr.time_range as "time",
    t.surname_start as "surname",
    t.surname_end as "surname_end",
    t.name as "name",
    u.apartment_number as "room",
    vr.id as "id_video"
FROM video_request vr
LEFT JOIN users u ON vr.id_user = u.id
LEFT JOIN telephon t ON u.apartment_number = t.number_room
WHERE vr.reply_date = FALSE
'''


ADD_INPUT_DATA = '''
--добавить новые входные данные пользователя
INSERT INTO accesses (number_room, ip_address, login_user, password_user, date_receiving, user_type) VALUES ({0}, {1}, {2}, {3}, {4}, {5})
'''

UPDATE_USER = '''
--подтверждение переадчи данных собственнику
UPDATE accesses SET date_issue = {1} WHERE number_room = {0}
'''

ADD_PHONE = '''
--добавить новые входные данные пользователя
INSERT INTO telephon (number, name, number_room, surname_start, surname_end) VALUES ({0}, {1}, {2}, {3}, {4})
'''

DELETE_TELEPHONE = '''
--удаление из таблици телефонов
DELETE FROM telephon
WHERE number_room={0};
'''

DELETE_ACCESSES = '''
--удаление из таблици доступов
DELETE FROM accesses
WHERE number_room={0};
'''

DELETE_USER = '''
--удаление из таблици доступов
DELETE FROM users
WHERE apartment_number={0};
'''

UPDATE_USER_ACCESSES  = '''
--подтверждение переадчи данных собственнику
UPDATE accesses SET user_type = {1} WHERE number_room = {0}
'''

UPDATE_USER_USERS = '''
--подтверждение переадчи данных собственнику
UPDATE users SET user_type = {1} WHERE apartment_number = {0}
'''


FULFILLED = '''
-- запрос закрытия архивной заявки
UPDATE video_request SET reply_date = {2}, name_video = {1} WHERE id = {0}
'''
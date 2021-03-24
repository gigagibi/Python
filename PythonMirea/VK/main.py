import vk_api
import json
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import psycopg2
import random


# класс пользователя, содержит id пользователя и его режим меню
class User:
    def __init__(self, id, mode):
        self.id = id
        self.mode = mode


# подключение к БД
con = psycopg2.connect(
    database='memes',
    user='postgres',
    password='admin',
    host='127.0.0.1',
    port=5432
)
cur = con.cursor()

# авторизация вк
my_token = '48ffce920468e8a766fd2baae4af76619a80c8f72416c7360e2a0254169bdb86872f6a00369c6fa0d8c8c'
vk_session = vk_api.VkApi(token=my_token)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

# добавление клавиатуры для выбора мема
keyboard = VkKeyboard(one_time=False)
keyboard.add_button(label="Кринж", color=VkKeyboardColor.POSITIVE)
keyboard.add_button(label="Floppa", color=VkKeyboardColor.POSITIVE)
keyboard.add_button(label="Клоун", color=VkKeyboardColor.POSITIVE)
keyboard.add_button(label="Who tf asked", color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button(label="Pepe", color=VkKeyboardColor.POSITIVE)
keyboard.add_button(label="толстяк с пистолетом", color=VkKeyboardColor.POSITIVE)
#keyboard.add_line()
keyboard.add_button(label="Создать мем", color=VkKeyboardColor.POSITIVE)
# клавиатура для выбора рандома или списка мемов
end_keyboard = VkKeyboard(one_time=False)
end_keyboard.add_button(label='Рандомный мем', color=VkKeyboardColor.POSITIVE)
end_keyboard.add_button(label='Список мемов', color=VkKeyboardColor.POSITIVE)
end_keyboard.add_button(label='Назад', color=VkKeyboardColor.NEGATIVE)
# кнопка для окончания добавления тегов
tags_end_keyboard = VkKeyboard(one_time=False)
tags_end_keyboard.add_button(label="СТОП", color=VkKeyboardColor.NEGATIVE)
tags_end_keyboard.add_button(label='Назад', color=VkKeyboardColor.NEGATIVE)
# клавиатура с кнопкой назад
goback_keyboard = VkKeyboard(one_time=False)
goback_keyboard.add_button(label='Назад', color=VkKeyboardColor.NEGATIVE)

# клавиатура с мемами пользо)вателя
# users_keyboard = VkKeyboard(one_time=False)
# keyboard.add_button(


# добавляет пользователя в базу данных
def add_user_into_DB(user):
    cur.execute(
        'insert into users values(%s, %s)',
        (user.id, user.mode)
    )
    con.commit()


# возвращает список пользователей из базы данных
def get_users_from_DB():
    us_obj = []
    cur.execute(
        "select * from users",
    )
    us_str = cur.fetchall()
    con.commit()
    for string in us_str:
        us_obj.append(User(int(string[0]), string[1]))
    return us_obj


# обновляет параметры пользователя в БД
def update_user(id, mode):
    cur.execute(
        "update users set mode = %s where user_id=%s",
        (mode, id)
    )
    con.commit()


# возвращает список мемов
def search_meme_in_DB(name):
    cur.execute(
        "select link from links where name like %s or name like LOWER(%s) or array_to_string(tags, ' ') like LOWER(%s) or array_to_string(tags, ' ') like %s",
        ('%' + name + '%', '%' + name + '%', '%' + name + '%', '%' + name + '%')
    )
    con.commit()
    memes = cur.fetchall()
    return ['Ничего не найдено'] if len(memes) == 0 else memes


# возвращает случайный мем из списка
def return_random_meme(name):
    catalog = search_meme_in_DB(name)
    rand_num = random.randint(0, len(catalog) - 1)
    return catalog[rand_num]


# отправляет сообщение
def send_message(id, text, keyb):
    if (keyb is not None):
        vk_session.method('messages.send',
                          {"user_id": id, "message": text, "random_id": 0, "keyboard": keyb.get_keyboard()})
    else:
        vk_session.method('messages.send', {"user_id": id, "message": text, "random_id": 0})


def add_meme(name, link, tags):
    cur.execute(
        'insert into links(name, link, tags) values(%s, %s, %s)',
        (name, link, str(tags).replace('[', '{').replace(']', '}'))
    )
    con.commit()


# главный цикл
users = get_users_from_DB()
memes_list = []
add_name, add_link, add_tags = '', '', []
for event in longpoll.listen():
    users = get_users_from_DB()
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            msg = event.text.lower()
            id = event.user_id
            if msg == 'начать':
                flag = 0
                for user in users:
                    if id == user.id:
                        user.mode = 'start'
                        update_user(user.id, user.mode)
                        send_message(id, 'Введи слово, связанное с мемом, или нажми на кнопку', keyboard)
                        flag = 1
                if flag == 0:
                    add_user_into_DB(User(id, 'start'))
                    users = get_users_from_DB()
                    send_message(id, 'Введи слово, связанное с мемом, или нажми на кнопку', keyboard)
            for user in users:

                if user.id == id:
                    if user.mode == 'start' and msg != 'начать' and msg != 'создать мем':
                        memes_list = search_meme_in_DB(msg)
                        user.mode = 'end'
                        update_user(id, user.mode)
                        send_message(id, 'Прислать один рандомный найденный мем или список найденных мемов?',
                                     end_keyboard)
                    elif user.mode == 'start' and msg == 'создать мем' and msg != 'начать' and msg!='назад':
                        user.mode = 'add_name'

                        update_user(id, user.mode)
                        send_message(id, 'Введи имя для мема', goback_keyboard)
                    elif user.mode == 'add_name' and msg != 'начать' and msg != 'назад':
                        user.mode = 'add_link'
                        update_user(id, user.mode)
                        add_name = msg
                        send_messmage(id, 'Введи вк-ссылку на мем(фото, видео или гиф)', goback_keyboard)
                    elif user.mode == 'add_link' and msg != 'начать' and msg != 'назад':
                        user.mode = 'add_tags'
                        add_link = msg
                        update_user(id, user.mode)
                        send_message(id, 'Введи тэг, затем отправь его. Когда надоест, нажми на кнопку СТОП', tags_end_keyboard)
                    elif user.mode == 'add_tags' and msg != 'стоп' and msg != 'начать' and msg != 'назад':
                        add_tags.append(msg)
                        send_message(id, 'Введи тэг, затем отправь его. Когда надоест, нажми на кнопку СТОП',
                                     tags_end_keyboard)
                    elif user.mode == 'add_tags' and msg == 'стоп' and msg != 'начать' and msg != 'назад':
                        user.mode = 'start'
                        update_user(id, user.mode)
                        add_meme(add_name, add_link, add_tags)
                        send_message(id, 'Твой мем добавлен в общую базу. Спасибо за вклад, чумба!', None)
                        send_message(id, 'Введи слово, связанное с мемом, или нажми на кнопку', keyboard)
                    elif user.mode == 'end':
                        if msg == 'рандомный мем':
                            send_message(id, memes_list[random.randint(0, len(memes_list) - 1)], keyboard)
                            user.mode = 'start'
                            update_user(id, user.mode)
                        elif msg == 'список мемов':
                            for meme in memes_list:
                                send_message(id, meme, keyboard)
                            user.mode = 'start'
                            update_user(id, user.mode)
                        elif msg == 'назад':
                            user.mode = 'start'
                            update_user(id, user.mode)
                            send_message(id, 'Введи слово, связанное с мемом, или нажми на кнопку', keyboard)
# l = []
# l.append('a')
# l.append('b')
# l.append('n')
# print(str(l).replace('[', '{').replace(']', '}'))

import vk_api
import json
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import psycopg2
import random

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

# добавление клавиатуры
keyboard = VkKeyboard(one_time=False)
keyboard.add_button(label="Кринж", color=VkKeyboardColor.POSITIVE)
keyboard.add_button(label="Floppa", color=VkKeyboardColor.POSITIVE)
keyboard.add_button(label="Клоун", color=VkKeyboardColor.POSITIVE)
keyboard.add_button(label="Who tf asked", color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button(label="Pepe", color=VkKeyboardColor.POSITIVE)
keyboard.add_button(label="толстяк с пистолетом", color=VkKeyboardColor.POSITIVE)
keyboard.add_button(label='Назад', color=VkKeyboardColor.NEGATIVE)

end_keyboard = VkKeyboard(one_time=False)
end_keyboard.add_button(label='Рандомный мем', color=VkKeyboardColor.POSITIVE)
end_keyboard.add_button(label='Список мемов', color=VkKeyboardColor.POSITIVE)
end_keyboard.add_button(label='Назад', color=VkKeyboardColor.NEGATIVE)


# возвращает список мемов
def search_meme_in_DB(name):
    cur.execute(
        "select link from links where name like %s or name like LOWER(%s) or LOWER(%s)=ANY(tags) or %s=ANY(tags)",
        (name, name, name, name)
    )
    con.commit()
    str = cur.fetchall()
    return 'Ничего не найдено' if str is None else str


# возвращает случайный мем из списка
def return_random_meme(name):
    catalog = search_meme_in_DB(name)
    rand_num = random.randint(0, len(catalog) - 1)
    return catalog[rand_num]


def send_message(id, text, keyb):
    vk_session.method('messages.send',
                      {"user_id": id, "message": text, "random_id": 0, "keyboard": keyb.get_keyboard()})


def main(ev):
    if ev.type == VkEventType.MESSAGE_NEW:
        if ev.to_me:
            send_message(ev.user_id, 'Введите ключевое слово, связанное с мемом, или нажмите кнопку', keyboard)
            meme_name = ev.text
            if ev.type == VkEventType.MESSAGE_NEW:
                send_message(ev.user_id, 'Вам прислать список найденных мемов или один рандомный найденный?',
                             end_keyboard)
                if ev.text == 'Рандомный мем' or ev.text == 'рандомный мем':
                    send_message(return_random_meme(meme_name))
                elif ev.text == 'Список мемов' or ev.text == 'cписок мемов':
                    meme_list = search_meme_in_DB(ev.text)
                    meme_str = ''
                    for meme in meme_list:
                        meme_str = meme + '\n'


for event in longpoll.listen():
    main(event)

# print(search_meme_in_DB('Китай'))

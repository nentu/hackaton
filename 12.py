# -*- coding: utf8 -*-
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id

try:
    from urllib import urlopen
    import sys

    reload(sys)
    sys.setdefaultencoding('utf-8')
except Exception:
    from urllib.request import urlopen
import threading, time
import requests, json, datetime
import pandas as pd
import numpy as np

print('ready')
if 0:
    print('cleared')
    user_balance_data = pd.DataFrame({'balance': [], 'reg_date': [], 'promo_code': []}, index=[])
    user_balance_data.index.name = 'vk_index'
else:
    try:
        user_balance_data = pd.read_csv('filename.csv', sep=',')
        indexs = user_balance_data['Unnamed: 0'].tolist()
        del user_balance_data['Unnamed: 0']
        user_balance_data.index = indexs
    except Exception:
        user_balance_data = pd.DataFrame({'balance': [], 'reg_date': [], 'promo_code': []}, index=[])
        user_balance_data.index.name = 'vk_index'
        user_balance_data.to_csv('filename.csv')
print(user_balance_data.index.values.tolist())


def create_empty_keyboard():
    keyboardd = VkKeyboard.get_empty_keyboard()
    return keyboardd
    # Эта функция используется для закрытия клавиатуры


def courses(event):
    global list_of_users
    msg_send(event.object.peer_id,
             'Список кружков: (сортировка в алфавитном порядке)\n'
             '(название кружка), (ссылка на группу), (Имя и фамилия преподавателя), (ссылка на его стр в вк), (Твоя средняя оценка)/(Средняя оценка по группе)', coutses_keyboard())

def achievement(event):
    global list_of_users
    msg_send(event.object.peer_id,
             'Здесь можно добавить новое достижение, которое будет отправлено на подтверждение тренеру, или посмотреть имеющиеся', achievement_keyboard())
def new_achievement(event):
    global list_of_users
    msg_send(event.object.peer_id,
             'Выберите количество баллов за это достижение', new_achievement_keyboard())
def new_achievement_2(event):
    global list_of_users
    msg_send(event.object.peer_id,
             'Опишите, за что вы получили это достижение и прикрепите фото или видео, если они нужны')

def course_search(event):
    global list_of_users
    msg_send(event.object.peer_id,
             'Выберите подходящий для вас вариант поиска', search_keyboard())

def course_search_by_geopos(event):
    def list_new_courses():
        keyboard = VkKeyboard(one_time=False)
        for i in range(9):
            keyboard.add_button("Кружок номер " + str(i+1), color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
        keyboard.add_button("Назад", color=VkKeyboardColor.DEFAULT)
        return keyboard.get_keyboard()


    msg_send(event.object.peer_id,
             'Появится изображение карты с ближайшими кружками в радиусе 1 км, где каждый имеет свои индекс для выбора',list_new_courses())

def course_search_by_text(event):
    def list_new_courses():
        keyboard = VkKeyboard(one_time=False)
        for i in range(9):
            keyboard.add_button("Кружок номер " + str(i+1), color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
        keyboard.add_button("Назад", color=VkKeyboardColor.DEFAULT)
        return keyboard.get_keyboard()
    msg_send(event.object.peer_id,
             'Список кружков в городе пользователя (с индексами для поиска).\n'
             'В дальнейшем планируется сделать сортировку кружков по рейтенгу, подходящих под пол и возраст ребенка,',None)

vkSession = VkApi(token='724ac9ca603d6d82f66f9716a19b06fb26108aad5d533deaefd375b7dd38853c3471bce39905f155bad0f')
longPoll = VkBotLongPoll(vkSession, 204037695 )
vk = vkSession.get_api()



def coutses_keyboard():
    keyboard = VkKeyboard(one_time=False)
    # False Если клавиатура должна оставаться откртой после нажатия на кнопку
    # True если она должна закрваться

    keyboard.add_button("Найти новый кружок", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("Нaзад", color=VkKeyboardColor.DEFAULT)
    return keyboard.get_keyboard()

def achievement_keyboard():
    keyboard = VkKeyboard(one_time=False)
    # False Если клавиатура должна оставаться откртой после нажатия на кнопку
    # True если она должна закрваться

    keyboard.add_button("Добавить новое", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("Посмотреть имеющиеся", color=VkKeyboardColor.DEFAULT)
    return keyboard.get_keyboard()

def new_achievement_keyboard():
    keyboard = VkKeyboard(one_time=False)
    # False Если клавиатура должна оставаться откртой после нажатия на кнопку
    # True если она должна закрваться
    for i in range(2, 5):
        keyboard.add_button(str(i)+" балла", color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    for i in range(5, 8):
        keyboard.add_button(str(i)+" баллов", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    for i in range(8, 11):
        keyboard.add_button(str(i)+" баллов", color=VkKeyboardColor.POSITIVE)
    return keyboard.get_keyboard()

def main_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button("Мои Кружки", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("Мои достижения", color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button("Расписание", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("Рейтинг", color=VkKeyboardColor.POSITIVE)
    return keyboard.get_keyboard()

def search_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button("По геопозиции", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("По имени в моем городе", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("Вернуться в главное меню", color=VkKeyboardColor.DEFAULT)

    return keyboard.get_keyboard()


def msg_send(user_id, text, keyboard=main_keyboard()):
    max_len = 4092
    try:
        if text != '':
            kols = len(text) // max_len
            vk.messages.send(peer_id=user_id,
                             message=text[0:max_len],
                             random_id=get_random_id(),
                             keyboard=keyboard)
            for i in range(kols):
                vk.messages.send(peer_id=user_id,
                                 message=text[max_len * i:max_len * (i + 1)],
                                 random_id=get_random_id())
    except Exception:
        pass

main_list = dict()

print('start')
while True:

    if 1:
        for event in longPoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if not event.object.peer_id in main_list.keys():
                    main_list[event.object.peer_id] = {'achiv points':None}
                if 'привет' in event.object['text'].lower() or event.object['text'].lower() == 'начать' or event.object['text'].lower() == 'Вернуться в главное меню'.lower():
                    msg_send(event.object.peer_id, 'Хорошо!', main_keyboard())
                elif event.object['text'].lower() == 'мои кружки':
                    threading.Thread(target=courses, args=[event]).start()
                elif event.object['text'].lower() == 'Найти новый кружок'.lower():
                    threading.Thread(target=course_search, args=[event]).start()
                elif event.object['text'].lower() == 'По геопозиции'.lower():
                    threading.Thread(target=course_search_by_geopos, args=[event]).start()
                elif event.object['text'].lower() == 'По имени в моем городе'.lower():
                    threading.Thread(target=course_search_by_text, args=[event]).start()
                elif event.object['text'].lower() == 'Мои достижения'.lower():
                    threading.Thread(target=achievement, args=[event]).start()
                elif event.object['text'].lower() == 'Добавить новое'.lower():
                    threading.Thread(target=new_achievement_2, args=[event]).start()


                elif event.object['text'].lower() == 'Нaзад'.lower():
                    msg_send(event.object.peer_id, 'Хорошо!', main_keyboard())
                elif event.object['text'].lower() == 'Назад'.lower():
                    msg_send(event.object.peer_id, 'Хорошо!', search_keyboard())

                else:
                    msg_send(event.object.peer_id, 'Не смог понять команду')

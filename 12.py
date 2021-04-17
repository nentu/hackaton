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

vkSession = VkApi(token='724ac9ca603d6d82f66f9716a19b06fb26108aad5d533deaefd375b7dd38853c3471bce39905f155bad0f')
longPoll = VkBotLongPoll(vkSession, 204037695 )
vk = vkSession.get_api()

def create_empty_keyboard():
    keyboardd = VkKeyboard.get_empty_keyboard()
    return keyboardd
    # Эта функция используется для закрытия клавиатуры


def courses(event):
    global main_list
    msg_send(event.object.peer_id,
             'Запустится поиск по ключевым словам\n'
             'Список кружков: (сортировка в алфавитном порядке)\n'
             '(название кружка), (ссылка на группу), (Имя и фамилия преподавателя), (ссылка на его стр в вк), (Твоя средняя оценка)/(Средняя оценка по группе)', coutses_keyboard())

def achievement(event):
    global main_list
    msg_send(event.object.peer_id,
             'Здесь можно добавить новое достижение, которое будет отправлено на подтверждение тренеру, или посмотреть имеющиеся', achievement_keyboard())
def new_achievement(event):
    global main_list
    msg_send(event.object.peer_id,
             'Выберите количество баллов за это достижение', new_achievement_keyboard())
def new_achievement_2(event):
    global main_list

    def cansel_keyboard():
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("Отмена", color=VkKeyboardColor.DEFAULT)
        return keyboard.get_keyboard()

    msg_send(event.object.peer_id,
             'Опишите, за что вы получили это достижение и прикрепите фото или видео, если они нужны', cansel_keyboard())
    tmp = main_list['is_sending_ach'].copy()
    tmp[main_list[main_list['id'] == event.object.peer_id].index.values.tolist()[0]] = True
    main_list['is_sending_ach'] = tmp

def course_search(event):
    global main_list
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
def send_photo(peer_id, attachments, msg, random_id=0):
    vkSession.method('messages.send',
        {"peer_id": peer_id, "message":msg, "attachment": attachments, "random_id": random_id})

def upload_achinment(event):
    global main_list

    tmp = main_list['achivments'].copy()
    tmp[main_list[main_list['id'] == event.object.peer_id].index.values.tolist()[0]].append(event.object['text'])
    main_list['achivments'] = tmp

    for item in event.object['attachments']:
        if item['type'] == 'photo':
            print('photo', event.object.peer_id, event.object['text'], None, ['photo{}_{}'.format(item['photo']['owner_id'], item['photo']['id'])])
            msg_send(event.object.peer_id, event.object['text'], None, ['photo{}_{}'.format(item['photo']['owner_id'], item['photo']['id'])])
            #send_photo(648859248, 'photo{}_{}'.format(item['photo']['owner_id'], item['photo']['id']), 'sfsdf')


def current_achs(event):
    global main_list
    tmp = main_list['achivments'][main_list[main_list['id'] == event.object.peer_id].index.values.tolist()[0]]
    msg_send(event.object.peer_id, 'Твои дотижения:\n'+'\n'.join([str(i+1)+') '+tmp[i] for i in range(len(tmp))]),sharing_achs_keyboard())

def sharing_achs(event):
    global main_list

    tmp = main_list['is_sharing_ach'].copy()
    tmp[main_list[main_list['id'] == event.object.peer_id].index.values.tolist()[0]] = True
    main_list['is_sharing_ach'] = tmp

    msg_send(event.object.peer_id, 'Введите номер достижения для выбора и дальнейшей публикации',sharing_achs_keyboard())

def sharing_achs_keyboard():
    keyboard = VkKeyboard(one_time=False)


    keyboard.add_button("Хочу опубликовать одно из них", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("Нaзaд", color=VkKeyboardColor.DEFAULT)
    return keyboard.get_keyboard()

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
    # True если она должна закрваться\

    keyboard.add_button("Посмотреть имеющиеся", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("Добавить новое", color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button("Hазад", color=VkKeyboardColor.DEFAULT)

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


def sharing_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button("На стене", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("В истории", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("В сообщениях", color=VkKeyboardColor.POSITIVE)
    return keyboard.get_keyboard()
def hau_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button("Я ученик", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("Я родитель", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("Я учитель", color=VkKeyboardColor.POSITIVE)
    return keyboard.get_keyboard()


def msg_send(user_id, text, keyboard=main_keyboard(), attachments =[]):
    max_len = 4092
    if 1:
        if text != '':
            kols = len(text) // max_len
            vk.messages.send(peer_id=user_id,
                             message=text[0:max_len],
                             random_id=get_random_id(),
                             attachment = attachments,
                             keyboard=keyboard)
            for i in range(kols):
                vk.messages.send(peer_id=user_id,
                                 message=text[max_len * i:max_len * (i + 1)],
                                 random_id=get_random_id())
    #except Exception:
    #    pass
#msg_send(389093483, 'Ghbdtn', None, 'photo389093483_457248228')

main_list = pd.DataFrame({'id': [3819093483, 305703132], 'type': ['teacher', 'student'], 'is_sending_ach':[False, False], 'teacher':[305703132, 389093483],'is_sharing_ach':[False, False],'sharing_ach_id':[None, None], 'courses':[['Клуб дзюдо 98'], []], 'lessons_times':[['Дзюдо 16:00 - 18:00', '-', 'Английский 16;00 - 18:00', '-', 'Дзюдо 16:00-18:00', '-', '-'], ['Дзюдо 16:00 - 18:00', '-', 'Английский 16;00 - 18:00', '-', 'Дзюдо 16:00-18:00', '-', '-']], 'achivments':[[], []]})

print('start')
while True:

    if 1:
        for event in longPoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:

                if not event.object.peer_id in main_list.id.values.tolist():
                    if event.object['text'].lower() == 'Я ученик'.lower():
                        main_list = main_list.append({'id': event.object.peer_id,
                                                      'type': 'student',
                                                      'is_sending_ach': False,
                                                      'is_sharing_ach': False,
                                                      'sharing_ach_id': None,
                                                      'courses': [],
                                                      'lessons_times': [],
                                                      'achivments': []}, ignore_index=True)
                        msg_send(event.object.peer_id, 'Привет!', main_keyboard())
                    elif event.object['text'].lower() == 'Я учитель'.lower():
                        main_list = main_list.append({'id': event.object.peer_id,
                                                      'type': 'teacher',
                                                      'is_sending_ach': False,
                                                      'is_sharing_ach': False,
                                                      'sharing_ach_id': None,
                                                      'courses': [],
                                                      'lessons_times': [],
                                                      'achivments': []}, ignore_index=True)
                        msg_send(event.object.peer_id, 'Здравствуйте!', main_keyboard())
                    elif event.object['text'].lower() == 'Я родитель'.lower():
                        main_list = main_list.append({'id': event.object.peer_id,
                                                      'type': 'parent',
                                                      'is_sending_ach': False,
                                                      'is_sharing_ach': False,
                                                      'sharing_ach_id': None,
                                                      'courses': [],
                                                      'lessons_times': [],
                                                      'achivments': []}, ignore_index=True)
                        msg_send(event.object.peer_id, 'Здравствуйте!', main_keyboard())
                    else:
                        msg_send(event.object.peer_id, 'Здравствуйте! Кто вы!', hau_keyboard())
                    continue

                if main_list['is_sending_ach'][main_list[main_list['id'] == event.object.peer_id].index.values.tolist()[0]] == True:
                    if event.object['text'].lower() == 'отмена':
                        msg_send(event.object.peer_id, 'Загрузка достижения отменена', achievement_keyboard())
                    else:
                        print('ach')
                        threading.Thread(target=upload_achinment, args=[event]).start()
                        msg_send(event.object.peer_id, 'Достижение отправлено учителю')
                    tmp = main_list['is_sending_ach'].copy()
                    tmp[main_list[main_list['id'] == event.object.peer_id].index.values.tolist()[0]] = False
                    main_list['is_sending_ach'] = tmp
                    continue
                elif main_list['is_sharing_ach'][main_list[main_list['id'] == event.object.peer_id].index.values.tolist()[0]] == True:
                    if str(event.object['text']).isdigit() and 0<int(event.object['text'])<len(main_list['achivments'][main_list[main_list['id'] == event.object.peer_id].index.values.tolist()[0]])+1:
                        tmp = main_list['sharing_ach_id'].copy()
                        tmp[main_list[main_list['id'] == event.object.peer_id].index.values.tolist()[0]] = int(event.object['text'])
                        main_list['sharing_ach_id'] = tmp

                        tmp = main_list['is_sharing_ach'].copy()
                        tmp[main_list[main_list['id'] == event.object.peer_id].index.values.tolist()[0]] = False
                        main_list['is_sharing_ach'] = tmp
                        msg_send(event.object.peer_id, 'Как вы хотите поделиться достижением?', keyboard=sharing_keyboard())
                    else:
                        msg_send(event.object.peer_id, 'Пришлите число- номер достижения', None)
                    continue



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
                elif event.object['text'].lower() == 'Посмотреть имеющиеся'.lower():
                    threading.Thread(target=current_achs, args=[event]).start()
                elif event.object['text'].lower() == 'Хочу опубликовать одно из них'.lower():
                    threading.Thread(target=sharing_achs, args=[event]).start()
                elif event.object['text'].lower() in ['На стене'.lower(), 'В сообщениях'.lower(), 'В истории'.lower()]:
                    msg_send(event.object.peer_id, 'Достижение опубликовано', achievement_keyboard())
                elif event.object['text'].lower() == 'Нaзад'.lower() or event.object['text'].lower() == 'Hазад'.lower():
                    msg_send(event.object.peer_id, 'Хорошо!', main_keyboard())
                elif event.object['text'].lower() == 'Назад'.lower():
                    msg_send(event.object.peer_id, 'Хорошо!', search_keyboard())


                elif event.object['text'].lower() == 'Расписание'.lower():
                    tmp = main_list['lessons_times'][
                        main_list[main_list['id'] == event.object.peer_id].index.values.tolist()[0]]
                    if len(tmp)!=0:
                        msg = 'Расписание на 7 дней\n'
                        for i in range(7):
                            msg += (datetime.datetime.today() + datetime.timedelta(days=i)).date().strftime(
                                "%d.%m.%Y") + ': ' + tmp[i] + '\n'

                        msg_send(event.object.peer_id, msg, None)
                    else:
                        msg_send(event.object.peer_id, 'У вас еще нет расписания', None)


                else:
                    msg_send(event.object.peer_id, 'Не смог понять команду')

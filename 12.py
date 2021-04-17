from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import threading, datetime
import json
import pandas as pd
# Общие

GROUP_TOKEN = '724ac9ca603d6d82f66f9716a19b06fb26108aad5d533deaefd375b7dd38853c3471bce39905f155bad0f'
API_VERSION = '5.120'

# Запускаем бот
vk_session = VkApi(token=GROUP_TOKEN, api_version=API_VERSION)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id=204037695)

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
        keyboard.add_button("Отмена", color=VkKeyboardColor.SECONDARY)
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
def list_new_courses():
    keyboard = VkKeyboard(one_time=False)
    for i in range(9):
        keyboard.add_button("Кружок номер " + str(i+1), color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
    keyboard.add_button("Назад", color=VkKeyboardColor.SECONDARY)
    return keyboard.get_keyboard()
def course_search_by_geopos(event):



    msg_send(event.object.peer_id,
             'Появится изображение карты с ближайшими кружками в радиусе 1 км, где каждый имеет свои индекс для выбора',list_new_courses())

def course_search_by_text(event):
    global main_list
    def list_new_courses():
        keyboard = VkKeyboard(one_time=False)
        for i in range(9):
            keyboard.add_button("Кружок номер " + str(i+1), color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
        keyboard.add_button("Назад", color=VkKeyboardColor.SECONDARY)
        return keyboard.get_keyboard()

    tmp = main_list['is_searching'].copy()
    tmp[main_list[main_list['id'] == event.object.peer_id].index.values.tolist()[0]] = True
    main_list['is_searching'] = tmp
    msg_send(event.object.peer_id,
             'Список кружков в городе пользователя (с индексами для поиска).\n'
             'В дальнейшем планируется сделать сортировку кружков по рейтенгу, подходящих под пол и возраст ребенка,',None)
def send_photo(peer_id, attachments, msg, random_id=0):
    vkSession.method('messages.send',
        {"peer_id": peer_id, "message":msg, "attachment": attachments, "random_id": random_id})

def upload_achinment(event):
    global main_list

    tmp = main_list['achivments'].copy()
    tmp[main_list[main_list['id'] == event.object.peer_id].index.values.tolist()[0]].append(event.object['text']+': на одобрении')
    main_list['achivments'] = tmp

    teacher = main_list['teacher'][main_list[main_list['id'] == event.object.peer_id].index.values.tolist()[0]]
    vk.messages.send(
        user_id=teacher,
        random_id=get_random_id(),
        peer_id=teacher,
        keyboard=keyboard_1.get_keyboard(),
        message='Заявка на достижение:\n'
                'От: https://vk.com/id'+str(event.object.peer_id)+
                '\nДостижение:\n'+event.object['text'])

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
    keyboard.add_button("Галерея достижений", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("Нaзaд", color=VkKeyboardColor.SECONDARY)
    return keyboard.get_keyboard()

def coutses_keyboard():
    keyboard = VkKeyboard(one_time=False)
    # False Если клавиатура должна оставаться откртой после нажатия на кнопку
    # True если она должна закрваться

    keyboard.add_button("Найти новый кружок", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("Нaзад", color=VkKeyboardColor.SECONDARY)
    return keyboard.get_keyboard()

def achievement_keyboard():
    keyboard = VkKeyboard(one_time=False)
    # False Если клавиатура должна оставаться откртой после нажатия на кнопку
    # True если она должна закрваться\

    keyboard.add_button("Посмотреть имеющиеся", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("Добавить новое", color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button("Hазад", color=VkKeyboardColor.SECONDARY)

    return keyboard.get_keyboard()

def new_achievement_keyboard():
    keyboard = VkKeyboard(one_time=False)
    # False Если клавиатура должна оставаться откртой после нажатия на кнопку
    # True если она должна закрваться
    for i in range(2, 5):
        keyboard.add_button(str(i)+" балла", color=VkKeyboardColor.SECONDARY)
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
    keyboard.add_button("Вернуться в главное меню", color=VkKeyboardColor.SECONDARY)

    return keyboard.get_keyboard()


def sharing_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button("На стене", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("В истории", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("В сообщениях", color=VkKeyboardColor.POSITIVE)
    return keyboard.get_keyboard()

def rank_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button("В кружке", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("По городу", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("По стране", color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button("Hазад", color=VkKeyboardColor.SECONDARY)

    return keyboard.get_keyboard()
def hau_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button("Я ученик", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("Я родитель", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("Я учитель", color=VkKeyboardColor.POSITIVE)
    return keyboard.get_keyboard()

def join_course():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button("Присоединиться", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("Отмена", color=VkKeyboardColor.SECONDARY)
    return keyboard.get_keyboard()

# №1. Клавиатура с 3 кнопками: "показать всплывающее сообщение", "открыть URL" и изменить меню (свой собственный тип)
keyboard_1 = VkKeyboard(**dict(one_time=False, inline=True))
keyboard_1.add_callback_button(label='1 балл', color=VkKeyboardColor.POSITIVE, payload={"type": "1_point"})
keyboard_1.add_callback_button(label='2 балла', color=VkKeyboardColor.POSITIVE, payload={"type": "2_point"})
keyboard_1.add_callback_button(label='3 балла', color=VkKeyboardColor.POSITIVE, payload={"type": "3_point"})
keyboard_1.add_line()
keyboard_1.add_callback_button(label='Отклонить достижение', color=VkKeyboardColor.PRIMARY, payload={"type": "Denied"})

def msg_send(user_id, text, keyboard=main_keyboard(), attachments =[]):
    max_len = 4092
    if 1:
        if text != '':
            kols = len(text) // max_len


            vk.messages.send(peer_id=user_id,
                             user_id=user_id,
                             message=text[0:max_len],
                             random_id=get_random_id(),
                             attachment = attachments,
                             keyboard=keyboard)
            for i in range(kols):
                vk.messages.send(peer_id=user_id,
                                 message=text[max_len * i:max_len * (i + 1)],
                                 random_id=get_random_id())

main_list = pd.DataFrame({'id': [389093483, 305703132], 'type': ['teacher', 'student'], 'is_sending_ach':[False, False], 'teacher':[389093483, 305703132],'is_sharing_ach':[False, False],'is_searching':[False, False],'sharing_ach_id':[None, None], 'courses':[['Клуб дзюдо 98'], []], 'lessons_times':[['Дзюдо 16:00 - 18:00', '-', 'Английский 16;00 - 18:00', '-', 'Дзюдо 16:00-18:00', '-', '-'], ['Дзюдо 16:00 - 18:00', '-', 'Английский 16;00 - 18:00', '-', 'Дзюдо 16:00-18:00', '-', '-']], 'achivments':[[], []]})

for event in longpoll.listen():
    # отправляем меню 1го вида на любое текстовое сообщение от пользователя
    if event.type == VkBotEventType.MESSAGE_NEW:

        if event.object['text'] != '':
            if event.from_user:
                main_list.to_csv('data.csv', encoding='utf-8', index=False)
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
                        continue
                    elif event.object['text']=='Нaзaд':
                        tmp = main_list['is_sharing_ach'].copy()
                        tmp[main_list[main_list['id'] == event.object.peer_id].index.values.tolist()[0]] = False
                        main_list['is_sharing_ach'] = tmp
                        msg_send(event.object.peer_id, 'Хорошо', None)

                    else:
                        msg_send(event.object.peer_id, 'Пришлите число- номер достижения', None)
                        continue
                elif main_list['is_searching'][main_list[main_list['id'] == event.object.peer_id].index.values.tolist()[0]] == True:
                    tmp = main_list['is_searching'].copy()
                    tmp[main_list[main_list['id'] == event.object.peer_id].index.values.tolist()[0]] = False
                    main_list['is_searching'] = tmp
                    if event.object['text'].lower() in 'Клуб дзюдо 98'.lower().split():
                        msg_send(event.object.peer_id, '1) Клуб дзюдо 98', join_course())
                    else:
                        msg_send(event.object.peer_id, 'Кружки не найдены', None)
                    continue


                if 'привет' in event.object['text'].lower() or event.object['text'].lower() == 'начать':
                    msg_send(event.object.peer_id, 'Привет!', main_keyboard())
                elif event.object['text'].lower() == 'Вернуться в главное меню'.lower():
                    msg_send(event.object.peer_id, 'Хорошо!', main_keyboard())
                elif event.object['text'].lower() == 'мои кружки':
                    threading.Thread(target=courses, args=[event]).start()
                elif event.object['text'].lower() == 'Найти новый кружок'.lower():
                    threading.Thread(target=course_search, args=[event]).start()
                elif event.object['text'].lower() == 'По геопозиции'.lower() or event.object['text'].lower() == 'Отмена'.lower():
                    threading.Thread(target=course_search_by_geopos, args=[event]).start()
                elif event.object['text'].lower() == 'По имени в моем городе'.lower():
                    threading.Thread(target=course_search_by_text, args=[event]).start()
                elif event.object['text'].lower() == 'Мои достижения'.lower() or event.object['text'].lower() == 'Нaзaд'.lower():
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
                elif 'Кружок номер'.lower() in event.object['text'].lower():
                    msg_send(event.object.peer_id, 'Полная информация с местоположением и ссылкой на группу', join_course())
                elif event.object['text'].lower() == 'Присоединиться'.lower():
                    msg_send(event.object.peer_id, 'Заявка на вступлени в кружок была отправлена на подтверждение', list_new_courses())
                elif event.object['text'].lower() == 'Рейтинг'.lower():
                    msg_send(event.object.peer_id, 'Выберите область рейтинга', rank_keyboard())
                elif event.object['text'].lower() == 'Галерея достижений'.lower():
                    msg_send(event.object.peer_id, 'Здесь будут достижения с их фотографиями и видео', None)

                elif event.object['text'].lower() in ['По стране'.lower(), 'По городу'.lower(), 'В кружке'.lower()]:
                    msg_send(event.object.peer_id, 'Ваш рейтинг '+event.object['text'].lower()+': 1/1', rank_keyboard())

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
                # Если клиент пользователя не поддерживает callback-кнопки,
                # нажатие на них будет отправлять текстовые
                # сообщения. Т.е. они будут работать как обычные inline кнопки.


    # обрабатываем клики по callback кнопкам
    elif event.type == VkBotEventType.MESSAGE_EVENT:
        print(event)
        if 'point' in event.object.payload.get('type'):
            tmp = main_list['achivments'].copy()
            for i in main_list[main_list['teacher']==event.object.peer_id].index.values.tolist():
                print(tmp[i])
                if len(tmp[i])>0:
                    if tmp[i][-1][-1*len(': на одобрении'):] == ': на одобрении':

                        tmp[i][-1] = tmp[i][-1][:-1*len(': на одобрении')]+'. Баллов: '+event.object.payload.get('type')[0]
            main_list['achivments'] = tmp

            last_id = vk.messages.edit(
                      peer_id=event.obj.peer_id,
                      message='Подтверждено, поставлены баллов: '+event.object.payload.get('type')[0],
                      conversation_message_id=event.obj.conversation_message_id,
                      keyboard=None)
        elif event.object.payload.get('type') == 'Denied':
            last_id = vk.messages.edit(
                      peer_id=event.obj.peer_id,
                      message='Отклонено',
                      conversation_message_id=event.obj.conversation_message_id,
                      keyboard=None)

if __name__ == '__main__':
    print()

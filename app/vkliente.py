import vk_api as api
import time

file = open('config.txt', 'r+')
TOKEN = file.read()
session = api.VkApi(token=TOKEN)
vk = session.get_api()


def menu():
    print('[1] Друзья')
    print('[2] Настройки')
    print('[3] Отложенные сообщения')
    menu_input = int(input())
    if menu_input == 1:
        message()
    if menu_input == 2:
        settings()
    if menu_input == 3:
        delay()

def settings():
    postfix = ''
    f = open('settings.txt', 'r')
    set_fr = int(f.readline())
    set_mes = int(f.readline())
    set_order = f.readline()
    old1 = str(set_fr)
    old2 = str(set_mes)
    unread = ''
    old3 = set_order
    f.close()
    data = vk.friends.get(order=set_order, count=set_fr, fields='nickname, online', name_case='nom')
    if set_order == 'hints':
        o = 'по важности'
    if set_order == 'name':
        o = 'по алфавиту'
    print('''Вы вошли в меню настроек. 
Количество друзей в меню – ''', set_fr, "Изменить – /set friends, максимум – " + str(data['count']))
    print('Количество сообщений в диалоге – ', set_mes, "Изменить – /set messages, максимум - 200")
    print('Режим отображения друзей – ', o + '. Изменить – /set order (1 - По важности, 2 - по имени)')
    print('/exit чтобы выйти')
    option = input()
    if option == '/exit':
        menu()
    if option[:12] == '/set friends':
        f = open('settings.txt', 'w')
        set_fr = str(set_fr)
        new_data = set_fr.replace(old1, option[13:])
        if int(new_data) > data['count']:
            print('Число превышает максимально возможное')
            time.sleep(1)
        else:
            with open('settings.txt', 'w') as f:
                f.write(new_data + '\n')
                f.write(old2 + '\n')
                f.write(old3)
            print('Количество друзей в меню –', new_data)
            message()
    elif option[:13] == '/set messages':
        f = open('settings.txt', 'w')
        set_mes = str(set_mes)
        new_data = set_mes.replace(old2, option[14:])
        with open('settings.txt', 'w') as f:
            f.write(old1 + '\n')
            f.write(new_data + '\n')
            f.write(old3)
        print('Количество сообщений в диалоге –', new_data)
        message()
    elif option[:10] == '/set order':
        f = open('settings.txt', 'w')
        if option[11:] == '1':
            new_data = 'hints'
            o = 'по важности'
        elif option[11:] == '2':
            new_data = 'name'
            o = 'по имени'
        else:
            print('Неверный формат')
        with open('settings.txt', 'w') as f:
            f.write(old1 + '\n')
            f.write(old2 + '\n')
            f.write(new_data)
        print('Режим отображения друзей –', o)
        menu()


def message():
    vm_check = False
    postfix = ''
    f = open('settings.txt', 'r')
    set_fr = int(f.readline())
    set_mes = int(f.readline())
    set_order = f.readline()
    old1 = str(set_fr)
    old2 = str(set_mes)
    unread = ''
    i = 0
    old3 = set_order
    f.close()
    global msg
    data = vk.friends.get(order=set_order, count=set_fr, fields='nickname, online', name_case='nom')
    read = vk.messages.getConversations(filter='unread')
    # получение непрочитанных сообщений
    read = vk.messages.getConversations(filter='unread')
    for i in range(read['unread_count']):
        if read['items'][i]['conversation']['peer']['type'] == 'user':
            try:
                if read['items'][i]['conversation']['unread_count'] != 0:
                    unread_id = str(read['items'][i]['conversation']['peer']['id'])
                    unread = unread + unread_id
            except KeyError:
                i += 1
    # вывод списка друзей
    for i in range(set_fr):
        numb = i + 1
        if str(data['items'][i]['id']) in unread and int(data['items'][i]['online']) == 1:
            print('[' + str(numb) + ']', data['items'][i]['first_name'], data['items'][i]['last_name'] + '⭕️️🟢')
        if str(data['items'][i]['id']) in unread:
            print('[' + str(numb) + ']', data['items'][i]['first_name'], data['items'][i]['last_name'] + '⭕️️')
        if int(data['items'][i]['online']) == 1:
            print('[' + str(numb) + ']', data['items'][i]['first_name'], data['items'][i]['last_name'] + '🟢')
        else:
            print('[' + str(numb) + ']', data['items'][i]['first_name'], data['items'][i]['last_name'])
    name = input()
    try:
        name = int(name)
    except ValueError:
        menu()
    data = vk.friends.get(order=set_order, count=set_fr, fields='nickname', name_case='ins')
    print(data['items'][int(name) - 1]['id'])
    print("Диалог с", data['items'][name - 1]['first_name'], data['items'][name - 1]['last_name'],". Пиши '/back' чтобы вернуться")
    vk.messages.markAsRead(peer_id= data['items'][name - 1]['id'])
    id = data['items'][name - 1]['id']
    msg = vk.messages.getHistory(user_id=id, rev=0, count = set_mes)
    n_mes = 0
    if msg['count'] < set_mes:
        n_mes = msg['count']
    else:
        n_mes = set_mes
    for i in range(n_mes):
        coef = n_mes - 1 - i
        try:
            if msg['items'][coef]['attachments'][0]['type'] == 'audio_message' and msg['items'][coef]['out'] == 1:
                print('Вы🎤:' + msg['items'][coef]['attachments'][0]['audio_message']['transcript'])
                i += 1
            if msg['items'][coef]['attachments'][0]['type'] == 'audio_message':
                print('🎤:' + msg['items'][coef]['attachments'][0]['audio_message']['transcript'])
                i += 1
        except IndexError:
            i += 1
            if msg['items'][coef]['out'] == 1:
                print('Вы: ' + msg['items'][coef]['text'])
            else:
                print(msg['items'][coef]['text'])
    text = input()
    while True:
        if text != "/back" and text != "" and text != '/rfr' and text != '/menu':
            vk.messages.send(user_id=id, random_id=0, message=text)
            text = input()
        elif text == '/rfr':
            msg = vk.messages.getHistory(peer_id=id, rev=0)
            if msg['count'] < set_mes:
                i = 0
                for i in range(msg['count']):
                    coef = msg['count'] - 1 - i
                    if msg['items'][coef]['out'] == 1:
                        print('Вы: ' + msg['items'][coef]['text'])
                    else:
                        print(msg['items'][coef]['text'])
            else:
                for i in range(set_mes):
                    coef = set_mes - 1 - i
                    print(coef)
                    if msg['items'][coef]['out'] == 1:
                        print('Вы: ' + msg['items'][coef]['text'])
                    else:
                        print(msg['items'][coef]['text'])
            text = input()
        elif text == '/menu':
            menu()
        else:
            message()


def delay():
    shorts = []
    sh = input('Enter short name(id)')
    while sh != "STOP":
        if sh == '/menu':
            menu()
            break
        shorts.append(sh)
        sh = input('Keep on entering ids. Enter "STOP" to stop')
    names = vk.users.get(user_ids=shorts, name_case='dat')
    ids = []  # массив c id указанных людей
    for i in range(len(shorts)):
        ids.append(names[i]['id'])
    print(ids)
    text = input('Enter message text')
    first = []
    last = []
    for i in range(len(ids)):
        first.append(names[i]['first_name'])
        last.append(names[i]['last_name'])

    day = int(input('Enter date'))
    month = int(input('Enter month'))
    year = int(input('Enter year'))
    hour = int(input('Enter hour'))
    minute = int(input('Enter minute'))

    print("Are you thure that you want to send", text, "to", last, 'at', str(hour) + ':' + str(minute),
          str(day) + '.' + str(month) + '.' + str(year))
    conf = input('(y/n)?')
    if conf == 'y':
        while True:
            struct = time.localtime()
            y = struct.tm_year
            m = struct.tm_mon
            d = struct.tm_mday
            h = struct.tm_hour
            minu = struct.tm_min
            print('Waiting...')
            if year <= y and month <= m and day <= d and hour <= h and minute <= minu:
                for i in range(len(ids)):
                    vk.messages.send(user_id=ids[i], random_id=0, message=text)
                print("Message was sent.")
                menu()
            time.sleep(10)
    else:
        menu()

menu()
input()

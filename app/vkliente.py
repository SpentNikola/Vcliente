import vk_api as api
import time

file = open('config.txt', 'r+')
TOKEN = file.read()
session = api.VkApi(token=TOKEN)
vk = session.get_api()

def message():
    f = open('settings.txt', 'r')
    set_fr = int(f.readline())
    set_mes = int(f.readline())
    set_order = f.readline()
    old1 = str(set_fr)
    old2 = str(set_mes)
    old3 = set_order
    f.close()
    global msg
    data = vk.friends.get(order=set_order, count=set_fr, fields='nickname, online', name_case='nom')
    # вывод списка друзей
    for i in range(set_fr):
        numb = i + 1
        if int(data['items'][i]['online']) == 1:
            print('[' + str(numb) + ']', data['items'][i]['first_name'], data['items'][i]['last_name'], '🟢')
        else:
            print('[' + str(numb) + ']', data['items'][i]['first_name'], data['items'][i]['last_name'])
    name = input()
    #меню настроек
    if name == '/settings':
        if set_order == 'hints':
            o = 'по важности'
        if set_order == 'name':
            o = 'по алфавиту'
        print('''Вы вошли в меню настроек. 
Количество друзей в меню – ''', set_fr, "Изменить – /set friends, максимум – "+ str(data['count']))
        print('Количество сообщений в диалоге – ', set_mes, "Изменить – /set messages, максимум -")
        print('Режим отображения друзей – ', o + '. Изменить – /set order (1 - По важности, 2 - по имени)')
        print('/exit чтобы выйти')
        option = input()
        if option == '/exit':
            message()
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
                    f.write(old2+ '\n')
                    f.write(old3)
                print('Количество друзей в меню –', new_data)
                message()
        elif option[:13] == '/set messages':
            f = open('settings.txt', 'w')
            set_mes = str(set_mes)
            new_data = set_mes.replace(old2, option[14:])
            with open('settings.txt', 'w') as f:
                f.write(old1 + '\n')
                f.write(new_data+ '\n')
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
            message()
    if name == '':
        message()
    else:
        try:
            name = int(name)
        except ValueError:
            messages()
    data = vk.friends.get(order='hints', count=set_fr, fields='nickname', name_case='ins')
    print(data['items'][name - 1]['id'])
    print("Диалог с", data['items'][name - 1]['first_name'], data['items'][name - 1]['last_name'],". Пиши '/back' чтобы вернуться")
    id = data['items'][name - 1]['id']
    msg = vk.messages.getHistory(user_id=id, rev=0, count = set_mes)
    if msg['count'] < set_mes:
        for i in range(msg['count']):
            coef = msg['count'] - 1 - i
            #print(msg['items'][coef]['text'])
            if msg['items'][coef]['out'] == 1:
                print('Вы: ' + msg['items'][coef]['text'])
            else:
                print(msg['items'][coef]['text'])
    else:
        for i in range(set_mes):
            #print(msg['items'][set_mes - 1 - i]['text'])
            if msg['items'][set_mes - 1 - i]['out'] == 1:
                print('Вы: ' + msg['items'][set_mes - 1 - i]['text'])
            else:
                print(msg['items'][set_mes - 1 - i]['text'])
    text = input()
    while True:
        if text != "/back" and text != "" and text != '/rfr':
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
        else:
            message()
message()
input()


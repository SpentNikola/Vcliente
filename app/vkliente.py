import vk_api as api

file = open('config.txt', 'r+')
TOKEN = file.read()
session = api.VkApi(token=TOKEN)
vk = session.get_api()


def message():
    f = open('settings.txt', 'r')
    set_fr = int(f.readline())
    set_mes = int(f.readline())
    old1 = str(set_fr)
    old2 = str(set_mes)
    f.close()
    global msg
    data = vk.friends.get(order='hints', count=set_fr, fields='nickname, online', name_case='nom')
    for i in range(set_fr):
        numb = i + 1
        if int(data['items'][i]['online']) == 1:
            print('[' + str(numb) + ']', data['items'][i]['first_name'], data['items'][i]['last_name'], ' online🟢')
        else:
            print('[' + str(numb) + ']', data['items'][i]['first_name'], data['items'][i]['last_name'])
    name = input()
    if name == '/settings':
        print('''Вы вошли в меню настроек. 
Количество друзей в меню – ''', set_fr, "Изменить – /set friends")
        print('Количество сообщений в диалоге – ', set_mes, "Изменить – /set messages")
        print('/exit чтобы выйти')
        option = input()
        if option == '/exit':
            message()
        if option[:12] == '/set friends':
            f = open('settings.txt', 'w')
            set_fr = str(set_fr)
            new_data = set_fr.replace(old1, option[13:])
            with open('settings.txt', 'w') as f:
                f.write(new_data + '\n')
                f.write(old2)
            print('Количество друзей в меню –', new_data)
            message()
        elif option[:13] == '/set messages':
            f = open('settings.txt', 'w')
            set_mes = str(set_mes)
            new_data = set_mes.replace(old2, option[14:])
            with open('settings.txt', 'w') as f:
                f.write(old1 + '\n')
                f.write(new_data)
            print('Количество друзей в меню –', new_data)
            message()
    else:
        name = int(name)
    data = vk.friends.get(order='hints', count=set_fr, fields='nickname', name_case='ins')
    for k in range(set_mes):
        if name == (k + 1):
            global id
            id = data['items'][k]['id']
            print("Диалог с", data['items'][k]['first_name'], data['items'][k]['last_name'],
                  ". Пиши '/back' чтобы вернуться")
            msg = vk.messages.getHistory(peer_id=id, rev=0)
            if msg['count'] < set_mes:
                i = 0
                for i in range(msg['count']):
                    coef = msg['count'] - 1 - i
                    print(msg['items'][coef]['text'])
            else:
                for i in range(set_mes):
                    print(msg['items'][set_mes - 1 - i]['text'])
    text = input()
    while True:
        if text != "/back" and text != "" and text != '/rfr':
            vk.messages.send(user_id=id, random_id=0, message=text)
            text = input()
        elif text == '/rfr':
            msg = vk.messages.getHistory(peer_id=id, rev=0, count=10)
            for i in range(set_mes):
                print(msg['items'][set_mes - 1 - i]['text'])
            text = input()

        else:
            message()
message()
input()

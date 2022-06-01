import vk_api  as api

file = open('config.txt', 'r')
TOKEN = file.read()
session = api.VkApi(token=TOKEN)
vk = session.get_api()

def message():
    global msg
    data = vk.friends.get(order = 'hints', count = 10,  fields = 'nickname, online', name_case = 'nom')    
    for i in range(10):
        numb = i + 1
        if int(data['items'][i]['online']) == 1:
            print('[' + str(numb) + ']', data['items'][i]['first_name'], data['items'][i]['last_name'], ' online🟢')
        else:
            print('[' + str(numb) + ']', data['items'][i]['first_name'], data['items'][i]['last_name'])
    name = int(input())
    data = vk.friends.get(order = 'hints', count = 10,  fields = 'nickname', name_case = 'ins')
    for k in range(10):
        if name == (k+1):
            global id
            id = data['items'][k]['id']
            print("Диалог с", data['items'][k]['first_name'], data['items'][k]['last_name'], ". Пиши '!back' чтобы вернуться")
            msg = vk.messages.getHistory(peer_id = id, rev = 0)
            if msg['count']<10:
                i = 0
                
                for i in range(msg['count']):
                    coef = msg['count'] - 1 - i
                    print(msg['items'][coef]['text'])
            else:
                for i in range(10):
                    print(msg['items'][9-i]['text'])
    text = input()
    while True:
        if text !="!back" and text != "":
            vk.messages.send(user_id = id, random_id = 0, message = text)
            text = input()
        elif text == '!rfr':
            message()
        else:
            message()

message()
input()

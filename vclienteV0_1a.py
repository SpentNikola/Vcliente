import vk_api  as api

file = open('config.txt', 'r')
TOKEN = file.read()
session = api.VkApi(token=TOKEN)
vk = session.get_api()

def message():
    data = vk.friends.get(order = 'hints', count = 10,  fields = 'nickname', name_case = 'ins')    
    for i in range(10):
        numb = i + 1
        print('[' + str(numb) + ']', data['items'][i]['first_name'], data['items'][i]['last_name'])
    name = int(input())
    for k in range(10):
        if name == (k+1):
            id = data['items'][k]['id']
            print("Диалог с", data['items'][k]['first_name'], data['items'][k]['last_name'], ". Пиши '!back' чтобы вернуться")
    text = input()
    while True:
        if text !="!back" or text != "":
            vk.messages.send(user_id = id, random_id = 0, message = text)
            text = input()
       else:
            message()
message()
exit = input('crush')

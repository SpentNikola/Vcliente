import time
import vk_api  as api
import os

file = open('config228.txt', 'r')
TOKEN = file.read()
session = api.VkApi(token=TOKEN)
vk = session.get_api()
count = 0
count1 = 1

def message():
    data = vk.friends.get(order = 'hints', count = 5, fields = 'nickname')
    i = 0    
    for i in range(5):
        numb = i + 1
        print('[' + str(numb) + ']', data['items'][i]['first_name'], data['items'][i]['last_name'])
    name = int(input())
    for k in range(5):
        if name == (k+1):
            id = data['items'][k]['id']
            print("Диалог с", data['items'][k]['first_name'], data['items'][k]['last_name'], ". Пиши '!back' чтобы вернуться")
    text = input()
    while text !="!back" or text != " ":
        if text !="!back" or text != " ":
            vk.messages.send(user_id = id, random_id = 0, message = text)
            text = input()
        if text == "!back" or text == " ":
            message()
message()
exit = input()
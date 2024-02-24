from config import URL, FORWARD

from db import addMessage

import pprint
import requests


#For skip offline updates
def firstUpdate():
    offset = None
    params = {'timeout': 10, 'offset': offset}
    response = requests.get(url=URL + 'getUpdates', params=params)
    upd = response.json()
    if len(upd['result']) > 0: 
        offset = upd['result'][-1]['update_id'] + 1
    return offset


#for text message
def sendMessage(text:str, user_name:str, user_id):
    params = {
        'chat_id': FORWARD,
        'text': f'{user_id}    @{user_name} \n\n{text}',
    }
    requests.get(url=URL + 'sendMessage', params=params)
    addMessage(user_id=user_id, user_name=user_name, text=text)


#for message with photo
def sendPhoto( photo_id:str, user_name:str, user_id, caption=''):
    params = {
        'chat_id': FORWARD,
        'caption': f'{user_id}    @{user_name} \n\n{caption}',
        'photo': photo_id,
    }
    requests.get(url=URL + 'sendPhoto', params=params)
    addMessage(user_id=user_id, user_name=user_name, photo_id=photo_id, caption=caption)


def answerCommand(text:str, user_name:str, user_id, chat_id):
    if text == '/start':
        params = {
            'chat_id': chat_id,
            'text': f'Hello',
        }
        requests.get(url=URL + 'sendMessage', params=params)
    else:
        params = {
            'chat_id': chat_id,
            'text': f'Not found',
        }
        requests.get(url=URL + 'sendMessage', params=params)


def hendelUpdate(update):
    
    if 'entities' in update['message']:
        if update['message']['entities'][0]['type'] == 'bot_command':
            text = update['message']['text']
            user_id = update['message']['from']['id']
            chat_id = update['message']['chat']['id']
            user_name = update['message']['from']['username']
            answerCommand(text=text, user_name=user_name, user_id=user_id, chat_id=chat_id)
    
    elif 'text' in update['message']:
        text = update['message']['text']
        user_id = update['message']['from']['id']
        #chat_id = update['message']['chat']['id']
        user_name = update['message']['from']['username']
        sendMessage(text, user_name, user_id)
        
    elif 'photo' in update['message']:
        caption = ''
        photo_id = update['message']['photo'][-1]['file_id']
        user_id = update['message']['from']['id']
        user_name = update['message']['from']['username']
        if 'caption' in update['message']:
            caption = update['message']['caption']

        sendPhoto(photo_id, user_name, user_id, caption)
        #pprint.pprint(update['message']['photo'][-1]['file_id'])
    


def getUpdates():
    offset = firstUpdate()
    #params = {'timeout': 10, 'offset': offset}
    while True:
        params = {'timeout': 10, 'offset': offset}
        response = requests.get(url=URL + 'getUpdates', params=params)
        updates = response.json()
        if len(updates['result']) > 0:
            offset = updates['result'][-1]['update_id'] + 1
            for update in updates['result']:
                #pprint.pprint(update)
                #if update['message']['from']['id'] != FORWARD: #не пересылает сообщения того кому пересылает.
                    hendelUpdate(update=update)
        

def main():
    getUpdates()


if __name__ == '__main__':
    main()
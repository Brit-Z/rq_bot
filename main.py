from config import URL, FORWARD

from db import addMessage

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
def sendMessage(text:str, user_name:str, user_id, recipient_id=''):
    if user_id != FORWARD:
        params = {
            'chat_id': FORWARD,
            'text': f'{user_id}    @{user_name} \n\n{text}',
        }
    else:
        params = {
            'chat_id': recipient_id,
            'text': f'{text}',
        }

    requests.get(url=URL + 'sendMessage', params=params)
    addMessage(user_id=user_id, user_name=user_name, text=text)


#for message with photo
def sendPhoto( photo_id:str, user_name:str, user_id, caption='', recipient_id=''):
    if user_id != FORWARD:
        params = {
            'chat_id': FORWARD,
            'caption': f'{user_id}    @{user_name} \n\n{caption}',
            'photo': photo_id,
        }
    else:
        params = {
            'chat_id': recipient_id,
            'caption': f'{caption}',
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
    else:
        params = {
            'chat_id': chat_id,
            'text': f'Not supported',
        }

    requests.get(url=URL + 'sendMessage', params=params)


def getRecipientId(update):
    if 'text' in update['message']['reply_to_message'] and True == update['message']['reply_to_message']['from']['is_bot']:
        recipient_id = update['message']['reply_to_message']['text']
        recipient_id = recipient_id.split(' ')[0]
    elif 'photo' in update['message']['reply_to_message'] and True == update['message']['reply_to_message']['from']['is_bot']:
        recipient_id = update['message']['reply_to_message']['caption']
        recipient_id = recipient_id.split(' ')[0]

    return recipient_id


def hendelUpdate(update):

    if True == update['message']['from']['is_bot']:
        return 0

    user_id = update['message']['from']['id']
    chat_id = update['message']['chat']['id']
    user_name = update['message']['from']['username']
    
    if 'entities' in update['message']:
        if update['message']['entities'][0]['type'] == 'bot_command':
            text = update['message']['text']
            answerCommand(text=text, user_name=user_name, user_id=user_id, chat_id=chat_id)
    
    elif 'text' in update['message']:
        text = update['message']['text']
        if user_id != FORWARD:
            sendMessage(text, user_name, user_id)
        elif 'reply_to_message' in update['message']:
            recipient_id = getRecipientId(update)
            sendMessage(text, user_name, user_id, recipient_id)
        
    elif 'photo' in update['message']:
        caption = ''
        photo_id = update['message']['photo'][-1]['file_id']
        if 'caption' in update['message']:
            caption = update['message']['caption']

        if user_id != FORWARD:
            sendPhoto(photo_id, user_name, user_id, caption)
        elif 'reply_to_message' in update['message']:
            recipient_id = getRecipientId(update)
            sendPhoto(photo_id, user_name, user_id, caption, recipient_id)
    else:
        answerCommand(text=text, user_name=user_name, user_id=user_id, chat_id=chat_id)
    

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
                #if update['message']['from']['id'] != FORWARD: #не пересылает сообщения того кому пересылает. #Теперь эта строка не нужна
                    hendelUpdate(update=update)
        

def main():
    getUpdates()


if __name__ == '__main__':
    main()
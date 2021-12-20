import requests, json, os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

def telegram_bot_remove_messages():
    
    bot_token = os.environ.get("BOT_TOKEN")
    bot_chatID = os.environ.get("BOT_CHAT_ID")
    get_messages_url = 'https://api.telegram.org/bot' + bot_token + '/getUpdates'
    response = requests.get(get_messages_url)
    result = response.json().get('result')
    for message in result:
        message_id = str(message['message']['message_id'])
        deleteResponse = requests.get('https://api.telegram.org/bot' + bot_token + '/getUpdates?chat_id=' + bot_chatID + '&message_id=' + message_id)
        print(deleteResponse)

telegram_bot_remove_messages()
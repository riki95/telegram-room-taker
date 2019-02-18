import json
import os
import sys
import aws_db as db

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./vendored"))
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot

TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)

bot = Bot(TOKEN)

def format_items(items):
    res = ''
    
    for item in items:
        res += json.dumps(item) + '\n'
        
    return res


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def handler(event, context):
    print('=== start ===')
    
    try:
        data = json.loads(event["body"])
        message = str(data["message"]["text"])
        chat_id = data["message"]["chat"]["id"]

        if '/scan' in message:
            response = format_items(db.scan_table('uc_db'))
        elif '/add' in message:
            mess_args = message.split()
            r = mess_args [1]
            response = r
        elif '/rooms' in message:
            button_list = [
                InlineKeyboardButton("col1", callback_data='uno'),
                InlineKeyboardButton("col2", callback_data='due'),
                InlineKeyboardButton("row 2", callback_data='tre')
            ]
            reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
            bot.send_message(chat_id, "A two-column menu", reply_markup=reply_markup)
            
        else:
            response = 'hello' #json.dumps(event)

        print('res', response)

        

    except Exception as e:
        response = str(e)
    
    data = {"text": response.encode("utf8"), "chat_id": chat_id}
    url = BASE_URL + "/sendMessage"
    requests.post(url, data)

    print('=== end ===')
    return {"statusCode": 200}
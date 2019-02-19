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


def handler_cb(data):
    text = data["callback_query"]["data"]
    chat_id = data["callback_query"]["message"]["chat"]["id"]
    cb_id = data["callback_query"]["id"]
    bot.answer_callback_query(cb_id)
    bot.send_message(chat_id, text)


def handler_mess(data):
    try:    
        message = str(data["message"]["text"])
        chat_id = data["message"]["chat"]["id"]

        reply_markup = None

        if '/scan' in message:
            response = format_items(db.scan_table('uc_db'))
        elif '/add' in message:
            mess_args = message.split()
            r = mess_args [1]
            response = r
        elif '/rooms' in message:
            button_list = [
                InlineKeyboardButton("Room 214", callback_data='214'),
                InlineKeyboardButton("Room 215", callback_data='215'),
                InlineKeyboardButton("Room 216", callback_data='216'),
                InlineKeyboardButton("Room 217", callback_data='217')
            ]
            reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
            response = "A two-column menu"
        else:
            response = 'hello'
    except Exception as e:
        response = str(e)

    bot.send_message(chat_id, response, reply_markup=reply_markup)


def handler(event, context):
    print('=== start ===')    

    data = json.loads(event["body"])
    if 'callback_query' in data:
        handler_cb(data)
    else:
        handler_mess(data)

    print('=== end ===')
    return {"statusCode": 200}
import json
import os
import sys
import traceback
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
        res += 'Room {item[room]}: {status}\n'.format(
            item=item, 
            status='occupied' if item["occupied"] else 'free')
    return res


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def button_list(rooms, status):
    return [ 
        InlineKeyboardButton(
            "Room {}".format(room["room"]),
            callback_data='room {} {}'.format(room["room"], status)
        ) for room in rooms
    ]


def handler_cb(data):
    try:
        text = data["callback_query"]["data"]
        chat_id = data["callback_query"]["message"]["chat"]["id"]
        cb_id = data["callback_query"]["id"]

        text = text.split()
        bot.send_message(chat_id, json.dumps(text))

        if text[0] == 'room':
            db.insert_table(text[1], bool(text[2]))
            bot.send_message(chat_id, 'room {} {}'.format(text[1], 'taken' if bool(text[2]) else 'freed'))

        bot.answer_callback_query(cb_id)

    except Exception:
        bot.send_message(chat_id, traceback.format_exc())

def handler_mess(data):
    try:    
        bot.send_message(660987935, json.dumps(data["message"]))

        message = str(data["message"]["text"])
        chat_id = data["message"]["chat"]["id"]

        if '/status' in message:
            bot.send_message(chat_id, format_items(db.scan_table()))
        elif '/add' in message:
            mess_args = message.split()
            bot.send_message(chat_id, mess_args[1])
        elif '/take' in message:
            reply_markup = InlineKeyboardMarkup(build_menu(button_list(db.scan_table(), True), n_cols=2))
            bot.send_message(chat_id, "Take a room:", reply_markup=reply_markup)
        elif '/free' in message:
            reply_markup = InlineKeyboardMarkup(build_menu(button_list(db.scan_table(), False), n_cols=2))
            bot.send_message(chat_id, "Free a room:", reply_markup=reply_markup)
        else:
            bot.send_message(chat_id, 'ciao')
    except Exception:
        bot.send_message(chat_id, traceback.format_exc())


def handler(event, context):
    try:
        print('=== start ===')    

        bot.send_message('660987935', 'wewe')
        data = json.loads(event["body"])
        if 'callback_query' in data:
            bot.send_message('660987935', 'cb')
            handler_cb(data)
        else:
            bot.send_message('660987935', 'msg')
            handler_mess(data)

        print('=== end ===')
    except Exception:
        bot.send_message('660987935', traceback.format_exc())
    finally:
        return {"statusCode": 200}
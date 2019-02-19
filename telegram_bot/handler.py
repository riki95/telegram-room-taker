import json
import os
import sys
import traceback

import aws_db as db

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, './vendored'))
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot


TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = 'https://api.telegram.org/bot{}'.format(TOKEN)


bot = Bot(TOKEN)


def format_items(items):
    res = ''
    for item in items:
        res += 'Room {item[room]}: {status}\n'.format(
            item=item,
            status='occupied' if item['occupied'] else 'free')
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
            'Room {}'.format(room['room']),
            callback_data='room {} {}'.format(room['room'], status)
        ) for room in rooms
    ]


def handle_cb_room(data):
    chat_id = data['callback_query']['message']['chat']['id']
    text = data['callback_query']['data'].split()

    room = text[1]
    take = text[2] == 'take'

    db.insert_table(room, take)

    bot.send_message(chat_id, 'room {} {}'.format(room, 'taken' if take else 'freed'))



def handler_cb(data):
    cb_id = data['callback_query']['id']
    text = data['callback_query']['data'].split()

    if text[0] == 'room':
        handle_cb_room(data)

    bot.answer_callback_query(cb_id)


def handle_status(data):
    chat_id = data['message']['chat']['id']

    bot.send_message(chat_id, format_items(db.scan_table()))


def handle_room(data, action):
    chat_id = data['message']['chat']['id']

    buttons = button_list(db.scan_table(), action)
    menu = build_menu(buttons, n_cols=2)

    reply_markup = InlineKeyboardMarkup(menu)

    bot.send_message(chat_id, 'Take a room:', reply_markup=reply_markup)


def handler_mess(data):
    bot.send_message(660987935, json.dumps(data['message']))

    message = str(data['message']['text'])
    chat_id = data['message']['chat']['id']

    if '/status' in message:
        handle_message()
    elif '/add' in message:
        pass
    elif '/take' in message:
        handle_room(data, 'take')
    elif '/free' in message:
        handle_room(data, 'free')
    else:
        bot.send_message(chat_id, 'ciao')


def handler(event, context):
    try:
        print('=== start ===')

        data = json.loads(event['body'])
        if 'callback_query' in data:
            handler_cb(data)
        else:
            handler_mess(data)

        print('=== end ===')
    except Exception:
        bot.send_message('660987935', traceback.format_exc())
    finally:
        return {'statusCode': 200}

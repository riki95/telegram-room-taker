import json
import os
import sys
import traceback

import aws_db as db
import builders as builder

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, './vendored'))
from telegram import Bot


TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = 'https://api.telegram.org/bot{}'.format(TOKEN)
CHAT_BOT = os.environ['CHAT_BOT']

bot = Bot(TOKEN)


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

    bot.send_message(chat_id, builder.format_items(db.scan_table()))


def handle_room(data, action):
    chat_id = data['message']['chat']['id']

    buttons = builder.button_list(db.scan_table(), action)
    reply_markup = builder.build_menu(buttons, n_cols=2)

    bot.send_message(chat_id, 'Take a room:', reply_markup=reply_markup)


def handler_mess(data):
    bot.send_message(CHAT_BOT, json.dumps(data['message']))

    message = str(data['message']['text'])
    chat_id = data['message']['chat']['id']

    if '/status' in message:
        handle_status(data)
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
        bot.send_message(CHAT_BOT, traceback.format_exc())
    finally:
        return {'statusCode': 200}

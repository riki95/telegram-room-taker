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

	if take:
		db.update(room, take, chat_id)
	else:
		db.update(room, take, '0')

	bot.send_message(chat_id, 'room {} {}'.format(room, 'taken' if take else 'freed'))



def handler_cb(data):
	cb_id = data['callback_query']['id']
	text = data['callback_query']['data'].split()

	if text[0] == 'room':
		handle_cb_room(data)

	bot.answer_callback_query(cb_id)


def handle_status(data):
	chat_id = data['message']['chat']['id']

	bot.send_message(chat_id, builder.format_items(db.scan()))


def handle_room(data, action):
	chat_id = data['message']['chat']['id']

	occupied = action == 'free'
	if occupied:
		rooms = db.query(occupied, chat_id)
	else:
		rooms = db.query(occupied, '0')

	if len(rooms) == 0:
		bot.send_message(chat_id, 'No rooms available\nCheck /status' if action == 'take' else 'No rooms are occupied\nCheck /status')
	else:
		buttons = builder.button_list(rooms, action)
		reply_markup = builder.build_menu(buttons, n_cols=2)

		bot.send_message(chat_id, 'Choose a room to {}:'.format(action), reply_markup=reply_markup)


def handler_mess(data):
	message = str(data['message']['text'])
	chat_id = data['message']['chat']['id']

	if '/status' in message:
		handle_status(data)
	elif '/take' in message:
		handle_room(data, 'take')
	elif '/free' in message:
		handle_room(data, 'free')
	elif '/start' in message:
		first_name = data['message']['chat']['first_name']

		bot.send_message(chat_id, 'Welcome {}, click /info to see available commands'.format(first_name))
	elif '/info' in message:
		bot.send_message(chat_id, '/status to see available rooms\n/take to reserve a room\n/free to end reservation')
	else:
		pass


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
import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, './vendored'))

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot

def format_items(items):
    res = ''
    for item in items:
        res += 'Room {item[room]}: {status} by {item[id]}\n'.format(
            item=item,
            status='occupied' if item['occupied'] else 'free')
    return res


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    reply_markup = InlineKeyboardMarkup(menu)
    return reply_markup


def button_list(rooms, status):
    return [
        InlineKeyboardButton(
            'Room {}'.format(room['room']),
            callback_data='room {} {}'.format(room['room'], status)
        ) for room in rooms
    ]
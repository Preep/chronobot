import telebot
from telebot import types as telebot_types
import os
from . import parser
from .database import db_handler

dir_name = os.path.dirname(__file__)

with open(os.path.join(dir_name, 'token.txt'), 'r') as f:
    token = f.read()

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def __start_handler(message: telebot_types.Message):
    bot.send_message(message.chat.id, 'Приветик я будущий бот, я пока что в разработке. Попробуй позже.')


@bot.message_handler(content_types=['text'])
def __text_handler(message: telebot_types.Message):

    parsed_message_dict = parser.parse_and_sanitize(message.text)
    parsed_message_dict['chat_id'] = message.chat.id
    parsed_message_dict['user_id'] = message.from_user.id

    if parsed_message_dict['error'] is None:
        parsed_message_dict['color'] = None # TODO: Add colors keyboard for event types as per chronometr method by Kamaeva

        if db_handler.add_event(parsed_message_dict):
            bot.send_message(message.chat.id, 'Событие добавлено') # TODO: Add different cheerful messages
        else:
            bot.send_message(message.chat.id, 'Ой сломался') # TODO: Remove later

    else:
        bot.send_message(message.chat.id, parsed_message_dict['error'])


def start_polling():
    # bot.infinity_polling()
    bot.polling()

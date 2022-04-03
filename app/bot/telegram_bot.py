import telebot
from telebot import types as telebot_types
import os
from .parser import parse_and_sanitize

file_path = os.path.dirname(__file__)

with open(os.path.join(file_path, 'token.txt'), 'r') as f:
    token = f.read()

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def __start_handler(message: telebot_types.Message):
    bot.send_message(message.chat.id, 'Приветик я будущий бот, я пока что в разработке. Попробуй позже.')


@bot.message_handler(content_types=['text'])
def __text_handler(message: telebot_types.Message):

    parsed_message_dict = parse_and_sanitize(message.text)
    parsed_message_dict['chat_id'] = message.chat.id

    if parsed_message_dict['error'] is None:
        bot.send_message(message.chat.id, str(parsed_message_dict)) # TODO: Delete when DB handler is ready
        # TODO: Add colors keyboard for event types as per chronometr method by Kamaeva
        # TODO: Send parsed data and chosen color to IO handler
    else:
        bot.send_message(message.chat.id, parsed_message_dict['error'])


def start_polling():
    # bot.infinity_polling()
    bot.polling()

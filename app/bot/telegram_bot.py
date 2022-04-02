import telebot
from telebot.types import Message
import os
from .parser import parse_and_sanitize

file_path = os.path.dirname(__file__)

with open(os.path.join(file_path, 'token.txt'), 'r') as f:
    token = f.read()

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def __start_handler(message: Message):
    bot.send_message(message.chat.id, 'Приветик я будущий бот, я пока что в разработке. Попробуй позже.')


@bot.message_handler(content_types=['text'])
def __text_handler(message: Message):

    parsed_message_dict = parse_and_sanitize(message.text)
    bot.send_message(message.chat.id, str(parsed_message_dict))

    # if ok:
        # Show color menu
        # Send parsed text and color to IO handler
    # else:
        # Show error message


def start_polling():
    bot.infinity_polling()

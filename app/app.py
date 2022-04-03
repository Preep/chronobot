import bot.telegram_bot as telegram_bot
from bot.database import db_handler

if __name__ == '__main__':
    db_handler.init()
    telegram_bot.start_polling()

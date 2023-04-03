# в этом файле вся основа приложения, регистрация команд, запуск приложения

import logging
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import ApplicationBuilder
from telegram.ext import CommandHandler
from general_file_with_function import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)
proxy_url = "socks5://user:pass@host:port"
app = ApplicationBuilder().token("5853283682:AAH8OfYbD093o3_OAK2rMP-cCkR_8mIs9EE").proxy_url(proxy_url).build()


def main():
    application = Application.builder().token("5853283682:AAH8OfYbD093o3_OAK2rMP-cCkR_8mIs9EE").build()
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add", add))
    application.add_handler(CommandHandler("look_all", look_all))

    application.run_polling()


if __name__ == '__main__':
    main()

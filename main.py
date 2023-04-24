# в этом файле вся основа приложения, регистрация команд, запуск тг и бд

import logging
from telegram.ext import Application, MessageHandler, filters, ConversationHandler
from telegram.ext import ApplicationBuilder
from telegram.ext import CommandHandler
from general_file_with_function import *
from data import db_session

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
    application.add_handler(CommandHandler("look_all", look_all))
    conv_handler1 = ConversationHandler(
        entry_points=[CommandHandler('add', add)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_source)],  # бот спрашивает про ссылку на товар
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_price)]  # бот спрашивает про цену
        },
        fallbacks=[CommandHandler('stop_add', stop_add)]  # полностью добавляет товар в бд
    )
    conv_handler2 = ConversationHandler(
        entry_points=[CommandHandler('delete', delete)],
        states={1: [MessageHandler(filters.TEXT & ~filters.COMMAND, d)]
                },
        fallbacks=[CommandHandler('stop_delete', stop_delete)]
    )
    application.add_handler(CommandHandler('ptp', price_vs_price))
    application.add_handler(conv_handler1)
    application.add_handler(conv_handler2)
    job_queue = app.job_queue
    job_queue.run_repeating(price_vs_price, interval=60, first=10)
    application.run_polling()


if __name__ == '__main__':
    db_session.global_init("db/goods_from_wb.db")
    main()

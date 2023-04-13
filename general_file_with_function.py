# здесь все функции для бота
# https://www.wildberries.ru/catalog/83511998/detail.aspx?targetUrl=MI
# https://www.wildberries.ru/catalog/83511998/detail.aspx
from telegram import ReplyKeyboardMarkup
from telegram.ext import ConversationHandler
from selenium_wb import selenium_find

reply_keyboard2 = [['/add'], ['/look_all']]
markup2 = ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True, resize_keyboard=True)


async def help(update, context):
    file_text = open('texts/help_text', mode='r', encoding="utf-8")
    data_read = file_text.read()
    await update.message.reply_text(data_read, reply_markup=markup2)


reply_keyboard1 = [['/help']]
markup = ReplyKeyboardMarkup(reply_keyboard1, one_time_keyboard=True, resize_keyboard=True)


async def start(update, context):
    file_text = open('texts/start_text', mode='r', encoding="utf-8")
    data_read = file_text.read()
    await update.message.reply_text(data_read, reply_markup=markup)


reply_keyboard3 = [['/stop_add']]
markup3 = ReplyKeyboardMarkup(reply_keyboard3, one_time_keyboard=True, resize_keyboard=True)


async def add(update, context):  # команда пользователя, бот спрашивает про ссылку на товар с вб
    await update.message.reply_text("Добавление нового товара для отслеживания.\n"
                                    "\n"
                                    "Отправь артикул товара из котолога Wildberries\n", reply_markup=markup3)
    return 1


async def ask_source(update, context):  # бот читает ссылку на товар и спрашивает о цене
    source_product = update.message.text  # здесь ответ пользователя - артикул на товар
    await update.message.reply_text('Артикул получен, немного подождите...')
    answ = selenium_find(source_product)
    if answ is None:
        await update.message.reply_text('Кажется, что-то пошло не так. Повторите попытку.', reply_markup=markup4)
        return ConversationHandler.END
    await update.message.reply_text(
        f"Артикул на {answ} получена.\n"
        f"\n"
        f"Напиши цену, ниже которой надо оповестить тебя:)", reply_markup=markup3)
    return 2


async def ask_price(update, context):  # бот считывает цену, завершает диалог и добавляет все в бд
    price_product = update.message.text
    await update.message.reply_text('Цена получена.\n'
                                    'Товар добавлен в список отслеживаемых.\n'
                                    'Мы оповестим тебя сразу, как только цена на товар упадёт!')
    return ConversationHandler.END


reply_keyboard4 = [['/add'], ['/look_all'],
                   ['/help']]
markup4 = ReplyKeyboardMarkup(reply_keyboard4, one_time_keyboard=True, resize_keyboard=True)


async def stop_add(update, context):  # останавливает диалог и добавляет цену и товар в бд
    await update.message.reply_text('Товар не добавлен в список отслеживаемых.\n'
                                    'Выберите дальнейшие действия.', reply_markup=markup4)
    return ConversationHandler.END


async def look_all(update, context):
    pass

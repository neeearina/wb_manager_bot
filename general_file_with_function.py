# здесь все функции для бота
from telegram import ReplyKeyboardMarkup

reply_keyboard2 = [['/add'], ['/look_all']]
markup2 = ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=False, resize_keyboard=True)


async def help(update, context):
    file_text = open('texts/help_text', mode='r', encoding="utf-8")
    data_read = file_text.read()
    await update.message.reply_text(data_read, reply_markup=markup2)


reply_keyboard1 = [['/help']]
markup = ReplyKeyboardMarkup(reply_keyboard1, one_time_keyboard=False, resize_keyboard=True)


async def start(update, context):
    file_text = open('texts/start_text', mode='r', encoding="utf-8")
    data_read = file_text.read()
    await update.message.reply_text(data_read, reply_markup=markup)


async def add(update, context):
    pass


async def look_all(update, context):
    pass

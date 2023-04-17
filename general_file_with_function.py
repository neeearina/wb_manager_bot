# здесь все функции для бота
# https://www.wildberries.ru/catalog/83511998/detail.aspx?targetUrl=MI
# https://www.wildberries.ru/catalog/83511998/detail.aspx
from telegram import ReplyKeyboardMarkup
from telegram.ext import ConversationHandler
from selenium_wb import selenium_find, find_good_in_db, add_to_db, look, deleting

reply_keyboard2 = [['/add'], ['/look_all']]
markup2 = ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True, resize_keyboard=True)


async def help(update, context):
    file_text = open('texts/help_text', mode='r', encoding="utf-8")
    data_read = file_text.read()
    await update.message.reply_text(data_read, reply_markup=markup2)


reply_keyboard1 = [['/help']]
markup = ReplyKeyboardMarkup(reply_keyboard1, one_time_keyboard=True, resize_keyboard=True)


async def start(update, context):
    # user_id = update.message.from_user.id
    file_text = open('texts/start_text', mode='r', encoding="utf-8")
    data_read = file_text.read()
    await update.message.reply_text(data_read, reply_markup=markup)


reply_keyboard3 = [['/stop_add']]
markup3 = ReplyKeyboardMarkup(reply_keyboard3, one_time_keyboard=True, resize_keyboard=True)


async def add(update, context):  # команда пользователя, бот спрашивает про ссылку на товар с вб
    await update.message.reply_text("Добавление нового товара для отслеживания.\n"
                                    "\n"
                                    "Отправь артикул товара из каталога Wildberries\n", reply_markup=markup3)
    return 1


sp_for_db = []


async def ask_source(update, context):  # бот читает ссылку на товар и спрашивает о цене
    articul = update.message.text  # здесь ответ пользователя - артикул на товар
    chat_id = update.message.from_user.id
    sp_for_db.append(articul)
    sp_for_db.append(chat_id)
    await update.message.reply_text('Артикул получен')
    if articul.isdigit():
        answ = find_good_in_db(articul, chat_id)  # True или False
    else:
        await update.message.reply_text('Неверный формат артикула. Попробуйте еще раз.', reply_markup=markup4)
        sp_for_db.clear()
        return ConversationHandler.END
    if answ:
        await update.message.reply_text('Этот товар уже отслеживается.', reply_markup=markup4)
        sp_for_db.clear()
        return ConversationHandler.END
    await update.message.reply_text('Проверяем действительность артикула. Это займет время...')
    sp = selenium_find(articul)  # ['155916960', 'O`SHADE Кеды летние из натуральной кожи', '3 888 ₽']
    if sp is not None:
        sp_for_db.append(sp[1])
        sp_for_db.append(sp[2])
        await update.message.reply_text(
            f"Артикул на {sp[1]} действителен.\n"
            f"\n"
            f"Напиши цену, ниже которой надо оповестить тебя:)", reply_markup=markup3)
        return 2
    else:
        await update.message.reply_text('Артикул недействителен. Попробуйте еще раз.', reply_markup=markup4)
        sp_for_db.clear()
        return ConversationHandler.END


async def ask_price(update, context):  # бот считывает цену, завершает диалог и добавляет все в бд
    price_product_to_look = str(update.message.text).strip('₽')
    sp_for_db.append(price_product_to_look)
    print(price_product_to_look)
    # ['155916960', 984914572, 'O`SHADE Кеды летние из натуральной кожи', '3 888 ₽', '400']
    if price_product_to_look.isdigit():  # если пользователь отправил реальную цену
        await update.message.reply_text('Цена получена.\n'
                                        'Товар добавлен в список отслеживаемых.\n'
                                        'Мы оповестим тебя сразу, как только цена на товар упадёт!',
                                        reply_markup=markup4)
        add_to_db(sp_for_db[0], sp_for_db[1], sp_for_db[2], sp_for_db[3], sp_for_db[4])
        sp_for_db.clear()
        return ConversationHandler.END
    # если пользователь отправил не цену
    await update.message.reply_text('Введена неправильная цена. Попробуйте еще раз', reply_markup=markup4)
    return ConversationHandler.END


reply_keyboard4 = [['/add'], ['/look_all'],
                   ['/help'], ['/delete']]
markup4 = ReplyKeyboardMarkup(reply_keyboard4, one_time_keyboard=True, resize_keyboard=True)


async def stop_add(update, context):  # останавливает диалог и добавляет цену и товар в бд
    await update.message.reply_text('Товар не добавлен в список отслеживаемых.\n'
                                    'Выберите дальнейшие действия.', reply_markup=markup4)
    sp_for_db.clear()
    return ConversationHandler.END


async def look_all(update, context):
    sp = look()
    await update.message.reply_text('Номер товара, артикул, название, текущая, цена, цена отслеживания',
                                    reply_markup=markup4)
    for elem in sp:
        await update.message.reply_text(f'{elem}',
                                        reply_markup=markup4)
        return ConversationHandler.END
    return ConversationHandler.END


async def delete(update, context):
    await update.message.reply_text('Чтобы удалить товар, введите его номер',
                                    reply_markup=markup4)
    sp = look()
    await update.message.reply_text('Номер товара, артикул, название, текущая, цена, цена(от)',
                                    reply_markup=markup4)
    for elem in sp:
        await update.message.reply_text(f'{elem}',
                                        reply_markup=markup4)
    return 1


async def d(update, context):
    price_product_to_look = int(update.message.text)
    await update.message.reply_text('Номер товара получен',
                                    reply_markup=markup4)
    deleting(price_product_to_look)
    await update.message.reply_text('Неверный или несуществующий номер товара',
                                    reply_markup=markup4)
    return ConversationHandler.END


async def stop_delete(update, context):
    await update.message.reply_text('Товар не удален.\n'
                                    'Выберите дальнейшие действия.', reply_markup=markup4)
    return ConversationHandler.END

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import urllib.request
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os
from data import __all_models, db_session
from data.allgoods import OrmGoods


def add_to_db(articul, chat_id, name_good=1, price_good=1, price_to_look=1):  # добавление нового товара в базу данных
    db_sess = db_session.create_session()  # подключаемся к бд
    g = OrmGoods()
    g.chat_id = chat_id
    g.articul_good = articul
    g.name_good = name_good
    g.price_good = price_good
    g.price_to_look = price_to_look

    db_sess.add(g)
    db_sess.commit()


def find_good_in_db(articul, chat_id):
    db_sess = db_session.create_session()  # подключаемся к бд
    sp1 = []
    for element in db_sess.query(OrmGoods).filter(OrmGoods.chat_id == int(chat_id),
                                                  OrmGoods.articul_good == int(articul)):
        sp1.append(element)
    if len(sp1) == 0:
        sp1.clear()
        return False  # в бд не нашли, поэтому добавили новый элемент в бд
    else:
        sp1.clear()
        return True  # в бд нашли уже добавленный товар


def selenium_find(articul):
    try:
        url = 'https://www.wildberries.ru/'
        service = Service(executable_path='C:/chromedriver/chromedriver')  # указываем путь до драйвера
        browser = webdriver.Chrome(service=service)
        browser.get(url)
        time.sleep(1)
        wb_search = browser.find_element(By.ID, 'searchInput')
        wb_search.send_keys(articul)
        wb_search.send_keys(Keys.ENTER)
        time.sleep(2)  # заходим на страницу самого товара вб по артикулу
        """Вытаскиваем название, артикул, цена"""
        good_name = browser.find_element(By.CLASS_NAME, 'product-page__header').text
        good_id = browser.find_element(By.ID, 'productNmId').text
        good_price = browser.find_element(By.CLASS_NAME, 'price-block__final-price').text
        print(good_name, good_price)

        # cont = browser.find_element(By.CLASS_NAME, 'sw-slider-kt-mix__wrap')  # находим класс со слайдером
        # good_img = cont.find_element(By.TAG_NAME, 'img')  # находим тег фотографии
        # source_photo = good_img.get_attribute('src')  # ссылка на фото
        # img = urllib.request.urlopen(source_photo).read()
        # out = open("img.jpg", "wb")
        # out.write(img)
        # out.close()
        time.sleep(1)
        browser.quit()
        return [good_id, good_name, good_price]
    except Exception:
        browser.quit()
        return None

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import urllib.request
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os


def selenium_find(articul):
    try:
        url = 'https://www.wildberries.ru/'
        service = Service(executable_path='C:/chromedriver/chromedriver')  # указываем путь до драйвера
        browser = webdriver.Chrome(service=service)
        browser.get(url)
        # time.sleep(1)
        wb_search = browser.find_element(By.ID, 'searchInput')
        wb_search.send_keys(articul)
        wb_search.send_keys(Keys.ENTER)
        # time.sleep(2)  # заходим на страницу самого товара вб по артикулу
        """Вытаскиваем название, артикул, цена"""
        good_name = browser.find_element(By.CLASS_NAME, 'product-page__header').text
        good_id = browser.find_element(By.ID, 'productNmId').text
        good_price = browser.find_element(By.CLASS_NAME, 'price-block__final-price').text
        print(good_name, good_id, good_price)

        # cont = browser.find_element(By.CLASS_NAME, 'sw-slider-kt-mix__wrap')  # находим класс со слайдером
        # good_img = cont.find_element(By.TAG_NAME, 'img')  # находим тег фотографии
        # source_photo = good_img.get_attribute('src')  # ссылка на фото
        # img = urllib.request.urlopen(source_photo).read()
        # out = open("img.jpg", "wb")
        # out.write(img)
        # out.close()
        time.sleep(1)
        browser.quit()
        return good_name
    except Exception:
        browser.quit()
        return None

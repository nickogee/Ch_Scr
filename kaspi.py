import pandas as pd
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import random
import datetime
from share_functions import disc, disc_prercent


CATEGORY = 'Соки, вода, напитки'
URL = 'https://kaspi.kz/shop/c/food/?q=%3AallMerchants%3AMagnum%3AavailableInZones%3AMagnum_ZONE1'
# URL = 'https://2ip.ru/'

CHROMEDRIVER = '/Users/hachimantaro/PycharmProjects/Ch_scrp/chromedriver/chromedriver'


def make_driver():
    useragent = UserAgent()
    driver = webdriver.Chrome(service=Service(CHROMEDRIVER))

    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={useragent.chrome}')
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    return driver


def search_data(driver):
    rezult = []
    driver.get(URL)
    time.sleep(5 + random.randint(0, 7))
    Almaty = driver.find_element(By.CSS_SELECTOR, '[data-city-id="750000000"]')
    Almaty.click()

    category_list = driver.find_elements(By.CLASS_NAME, 'tree__link')

    for category in category_list:

        # Найдена нужная категория
        if category.text == CATEGORY:
            category.click()
            time.sleep(5 + random.randint(-2, 5))

            # ищем список подкатегорий
            sub_category_list = driver.find_elements(By.CLASS_NAME, 'tree__link')

            # начиная с индекса 3 - это список подкатегорий
            for i in range(3, len(sub_category_list)):

                if i > 3:
                    # ищем список подкатегорий занова, после каждой следующей итерации
                    sub_category_list = driver.find_elements(By.CLASS_NAME, 'tree__link')

                sub_category = sub_category_list[i]
                sub_category_text = sub_category.text
                sub_category.click()
                time.sleep(5 + random.randint(0, 15))

                next_page = True
                while next_page:
                    #  Внутри категории ищем элементы с названием и ценой продуктов
                    product_list = driver.find_elements(By.CLASS_NAME, 'item-card__info')

                    for product_card in product_list:
                        title_tag = product_card.find_element(By.CLASS_NAME, 'item-card__name')
                        price_tag = product_card.find_element(By.CLASS_NAME, 'item-card__prices-price')
                        priceL = [j for j in price_tag.text if j.isdigit()]
                        l = {
                            'title': title_tag.text,
                            'sub_category': sub_category_text,
                            'category': CATEGORY,
                            'brand': '',
                            'priceActual': float(''.join(priceL)),
                            'pricePrevious': 0,
                            }

                        rezult.append(l)

                    next_page = push_the_button_next(driver)

                else:
                    # ищем список элементов с категориями и подкатегориями
                    #  и возвращаемся на страницу со списком подкатегорий (кликаем по основной категории)
                    sub_category_list_ = driver.find_elements(By.CLASS_NAME, 'tree__link')
                    category_ = sub_category_list_[2]
                    category_.click()
                    time.sleep(5 + random.randint(0, 10))

            else:
                # все данные по искомой категории просмотренны
                break

    return rezult


def push_the_button_next(driver):


    try:
        next_btn_list = driver.find_elements(By.CLASS_NAME, 'pagination__el')
        next_btn = next_btn_list[-1]
    except Exception:
        # нет кнопок с переключением на след. страницу - это единственная страница по текущей подкатегории
        return False

    try:
        disabled_btn = driver.find_element(By.CLASS_NAME, '_disabled')
    except Exception:
        disabled_btn = None

    if disabled_btn and disabled_btn == next_btn:
        return False
    else:
        next_btn.click()
        time.sleep(5 + random.randint(-2, 10))
        return True


def to_file(rezult):
    now = datetime.datetime.now()
    df = pd.DataFrame(rezult)

    df['discount'] = df.loc[:, ['pricePrevious', 'priceActual']].apply(disc, axis=1)
    df['discount_prc'] = df.loc[:, ['pricePrevious', 'discount']].apply(disc_prercent, axis=1)

    df.to_excel(f'data_rezult/KaspiMagnum - {CATEGORY} {now.strftime("%d_%m_%Y")}.xlsx')
    return


def main():
    driver = make_driver()
    rezult = search_data(driver)
    to_file(rezult)

    time.sleep(5 + random.randint(-2, 10))
    driver.close()
    print('Готово!')


if __name__ == '__main__':
    main()



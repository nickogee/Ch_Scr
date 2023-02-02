import requests
import pandas as pd
import time
import random
from arbuz_fetchs import PARAMS, PAGE_COUNT, URL_NXT, URL_FST, PATTERN, CATEGORY
import datetime
from share_functions import disc, disc_prercent, get_fetch


class ArbuzApiScraper():

    def __init__(self):
        self.rezult = []
        self.df = None
        self.date_time_now = datetime.datetime.now()

    def __rand_pause(self):
        time.sleep(15 + random.randint(-10, 15))

    def __get_next_fetch(self, num):

        if num == 1:
            return get_fetch(URL_FST, PARAMS)
        else:
            return get_fetch(URL_NXT.replace(PATTERN, str(num)), PARAMS)

    def fill_rezult(self):

        for page_num in range(1, PAGE_COUNT + 1):
            print(f'Запрос {page_num} из {PAGE_COUNT}')
            cur_fetch = self.__get_next_fetch(page_num)
            sub_category = cur_fetch.json()['data']['name']
            category = cur_fetch.json()['data']['parent']['data']['name']
            products = cur_fetch.json()['data']['products']['data']

            for product in products:
                l = {
                    'title': product['name'],
                    'sub_category': sub_category,
                    'category': category,
                    'brand': product['brandName'],
                    'priceActual': product['priceActual'],
                    'pricePrevious': product['pricePrevious'],
                }

                self.rezult.append(l)

            if page_num != PAGE_COUNT:
                self.__rand_pause()


    def __make_DataFrame(self):
        df = pd.DataFrame(self.rezult)

        df['discount'] = df.loc[:, ['pricePrevious', 'priceActual']].apply(disc, axis=1)
        df['discount_prc'] = df.loc[:, ['pricePrevious', 'discount']].apply(disc_prercent, axis=1)
        self.df = df

    def __upload_to_excel(self):

        try:
            file_name = f'data_rezult/Арбуз - {CATEGORY} {self.date_time_now.strftime("%d_%m_%Y")}.xlsx'
            self.df.to_excel(file_name)
            print(f'Создан файл {file_name}')
        except Exception as ex:
            print(ex)

    def start(self):
        self.fill_rezult()
        self.__make_DataFrame()
        self.__upload_to_excel()


def main():

    arbuz = ArbuzApiScraper()
    arbuz.start()


if __name__ == '__main__':
    main()





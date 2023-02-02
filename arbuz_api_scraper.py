import pandas as pd
import time
import random
from arbuz_fetchs import PARAMS, URL_NXT, URL_FST, PAGE, SUB_CATALOG, CATALOG_NUMBER
import datetime
from share_functions import disc, disc_prercent, get_fetch


CATEGORY = ''

class ArbuzApiScraper():

    def __init__(self):
        self.rezult = []
        self.df = None
        self.date_time_now = datetime.datetime.now()

    def __rand_pause(self):
        time.sleep(15 + random.randint(-10, 15))

    def fill_rezult(self):
        global CATEGORY

        url = URL_FST.replace(SUB_CATALOG, str(CATALOG_NUMBER))
        fst_fetch = get_fetch(url, PARAMS)
        CATEGORY = fst_fetch.json()['data']['name']

        sub_catalog_list = [{'id': catalog['id'], 'uri': catalog['uri']}
                            for catalog in fst_fetch.json()['data']['catalogs']['data']]

        for sub_catalog_dict in sub_catalog_list:

            url = URL_FST.replace(SUB_CATALOG, str(sub_catalog_dict['id']))
            cur_fetch = get_fetch(url, PARAMS)

            products_count = cur_fetch.json()['data']['products']['page']['count']
            list_lim = cur_fetch.json()['data']['products']['page']['limit']
            add_page = 1 if (products_count % list_lim) > 0 else 0
            page_count = products_count // list_lim + add_page

            for page_num in range(1, page_count + 1):

                # ответ на запрос для первой страницы уже получен,
                if page_num > 1:
                    url = URL_NXT.replace(SUB_CATALOG, str(sub_catalog_dict['id']))
                    url = url.replace(PAGE, str(page_num))
                    cur_fetch = get_fetch(url, PARAMS)

                sub_category = cur_fetch.json()['data']['name']
                products = cur_fetch.json()['data']['products']['data']

                print(f'Запрос {page_num} из {page_count} по {sub_category}')

                for product in products:
                    l = {
                        'title': product['name'],
                        'sub_category': sub_category,
                        'category': CATEGORY,
                        'brand': product['brandName'],
                        'priceActual': product['priceActual'],
                        'pricePrevious': product['pricePrevious'],
                    }

                    self.rezult.append(l)

                if page_num != page_count:
                    self.__rand_pause()

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





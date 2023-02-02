import requests
import pandas as pd
from glovo_fetchs import PARAMS, URL_SERV, URL_FST, CATEGORY
import datetime
from share_functions import disc, disc_prercent



class GlovoApiScraper():

    def __init__(self):
        self.rezult = []
        self.head_response = self.get_fetch(URL_FST, PARAMS)
        self.categories = self.head_response.json()['data']['body'][0]['data']['elements']
        self.df = None
        self.date_time_now = datetime.datetime.now()

    def get_fetch(self, url, params):
        headers = params['headers']
        body = params['body']
        method = params['method']

        if method == 'POST':
            return requests.post(url=url, headers=headers, data=body)
        elif method == 'GET':
            return requests.get(url=url, headers=headers)

    def fill_rezult(self):

        for curr_category in self.categories:
            category_name = curr_category['data']['title']
            cat_route = curr_category['data']['action']['data']['path']
            response = self.get_fetch(URL_SERV + cat_route, PARAMS)
            category_groups = response.json()['data']['body']

            for sub_cat in category_groups:
                sub_category = sub_cat['data']['title']
                products = sub_cat['data']['elements']

                for product in products:
                    l = {
                        'title': product['data']['name'],
                        'sub_category': sub_category,
                        'category': category_name,
                        'brand': '',
                        'priceActual': product['data']['price'],
                        'pricePrevious': 0,
                    }

                    self.rezult.append(l)

    def __make_DataFrame(self):
        df = pd.DataFrame(self.rezult)

        df['discount'] = df.loc[:, ['pricePrevious', 'priceActual']].apply(disc, axis=1)
        df['discount_prc'] = df.loc[:, ['pricePrevious', 'discount']].apply(disc_prercent, axis=1)
        self.df = df

    def __upload_to_excel(self):

        try:
            file_name = f'data_rezult/Глово - {CATEGORY} {self.date_time_now.strftime("%d_%m_%Y")}.xlsx'
            self.df.to_excel(file_name)
            print(f'Создан файл {file_name}')
        except Exception as ex:
            print(ex)

    def start(self):
        self.fill_rezult()
        self.__make_DataFrame()
        self.__upload_to_excel()



now = datetime.datetime.now()

def fetch(url, params):
    headers = params['headers']
    body = params['body']
    method = params['method']

    if method == 'POST':
        return requests.post(url=url, headers=headers, data=body)
    elif method == 'GET':
        return requests.get(url=url, headers=headers)


def get_next_fetch(curr_url):
        return fetch(curr_url, PARAMS)


def fill_rezult():
    rezult = []

    head_response = get_next_fetch(URL_FST)
    categories = head_response.json()['data']['body'][0]['data']['elements']


    for curr_category in categories:

        category_name = curr_category['data']['title']
        cat_route = curr_category['data']['action']['data']['path']

        response = get_next_fetch(URL_SERV + cat_route)
        category_groups = response.json()['data']['body']
        for sub_cat in category_groups:

            sub_category = sub_cat['data']['title']
            products = sub_cat['data']['elements']

            for product in products:
                l = {
                    'title': product['data']['name'],
                    'sub_category': sub_category,
                    'category': category_name,
                    'brand': '',
                    'priceActual': product['data']['price'],
                    'pricePrevious': 0,
                }

                rezult.append(l)

    return rezult


def main():

    glovo = GlovoApiScraper()
    glovo.start()

    # df = pd.DataFrame(fill_rezult())
    #
    # df['discount'] = df.loc[:, ['pricePrevious', 'priceActual']].apply(disc, axis=1)
    # df['discount_prc'] = df.loc[:, ['pricePrevious', 'discount']].apply(disc_prercent, axis=1)
    #
    # df.to_excel(f'data_rezult/Глово - {CATEGORY} {now.strftime("%d_%m_%Y")}.xlsx')
    #
    # print('Готово!')


if __name__ == '__main__':
    main()

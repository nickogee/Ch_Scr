import requests
import pandas as pd
import time
import random
from arbuz_fetchs import PARAMS, PAGE_COUNT, URL_NXT, URL_FST, PATTERN, CATEGORY
import datetime
from share_functions import disc, disc_prercent


now = datetime.datetime.now()

def fetch(url, params):
    headers = params['headers']
    body = params['body']
    method = params['method']

    if method == 'POST':
        return requests.post(url=url, headers=headers, data=body)
    elif method == 'GET':
        return requests.get(url=url, headers=headers)


def get_next_fetch(num):

    if num == 1:
        return fetch(URL_FST, PARAMS)
    else:
        return fetch(URL_NXT.replace(PATTERN, str(num)), PARAMS)


def fill_rezult():
    rezult = []
    for page_num in range(1, PAGE_COUNT + 1):

        print(f'Запрос {page_num} из {PAGE_COUNT}')

        cur_fetch = get_next_fetch(page_num)

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

            rezult.append(l)

        if page_num != PAGE_COUNT:
            time.sleep(15 + random.randint(-10, 15))

    return rezult


def main():
    df = pd.DataFrame(fill_rezult())

    df['discount'] = df.loc[:, ['pricePrevious', 'priceActual']].apply(disc, axis=1)
    df['discount_prc'] = df.loc[:, ['pricePrevious', 'discount']].apply(disc_prercent, axis=1)

    df.to_excel(f'data_rezult/Арбуз - {CATEGORY} {now.strftime("%d_%m_%Y")}.xlsx')

    print('Готово!')

if __name__ == '__main__':
    main()





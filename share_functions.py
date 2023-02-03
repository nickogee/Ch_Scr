import pandas as pd
import requests


def disc(st_df):
    if st_df.pricePrevious:
        return st_df.pricePrevious - st_df.priceActual
    else:
        return 0


def disc_prercent(st_df):
    if st_df.discount:
        return round(st_df.discount / st_df.pricePrevious * 100, 2)
    else:
        return 0


def get_fetch(url, params):
    headers = params['headers']
    body = params['body']
    method = params['method']

    if method == 'POST':
        return requests.post(url=url, headers=headers, data=body)
    elif method == 'GET':
        return requests.get(url=url, headers=headers)


def make_DataFrame(rezult):
    df = pd.DataFrame(rezult)

    df['discount'] = df.loc[:, ['pricePrevious', 'priceActual']].apply(disc, axis=1)
    df['discount_prc'] = df.loc[:, ['pricePrevious', 'discount']].apply(disc_prercent, axis=1)
    return df


def upload_to_excel(df, file_name):

    try:
        df.to_excel(file_name)
        print(f'Создан файл {file_name}')
    except Exception as ex:
        print(ex)

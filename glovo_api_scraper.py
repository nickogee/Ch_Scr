from glovo_fetchs import PARAMS, URL_SERV, URL_FST, CATEGORY
import datetime
from share_functions import get_fetch, make_DataFrame, upload_to_excel


class GlovoApiScraper():

    def __init__(self):
        self.rezult = []
        self.head_response = get_fetch(URL_FST, PARAMS)
        self.categories = self.head_response.json()['data']['body'][0]['data']['elements']
        self.df = None
        self.date_time_now = datetime.datetime.now()

    def fill_rezult(self):

        for curr_category in self.categories:
            category_name = curr_category['data']['title']
            cat_route = curr_category['data']['action']['data']['path']
            response = get_fetch(URL_SERV + cat_route, PARAMS)
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
        self.df = make_DataFrame(self.rezult)

    def __upload_to_excel(self):
        file_name = f'data_rezult/Глово - {CATEGORY} {self.date_time_now.strftime("%d_%m_%Y")}.xlsx'
        upload_to_excel(self.df, file_name)

    def start(self):
        self.fill_rezult()
        self.__make_DataFrame()
        self.__upload_to_excel()


def main():

    glovo = GlovoApiScraper()
    glovo.start()


if __name__ == '__main__':
    main()

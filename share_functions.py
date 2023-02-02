
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
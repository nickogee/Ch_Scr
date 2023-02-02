
# -------------- изменяемое -- начало------
PARAMS = {
  "headers": {
    "accept": "application/json, text/plain, */*",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-type": "application/json",
    "sec-ch-ua": "\"Not_A Brand\";v=\"99\", \"Google Chrome\";v=\"109\", \"Chromium\";v=\"109\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "cookie": "PHPSESSID=d46ce89b5b7868b447883e084eebe8ca; arbuz-kz_jwt_v3=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0MGJlNmYxYy0wNzU5LTQ5MGYtOGViOC1mNGJjMDExOWVmNTMiLCJpc3MiOiJ5QjlHakV6WjlURDlET2VtbDJTMGpjakEwdXpSNTYweCIsImlhdCI6MTY3NDE1NzE0MCwiZXhwIjo0ODI3NzU3MTQwLCJjb25zdW1lciI6eyJpZCI6ImU1YzRlYTA1LWY4ZTgtNDJiZC1iMDJhLWNmMzNlODAyZjA5NiIsIm5hbWUiOiJhcmJ1ei1rei53ZWIuZGVza3RvcCJ9LCJjaWQiOm51bGx9.v87ho4cxMbZLDWkjvA1O4cAufTnZ725ABWXQgvtLG4A; _gcl_au=1.1.76030346.1674157142; mindboxDeviceUUID=ddaa7e3d-c9bf-4ee1-9c33-6ff36659f8c9; directCrm-session=%7B%22deviceGuid%22%3A%22ddaa7e3d-c9bf-4ee1-9c33-6ff36659f8c9%22%7D; _ym_uid=1674157142219607668; _ym_d=1674157142; _fbp=fb.1.1674157142556.425399229; _tt_enable_cookie=1; _ttp=8Pmwly3Fovrs02Gj5TGCcAW_5VT; __stripe_mid=db4fa26b-7c0a-4252-a49a-d3b315259b9a32f571; _gcl_aw=GCL.1674622920.CjwKCAiAoL6eBhA3EiwAXDom5iYQi-We3lkSkFj7g6reBOCPRiZo5DuW7HG8ftR13JvEIixrvV-TvRoCJjEQAvD_BwE; _gac_UA-109863448-1=1.1674622921.CjwKCAiAoL6eBhA3EiwAXDom5iYQi-We3lkSkFj7g6reBOCPRiZo5DuW7HG8ftR13JvEIixrvV-TvRoCJjEQAvD_BwE; _gid=GA1.2.222705349.1675343130; _ym_isad=2; _ym_visorc=w; __stripe_sid=732d5f05-23e1-455e-a67b-a15c3ed11d9a114ac9; _dc_gtm_UA-109863448-1=1; _ga=GA1.1.1826377655.1674157142; _ga_0X26SLE0CQ=GS1.1.1675355579.24.1.1675356879.24.0.0",
    "Referer": "https://arbuz.kz/ru/almaty/catalog/cat/225244-rastitelnye_produkty",
    "Referrer-Policy": "strict-origin-when-cross-origin"
  },
  "body": None,
  "method": "GET"
}

CATALOG_NUMBER = 225244
# -------------- изменяемое -- конец------

PAGE = '@PAGE@'
SUB_CATALOG = '@SUBCATALOG@'
URL_FST = f"https://arbuz.kz/api/v1/shop/catalog/{SUB_CATALOG}?&limit=32"
URL_NXT = f"https://arbuz.kz/api/v1/shop/catalog/{SUB_CATALOG}?page={PAGE}&limit=32"

###############

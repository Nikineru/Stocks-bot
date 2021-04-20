import requests
import fake_useragent

from lxml.html import fromstring
from random import randint

def GetStockPrice(Stock_id: int, search_date: str):
    params = {
        "curr_id": Stock_id,
        "smlID": str(randint(1000000, 99999999)),
        "header": 'AAPL Historical Data',
        "st_date": search_date,
        "end_date": search_date,
        "interval_sec": 'Daily',
        "sort_col": "date",
        "sort_ord": "DESC",
        "action": "historical_data"
    }

    head = {
        "User-Agent": fake_useragent.UserAgent().random,
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }

    URL = "https://www.investing.com/instruments/HistoricalDataAjax"
    Period_Data = requests.post(URL, headers=head, data=params)

    if Period_Data.status_code != 200:
        print(f"Не удалось подключиться, код - {Period_Data.status_code}")
        return -1
    
    root_ = fromstring(Period_Data.text)
    path_ = root_.xpath(".//table[@id='curr_table']/tbody/tr")

    if path_[0].xpath(".//td")[0].text_content() == 'No results found':
        print("Информаци не найдена...")
        return -1

    return float(path_[0].xpath(".//td")[1].get('data-real-value'))

print(GetStockPrice(6408, '03/23/2021'))
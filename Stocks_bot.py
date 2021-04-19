import requests
import re
import gzip
from io import StringIO
from time import time
from bs4 import BeautifulSoup

user = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1"
session = requests.Session()


def GetStockData(Stock_id, search_date):
    params = {
            "curr_id": Stock_id,
            "smlID": 1159963,
            "header": 'AAPL Historical Data', #TODO
            'st_date': search_date,
            'end_date': search_date,
            "interval_sec": 'Daily',
            "sort_col": "date",
            "sort_ord": "DESC",
            "action": "historical_data"
        }

    head = {
        "User-Agent": user,
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    URL = "https://www.investing.com/instruments/HistoricalDataAjax"
    Period_Data = requests.post(URL, headers=head, data=params)

    buf = StringIO(str(Period_Data.content))
    f = gzip.GzipFile(fileobj=buf)
    f.read()

    #soup = BeautifulSoup(Period_Data.content, 'html.parser')
    #print(Period_Data.content)
    #StocksQuote = soup.find("td", { "class" : re.compile(r"^(greenFont|redFont)$") })
    #return StocksQuote['data-real-value'] if StocksQuote != None else None


GetStockData(6408, '03/19/2021')
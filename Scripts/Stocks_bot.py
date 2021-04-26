import requests
import fake_useragent
import time
import numpy as np

import concurrent.futures
from lxml.html import fromstring
from random import randint

from Config import Config
from TableWorker import TableWorker
from StockFinder import DataBaseWorker

class InvestBot:
    def __init__(self):
        self.User = fake_useragent.UserAgent().random
        self.Config = Config()
        self.TableWorker = TableWorker(self.Config)
        self.DB_Worker = DataBaseWorker()

    def GetStockPrice(self, Stock_id: int, search_date: str):
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
            "User-Agent": self.User,
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

        if len(path_) < 1 or path_[0].xpath(".//td")[0].text_content() == 'No results found':
            print("Информаци не найдена...")
            return -1

        price = path_[0].xpath(".//td")[1].get('data-real-value')
        price = price.replace(',', '')
        return float(price)

    def GetStockId(self, ticker:str):
        URL = 'https://www.investing.com/search/?q=' + ticker

        head = {
            "User-Agent": self.User
        }

        response = requests.get(URL, headers=head)

        if response.status_code != 200:
            print(f"Не удалось подключиться, код - {Period_Data.status_code}")
            return -1

        root_ = fromstring(response.text)
        path_ = root_.xpath(".//div[@class='js-inner-all-results-quotes-wrapper newResultsContainer quatesTable']/script")

        if len(path_) < 1:
            print(f"По такому тикеру, нет данных - {ticker}")
            return -1

        data = path_[0].text
        data = data[data.index('pairId') + 8:]
        return int(data[:data.index(',')])

def GetStcoksPrice(tickers: list, finder:InvestBot):
    Result = list()

    for ticker in tickers:
        id_ = finder.DB_Worker.FindSecurityID(country=ticker[1], ticker=ticker[0])
    
        if id_ == None:
            id_ = finder.GetStockId(ticker[0])
    
        if id_ != -1:
            price = finder.GetStockPrice(id_, '03/23/2021')
            print(f"{ticker[0]} - {price}")
            Result.append((ticker[0], price))
    
    return Result

def main():
    Bot = InvestBot()
    start = time.time()
    ThreadsCount = 6

    Tickers = np.array_split(Bot.TableWorker.Tickers, ThreadsCount)
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        Threads = list()

        for i in range(ThreadsCount):
            Threads.append(executor.submit(GetStcoksPrice, Tickers[i], Bot))

        return_value = [thread.result() for thread in Threads]
        print(return_value)

    print(time.time() - start)
    #Bot.Config.SaveConfig()

if __name__ == '__main__':
    main()
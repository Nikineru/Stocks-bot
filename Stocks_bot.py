import requests, fake_useragent, openpyxl
import re
import datetime, os
import ID_founder
from ID_founder import program_path
import pickle 
from time import time
from bs4 import BeautifulSoup

user = fake_useragent.UserAgent().random
session = requests.Session()


days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']

def GetStockData(Stock_id, search_date):
    params = {
            "curr_id": Stock_id,
            "smlID": 0,
            "header": f'Прошлые данные - {ticker}',
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

    soup = BeautifulSoup(Period_Data.content, 'html.parser')
    StocksQuote = soup.find("td", { "class" : re.compile(r"^(greenFont|redFont)$") })

    return StocksQuote['data-real-value'] if StocksQuote != None else None

def GetStockCountry(Ticker):
    URL = f'https://ru.investing.com/search/?q={Ticker}'

    header = {
        'user-agent': user
    }

    response = requests.get(URL, headers=header)
    soup = BeautifulSoup(response.content, 'html.parser')

    FirstStock = soup.find('a', class_ = 'js-inner-all-results-quote-item row')
    if FirstStock != None:
        URL = 'https://www.investing.com{}'.format(FirstStock['href'])
    else:
        print("I can`t frind stock data")

    response = requests.get(URL, headers=header)
    soup = BeautifulSoup(response.content, 'html.parser')
    country_data = soup.find_all('a', class_='font-bold text-secondary hover:underline')
    return country_data[2].text.lower()

def GetAmericanDate(date):
    return f"{GetStringFromDay(date.month)}/{GetStringFromDay(date.day)}/{GetStringFromDay(date.year)}"

def GetStringFromDay(value):
    return value if value >= 10 else f"0{value}"

def IsTicker(value:str):
    value = value.replace(' ', '')

    if re.search(r'[^A-Z]', value):
        return False
    else:
        return True

def GetInputPosition(sheet, path="Data\\InputData.txt"):
    DatePos = None
    TickerPos = None
    path = program_path + path

    if os.path.getsize(path) > 0:
        with open(path,'rb') as inp:
            load_data = pickle.load(inp)
            _date = (0, 0)
            _ticker = (0, 0)

            if len(load_data) > 0:
                _date = load_data[0]
                _ticker = load_data[1]
                
                if type(sheet.cell(row=_date[0], column=_date[1]).value) == datetime.datetime:
                    DatePos = _date

                if IsTicker(str(sheet.cell(row=_ticker[0], column=_ticker[1]).value)):
                    TickerPos = _ticker
    else:
        print("Тут ничего нет ;/")

    if DatePos == None or TickerPos == None:
        for row in sheet.rows:
            for cell in row:
                if TickerPos == None and IsTicker(str(cell.value)):
                    TickerPos = (cell.row, cell.column)

                if DatePos == None and type(cell.value) == datetime.datetime:
                    DatePos = (cell.row, cell.column)
                
                if TickerPos != None and DatePos != None:
                    break

        with open(path,'wb') as out:
            save_data = [DatePos, TickerPos]
            pickle.dump(save_data,out)

    return (DatePos, TickerPos)

start_time = time()
path_to_TablePath = (program_path + 'Data\\TablePath.txt').replace('\\', '/')
path = ''

if os.path.getsize(path_to_TablePath) > 0:
    with open(path_to_TablePath,'rb') as inp:
            path = pickle.load(inp)
if len(path) < 1:
    path = input("Введите путь до таблицы: ")
    path = path.replace('\"', '')

    if len(path) > 0:
        with open(path_to_TablePath,'wb') as out:
                pickle.dump(path, out)
try:
    book = openpyxl.load_workbook(path) 
    sheet = book.active
except:
    f = open(path_to_TablePath, 'w')
    f.close()
    exit('Введите корректный путь')

Tickers = list()
RowOfLastTicker = 1

Input = GetInputPosition(sheet)
for row in sheet.iter_rows(min_row=Input[1][0], max_col=1):
    for cell in row:
        value = str(cell.value)
        if value.isupper() and value.isdigit() == False:
            country = sheet.cell(row=cell.row, column=cell.column + 1)
            Tickers.append((cell, country))
            RowOfLastTicker += 1

Date = sheet.cell(row=Input[0][0], column=Input[0][1]).value
DayOfWeek = Date.weekday()

if DayOfWeek > 4:
    print(f"В {days[Date.weekday()]} торги не ведутся, введите другой день!")
    exit()

StartDate = GetAmericanDate(Date)
if Date > datetime.datetime.now():
    print("Введите корректную дату")
    exit()

EndDate = StartDate
print(f"Я буду работать с данными тикерами: {', '.join([i[0].value for i in Tickers])}")
print(f"Данные будут получены на: {Date}\n")

for ticker_data in Tickers:
    ticker = ticker_data[0]
    country = ticker_data[1]

    if country.value == None:
        country.value = GetStockCountry(ticker.value)
    
    StockID = ID_founder.GetStockData(ticker=ticker.value, country=country.value)
    Quote = GetStockData(StockID, StartDate)

    if Quote == None:
        Quote = '-'

    sheet.cell(row=ticker.row, column=ticker.column + 2).value = Quote
    print(f"Я получил акцию с тикером {ticker.value}, её котировка - {Quote}")

try:
    book.save(path)
    print('Я выполнил свою работу за - {:0.2f} секунд!'.format(time() - start_time))
    os.startfile(path)
except:
    print("Закройте numbers и перезапустите программу")
import requests
import fake_useragent
import openpyxl
import re
import datetime
from bs4 import BeautifulSoup


def GetStockData(ticker, start_date, end_date):
    StockQuotes = list()
    Dates = list()
    ExtraInfo = list()
    buffer = list()

    session = requests.Session()
    URL = f'https://ru.investing.com/search/?q={ticker}'
    user = fake_useragent.UserAgent().random

    header = {
        'user-agent': user
    }

    response = requests.get(URL, headers=header)
    soup = BeautifulSoup(response.content, 'html.parser')
    FirstStock = soup.find('a', class_ = 'js-inner-all-results-quote-item row')
    URL = 'https://ru.investing.com{}-historical-data'.format(FirstStock['href'])

    response = requests.get(URL, headers=header)
    soup = BeautifulSoup(response.content, 'html.parser')
    CurretPrice = soup.find('span', id = 'last_last')

    Stock_id = soup.find('div', class_ = 'headBtnWrapper float_lang_base_2 js-add-alert-widget')['data-pair-id']
        
    params = {
            "curr_id": Stock_id,
            "smlID": 0,
            "header": f'Прошлые данные - {ticker}',
            'st_date': StartDate,
            'end_date': EndDate,
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
    StocksData = soup.findAll('td')


    def AddQuote(value):
        nonlocal buffer
        nonlocal StockQuotes

        buffer.append(i.text)

        if len(buffer) >= 6:
            StockQuotes.append(buffer)
            buffer = list()

    for i in StocksData:
        if i.has_attr('class'):
            stock_class = ' '.join(i['class'])
            
            if stock_class == 'first left bold noWrap':
                Dates.append(i.text)

            elif stock_class == 'noBold noWrap left first' or stock_class == 'noWrap':
                ExtraInfo.append(i.text)

            else:
                AddQuote(i.text)

        else:
            AddQuote(i.text)

    return (StockQuotes, Dates, ExtraInfo)

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

def GetInputPosition(sheet, path=r"C:\Users\isbud\OneDrive\Рабочий стол\Stocks-bot\InputData.txt"):
    DatePos = None
    TickerPos = None
    
    File = open(path, 'r')

    lines = File.readlines()
    _date = [int(i) for i in lines[0].split()]
    _ticker = [int(i) for i in lines[1].split()]
    
    if type(sheet.cell(row=_date[0], column=_date[1]).value) == datetime.datetime:
        DatePos = tuple(_date)

    if IsTicker(str(sheet.cell(row=_ticker[0], column=_ticker[1]).value)):
        TickerPos = tuple(_ticker)

    File.close()

    if DatePos == None or TickerPos == None:
        for row in sheet.rows:
            for cell in row:
                if TickerPos == None and IsTicker(str(cell.value)):
                    TickerPos = (cell.row, cell.column)

                if DatePos == None and type(cell.value) == datetime.datetime:
                    DatePos = (cell.row, cell.column)
                
                if TickerPos != None and DatePos != None:
                    break
    
        File = open(path, 'w')
        date = f"{DatePos[0]} {DatePos[1]}"
        ticker = f"{TickerPos[0]} {TickerPos[1]}"

        File.write(f"{date}\n{ticker}")
        File.close()

    return (DatePos, TickerPos)

path = r"C:\Users\isbud\OneDrive\Рабочий стол\Stocks-bot\Акции.xlsx"
book = openpyxl.load_workbook(path) 
sheet = book.active

Tickers = list()
RowOfLastTicker = 1

Input = GetInputPosition(sheet)

for row in sheet.iter_rows(min_row=Input[1][0], max_col=1):
    for cell in row:
        value = str(cell.value)
        if value.isupper() and value.isdigit() == False:
            Tickers.append(cell)
            RowOfLastTicker += 1

StartDate = GetAmericanDate(sheet.cell(row=Input[0][0], column=Input[0][1]).value)
EndDate = StartDate
print(StartDate, EndDate)
print([i.value for i in Tickers])

for ticker in Tickers:
    Data = GetStockData(ticker.value, StartDate, EndDate)
    WasBidding = False
    curret_data_index = 0


    if len(Data[0]):
        print(ticker.value)
        print(f"Ценна - {Data[0]}")
        WasBidding = True

    for row in sheet.iter_rows(min_row=ticker.row, max_row=ticker.row, min_col=2, max_col=ticker.column + 6):
        for cell in row:
            if WasBidding:
                sheet.cell(row=cell.row, column=cell.column).value = Data[0][0][curret_data_index]
            else:
                sheet.cell(row=cell.row, column=cell.column).value = "-"
            curret_data_index += 1
        curret_data_index = 0
book.save(path)
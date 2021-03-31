import requests
import fake_useragent
import openpyxl
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

    #workbook = xlsxwriter.Workbook(r"C:\Users\isbud\OneDrive\Рабочий стол\Акции.xlsx")
    #worksheet = workbook.add_worksheet()

    #for i in range(len(Dates)):
    #    worksheet.write(i, 0, Dates[i])
    #    for j in range(6):
    #        worksheet.write(i, 1 + j, StockQuotes[i][j])

    #workbook.close()

    return (StockQuotes, Dates, ExtraInfo)

def GetAmericanDate(date):
    return f"{GetStringFromDay(date.month)}/{GetStringFromDay(date.day)}/{GetStringFromDay(date.year)}"

def GetStringFromDay(value):
    return value if value > 10 else f"0{value}"

path = r"C:\Users\isbud\OneDrive\Рабочий стол\Акции.xlsx"
book = openpyxl.load_workbook(path) 
sheet = book.active

Tickers = list()

StartDate = GetAmericanDate(sheet["A5"].value)
EndDate = GetAmericanDate(sheet["B5"].value)

for row in sheet.iter_rows(min_row=2, max_row=4, max_col=1):
    for cell in row:
        Tickers.append(cell)

for ticker in Tickers:
    Data = GetStockData(ticker.value, StartDate, EndDate)
    print(ticker.value)
    print(f"Ценна - {Data[0]}")
    
    for row in sheet.iter_rows(min_row=2, max_row=4, min_col=2, max_col=ticker.column + 7):
        for cell in row:
            cell = "Test"
book.save(path)
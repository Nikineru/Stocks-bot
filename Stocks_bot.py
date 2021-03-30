import requests
import fake_useragent
import xlsxwriter
from bs4 import BeautifulSoup

session = requests.Session()
ticker = input("Тикер: ")
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
print(f"Текущая цена - {CurretPrice.text}")

Stock_id = soup.find('div', class_ = 'headBtnWrapper float_lang_base_2 js-add-alert-widget')['data-pair-id']
    
params = {
        "curr_id": Stock_id,
        "smlID": 0,
        "header": f'Прошлые данные - {ticker}',
        'st_date': '03/01/2010',
        'end_date': '03/03/2021',
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
StockQuotes = list()
Dates = list()
ExtraInfo = list()
buffer = list()

for i in StocksData:
    if i.has_attr('class'):
        stock_class = ' '.join(i['class'])
        
        if stock_class == 'first left bold noWrap':
            Dates.append(i.text)

        elif stock_class == 'noBold noWrap left first' or stock_class == 'noWrap':
            ExtraInfo.append(i.text)

        else:
            value = i.text.replace('%' , '')
            value = value.replace('M' , '')

            buffer.append(float(value))

            if len(buffer) >= 6:
                StockQuotes.append(buffer)
                buffer = list()
    else:
        value = i.text.replace('%' , '')
        value = value.replace('M' , '')
        buffer.append(float(value))

        if len(buffer) >= 6:
            StockQuotes.append(buffer)
            buffer = list()

workbook = xlsxwriter.Workbook(r"C:\Users\isbud\OneDrive\Рабочий стол\Акции.xlsx")
worksheet = workbook.add_worksheet()

for i in range(len(Dates)):
    worksheet.write(i, 0, Dates[i])
    for j in range(6):
        worksheet.write(i, 1 + j, StockQuotes[i][j])

# Тип диаграммы
chart = workbook.add_chart({'type': 'line'})
 
# Строим по нашим данным
chart.add_series({'values': f'=Sheet1!B1:B{len(Dates)}'})
 
worksheet.insert_chart('J1', chart)
workbook.close()
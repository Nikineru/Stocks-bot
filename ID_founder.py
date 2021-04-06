import pickle
import os

program_path = os.path.abspath(__file__).replace('\\', '/')
program_path = program_path[:program_path.rindex('/') + 1]
StocksPath = program_path + "Data/Stocks_data.txt"
StockData = dict()

def Get_JSON_FromText():
    pass
    with open(r"C:\Users\isbud\OneDrive\Рабочий стол\Stocks-bot\Stocks.txt", 'r', encoding='utf-8') as File:
        Lines = File.readlines()
        LastCountry = ''
        buffer = list()

        for line_index in range(1, len(Lines)):
            line = Lines[line_index].split(',')

            Country = line[0]
            Ticker = line[-1].replace('\n', '')
            Ticker = Ticker.replace(' ', '')
            Stock_Id = line[-3]

            if LastCountry != '' and LastCountry != Country:
                StockData[Country] = buffer
                buffer = list()
                LastCountry = Country
            
            LastCountry = Country
            StockData[Country] = buffer
            buffer.append((Ticker, Stock_Id))

def LoadStocks():
    global StockData

    with open(StocksPath,'rb') as inp:
        StockData = pickle.load(inp)

def GetStockData(country, ticker):
    result = list(filter(lambda x: x[0] == ticker, StockData[country]))
    return result[0][1] if len(result) > 0 else -1

LoadStocks()
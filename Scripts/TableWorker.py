import openpyxl
import os
import re

from Config import Config

class TableWorker:
    def __new__(cls, config, *args, **kwargs):
        if not hasattr(cls, 'instance') and config != None:
            cls.instance = super(TableWorker, cls).__new__(cls, *args, **kwargs)
        return cls.instance
    
    def __init__(self, config, *args, **kwargs):
        self.Path = config.TablePath
        self.Config = config

        while os.path.exists(self.Path) is False:
            self.Path = input("Введите путь до таблицы: ").replace('\"', '')
            config.TablePath = self.Path

        self.Book = openpyxl.load_workbook(self.Path)
        self.Sheet = self.Book.active
        self.Tickers = self.GetTickers()
    
    def GetTickers(self):
        TickerPos = self.Config.TickersStartPos
        Ticker = self.Sheet.cell(row=TickerPos[0], column=TickerPos[1]).value
        if Ticker == None or self.IsTicker(Ticker):
            for row in self.Sheet.rows:
                for cell in row:
                    if cell != None and self.IsTicker(str(cell.value)):
                        TickerPos = (cell.row, cell.column)
                        break
        print(TickerPos)
    
    def IsTicker(self, value:str):
        return re.search(r'[^A-Z_p]', value) == None

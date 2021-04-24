import openpyxl
import os
import re

from datetime import datetime
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
        TableData = self.GetTickersAndDate()
        self.Tickers = TableData[0]
        self.Date = TableData[1]
        print(self.Date, self.Tickers)
    
    def GetTickersAndDate(self):
        TickerPos = list(self.Config.TickersStartPos)
        Ticker = None

        Date = None
        Result = list()
        FoundTicker = True
        FoundDate = True

        if len(TickerPos) > 0:
            Ticker = self.Sheet.cell(row=TickerPos[0], column=TickerPos[1]).value
        
        if Ticker == None or self.IsTicker(Ticker):
            FoundTicker = False

        for row in self.Sheet.columns:
            for cell in row:
                if cell != None:
                    if FoundTicker is False and self.IsTicker(str(cell.value)):
                        TickerPos = [cell.row, cell.column]
                        self.Config.TickersStartPos = TickerPos
                        FoundTicker = True

                    if type(cell.value) is datetime:
                        Date = cell.value
                        self.Config.DatePos = [cell.row, cell.column]
                        if FoundTicker:
                            break
        
        while True:
            try:
                cell = self.Sheet.cell(row=TickerPos[0], column=TickerPos[1]).value

                if cell != None and self.IsTicker(cell):
                    if '_P' in cell:
                        cell = cell[:cell.index('_P')] + '_p'
                        
                    Result.append((cell, self.Sheet.cell(row=TickerPos[0], column=TickerPos[1] + 1).value))

                elif cell != None:
                    break
                TickerPos[0] += 1
            except:
                break
        
        return (Result, Date)
    
    def IsTicker(self, value:str):
        return re.search(r'[^A-Z0-9_p]', value) == None
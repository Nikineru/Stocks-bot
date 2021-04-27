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
        self.EndTickerPos = list()
        TableData = self.GetTickersAndDate()
        self.Tickers = TableData[0]
        self.Date = TableData[1]
        self.Date = f"{self.Date.month}/{self.Date.day}/{self.Date.year}"
        print(self.EndTickerPos)
        print(f"Акции - {', '.join([tic[0] for tic in self.Tickers])} - за {self.Date}\n")
    
    def GetTickersAndDate(self):
        TickerPos = list(self.Config.TickersStartPos)
        DatePos = list(self.Config.DatePos)
        Ticker = None

        Date = None
        Result = list()
        FoundTicker = True
        FoundDate = True

        if TableWorker.IsСoordinates(TickerPos):
            Ticker = self.Sheet.cell(row=TickerPos[0], column=TickerPos[1]).value
        
        if Ticker == None or TableWorker.IsTicker(Ticker) == False:
            FoundTicker = False

        if TableWorker.IsСoordinates(DatePos):
            Date = self.Sheet.cell(row=DatePos[0], column=DatePos[1]).value

        if Date == None or type(Date) != datetime:
            FoundDate = False
            
        print(FoundTicker, FoundDate)
        for row in self.Sheet.columns:
            for cell in row:
                if cell != None:
                    if FoundTicker is False and TableWorker.IsTicker(str(cell.value)):
                        TickerPos = [cell.row, cell.column]
                        self.Config.TickersStartPos = TickerPos[:]
                        FoundTicker = True

                    if type(cell.value) is datetime:
                        Date = cell.value
                        self.Config.DatePos = [cell.row, cell.column]
                        if FoundTicker:
                            break
        EmptyCellsCount = 0
        while True:
            try:
                cell = self.Sheet.cell(row=TickerPos[0], column=TickerPos[1]).value

                if cell != None and TableWorker.IsTicker(cell):
                    if '_P' in cell:
                        cell = cell[:cell.index('_P')] + '_p'
                    
                    country = self.Sheet.cell(row=TickerPos[0], column=TickerPos[1] + 1).value
                    id_ = self.Sheet.cell(row=TickerPos[0], column=TickerPos[1] + 3).value
                    Result.append((cell, country, id_))
                    EmptyCellsCount = 0
                else:
                    EmptyCellsCount += 1
                
                if EmptyCellsCount > 1:
                    break
                    
                TickerPos[0] += 1
            except:
                break
        self.EndTickerPos = TickerPos[:]
        return (Result, Date)
    
    def WriteTickersPrice(self, data:dict):
        column = self.EndTickerPos[1]
        for row in range(1, self.EndTickerPos[0]):
            cell = self.Sheet.cell(row=row, column=column)

            if cell is not None and cell.value is not None:
                ticker = cell.value

                if '_P' in ticker:
                    ticker = ticker[:ticker.index('_P')] + '_p'
                if ticker in data.keys():
                    self.Sheet.cell(row=row, column=column + 2).value = data[ticker][0]
                    self.Sheet.cell(row=row, column=column + 3).value = data[ticker][1]

        self.Book.save(self.Config.TablePath)
        print("Таблица успешно изменена")

    @staticmethod
    def IsСoordinates(value:list):
        FirstCond = len(value) > 1

        if FirstCond is False:
            return False

        SecondCond = value[0] > 0 and value[1] > 0
        ThirdCond = value[0] < 1048576 and value[1] < 1048576

        return SecondCond and ThirdCond

    @staticmethod
    def IsTicker(value:str):
        return re.search(r'[^A-Z0-9_p]', value) == None
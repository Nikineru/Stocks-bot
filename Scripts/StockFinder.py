import csv
from pathlib import Path
import pandas as pd
from Config import Config

class Security:
    def __init__(self, path):
        self.Path = path
        self.Data = self.LoadCSV()

    def LoadCSV(self):
        RealPath = Config.GetProgramPath()
        RealPath = '/'.join(RealPath) + f"/Resources/{self.Path}"
        
        Data = pd.read_csv(RealPath, keep_default_na=False)
        return Data

class DataBaseWorker:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DataBaseWorker, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.Securities = [
            Security('stocks.csv'),
            Security('etfs.csv')]
    
    def FindSecurityByIndex(self, country, ticker, index):
        stocks = self.Securities[index].Data
        result = list(stocks[(stocks['country'] == country) & (stocks['symbol'] == ticker)]['id'])

        if len(result) > 0:
            return result[0]
        else:
            return -1

    def FindSecurityID(self, country, ticker):
        for i in range(len(self.Securities)):
            result = self.FindSecurityByIndex(country, ticker, i)

            if result != -1:
                return result
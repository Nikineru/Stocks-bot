import csv
from pathlib import Path

class Security:
    def __init__(self, path):
        self.Path = path
        self.Data = self.LoadCSV()

    def LoadCSV(self):
        RealPath = str(Path(__file__).parent.absolute()) + f"\\Resources\\{self.Path}"
        File = open(RealPath, encoding='utf-8')

        Data = list(csv.reader(File, delimiter = ","))
        File.close()
        return Data

class DataBaseWorker:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DataBaseWorker, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.Securities = [
            Security('stocks.csv'),
            Security('bonds.csv'),
            Security('etfs.csv')]
    
    def FindSecurityByIndex(self, country, ticker, index):
        if index > -1 and index < len(self.Securities):
            for stock in self.Securities[index].Data:
                if stock[0] == country and stock[-1] == ticker:
                    return stock
        return None

    def FindSecurityData(self, country, ticker, security_index=-1):
        if security_index == -1:
            for index in range(len(self.Securities)):
                stock = self.FindSecurityByIndex(country, ticker, index)

                if stock != None:
                    return stock
        else:
            return self.FindSecurityByIndex(country, ticker, security_index)
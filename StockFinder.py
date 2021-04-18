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

class Stock(Security):
    def __init__(self):
        super().__init__('stocks.csv')

class Bond(Security):
    def __init__(self):
        super().__init__('bonds.csv')

class ETF(Security):
    def __init__(self):
        super().__init__('etfs.csv')


class DataBaseWorker:
    def __init__(self):
        self.Stocks = Stock()
        self.Bonds = Bond()
        self.Etfs = ETF()
    
    def SecurityDataOfType(self, security_type, country, name):
        pass



Worker = DataBaseWorker()
print(Worker.Etfs.Data)
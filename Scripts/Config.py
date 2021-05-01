import json
import psutil
import os

class Config:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)
        return cls.instance

    def __init__(self, **kwargs):
        self.CPU_COUNT = psutil.cpu_count()
        self.StocksId_cash = dict()
        self.TablePath = ''
        self.TickersStartPos = tuple()
        self.DatePos = tuple()

        DirectPath = os.path.dirname(os.path.realpath(__file__)).split('\\')
        self.ConfigPath = DirectPath[:-1]
        self.ConfigPath = '/'.join(self.ConfigPath) + f"/Resources/Config.json"
        
        self.TickersPoses = list()
        with open('/'.join(DirectPath[:-1]) + "/Resources/CurretStocks.txt", 'r') as file:
            for position in [list(i.rstrip().replace('\"', '').split(', ')) for i in file.readlines()]:
                self.TickersPoses.append([int(i) for i in position])

        self.LoadConfig()
        print(self.TickersPoses)

    def LoadConfig(self):
        if os.path.exists(self.ConfigPath) is False:
            return
        
        with open(self.ConfigPath, 'rb') as f:
            try:
                data = json.load(f)
                self.TickersStartPos = data['TickersStartPos']
                self.DatePos = data['DatePos']
                self.TablePath = data['TablePath']
                self.StocksId_cash = data['StocksId_cash']
                print("Конфиг успешно загружен")
            except:
                print("Произошла ошибка при загрузке")

    def SaveConfig(self):
        if os.path.exists(self.ConfigPath):
            with open(self.ConfigPath, 'w') as f:
                data = json.dumps(self, cls=ConfigEncoder)
                f.write(data)
                print("Кофиг успешно сохранён")
        else:
            print(f"По такоему пути нет файла - {self.ConfigPath}")

class ConfigEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Config):
            data = obj.__dict__
            data.pop('ConfigPath', None)
            return data
        return json.JSONEncoder.default(self, obj)
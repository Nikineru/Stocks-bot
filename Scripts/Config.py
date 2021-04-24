import json
import os

class Config:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)
        return cls.instance

    def __init__(self, **kwargs):
        self.TablePath = ''
        self.TickersStartPos = tuple()
        self.DatePos = tuple()

        self.ConfigPath = os.path.dirname(os.path.realpath(__file__)).split('\\')
        self.ConfigPath = self.ConfigPath[:-1]
        self.ConfigPath = '/'.join(self.ConfigPath) + f"/Resources/Config.json"
        
        self.LoadConfig()

    def LoadConfig(self):
        if os.path.exists(self.ConfigPath) is False:
            return
        
        with open(self.ConfigPath, 'rb') as f:
            try:
                data = json.load(f)
                self.TickersStartPos = data['TickersStartPos']
                self.DatePos = data['DatePos']
                self.TablePath = data['TablePath']
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
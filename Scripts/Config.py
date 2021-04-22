import pickle
import os
from pathlib import Path

class Config:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.TablePath = ''
        self.TickersStartPos = tuple()
        self.DatePos = tuple()

        self.ConfigPath = str(Path(__file__).parent.absolute()).split('\\')
        self.ConfigPath = self.ConfigPath[:-1]
        self.ConfigPath = '/'.join(self.ConfigPath) + f"/Resources/Config.txt"

        self.LoadConfig()

    def LoadConfig(self):
        if os.path.exists(self.ConfigPath) is False:
            return
        
        with open(self.ConfigPath, 'rb') as f:
            try:
                data = pickle.load(f)
                self.TickersStartPos = data.TickersStartPos
                self.DatePos = data.DatePos
                self.TablePath = data.TablePath
                print("Конфиг успешно загружен")
            except:
                print("Произошла ошибка при загрузке")

    def SaveConfig(self):
        with open(self.ConfigPath, 'wb') as f:
            pickle.dump(self, f)
            print("Кофиг успешно сохранён")
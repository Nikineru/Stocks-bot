import pickle
from pathlib import Path

TablePath = ''
TickersStartPos = tuple()
DatePos = tuple()

ConfigPath = str(Path(__file__).parent.absolute()).split('\\')
ConfigPath = ConfigPath[:-1]
ConfigPath = '/'.join(ConfigPath) + f"/Resources/Config"
print(ConfigPath)

def LoadConfig():
    pass

def SaveConfig():
    pass
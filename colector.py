import pandas as pd
from paths import path
import csv

class protocol_current_values():
    def __init__(self):
        self._df = pd.read_csv(path(file_name="Protocolo valores de corrente"), quoting=csv.QUOTE_NONE, sep = ";")
        self.__data_formatting()

        print(self._df.sample)

    def __data_formatting(self):
        self._df.columns = self._df.columns.str.replace(r'"', '')
        self._df['timerName']= self._df['timerName'].str.replace(r'"', '')

wellding = protocol_current_values()
        

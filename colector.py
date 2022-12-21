import pandas as pd
import numpy as np
from paths import path
import csv
import SQL_manipulation as SQL

class protocol_current_values():
    def __init__(self):
        self._df = pd.read_csv(path(file_name="Protocolo valores de corrente"), quoting=csv.QUOTE_NONE, sep = ";")
        self.__data_formatting()
        self._filtered_df = self._df

        self._list_name = self._df['timerName'].unique()

        self.__main()        

    def __data_formatting(self):
        self._df.columns = self._df.columns.str.replace(r'"', '')
        self._df['timerName']= self._df['timerName'].str.replace(r'"', '')
    
    def __main(self):
        for robot_name in self._list_name:
            last_date = SQL.get_last_time(robot_name)
            last_electrode_num = SQL.get_last_electrode_num(robot_name)
            
            #filters
            df_mask_date = self._df['dateTime'] > last_date
            positions_date = np.flatnonzero(df_mask_date)
            self._filtered_df = self._df.iloc[positions_date]

            df_mask_names = self._filtered_df['timerName'] == robot_name
            positions_names = np.flatnonzero(df_mask_names)
            self._filtered_df = self._filtered_df.iloc[positions_names]


            self.__check_electrode_change()
            
            print(self._filtered_df)
    
    def __check_electrode_change(self):
        #self._filtered_df.sort_values(by = 'dateTime') #Redundancy the data already comes in ascending order

        last_milling = SQL.get_last_milling()

        for index in self._filtered_df.index





wellding = protocol_current_values()
        

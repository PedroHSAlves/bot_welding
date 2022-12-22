import pandas as pd
import numpy as np
from paths import path
import csv
import SQL_manipulation as SQL

class protocol_current_values():
    def __init__(self):
        """
        """
        self._df = pd.read_csv(path(file_name="Protocolo valores de corrente"), quoting=csv.QUOTE_NONE, sep = ";")
        self.__data_formatting()
        self._filtered_df = self._df

        self._list_name = self._df['timerName'].unique()

        self.__main()        

    def __data_formatting(self):
        """
        """
        self._df.columns = self._df.columns.str.replace(r'"', '')
        self._df['timerName']= self._df['timerName'].str.replace(r'"', '')
    
    def __main(self):
        """
        """
        for robot_name in self._list_name:
            last_date = SQL.get_last_time(robot_name)
            self._last_electrode_num = SQL.get_last_electrode_num(robot_name)
            self._last_milling = SQL.get_last_milling(robot_name)
            
            #filters
            df_mask_date = self._df['dateTime'] > last_date
            positions_date = np.flatnonzero(df_mask_date)
            self._filtered_df = self._df.iloc[positions_date]

            df_mask_names = self._filtered_df['timerName'] == robot_name
            positions_names = np.flatnonzero(df_mask_names)
            self._filtered_df = self._filtered_df.iloc[positions_names]

            #self._filtered_df.sort_values(by ='dateTime')

            print("\nrobot name: ", robot_name,end='\n\n')#Debug print
            self.__check_electrode_change()
            
            #print(self._df['timerName'].value_counts()[robot_name])
            #print(self._filtered_df.shape)
    
    def __check_electrode_change(self):
        """
        """
        list_index = self._filtered_df.index
        tam_list_index = len(list_index)
        count = 1 
        points_applied = 0
        n_milling = 0

        for index in range(tam_list_index):
            # avoids looking in an index that does not exist. 
            if (count + 1) > tam_list_index:
                break
            count += 1

            if self._last_milling <= self._filtered_df['tipDressCounter'][self._filtered_df.index[0]] and index == 0:
                SQL.revemove_line_in_SQL()
                points_applied = SQL.get_last_point_applied
            
            if self._filtered_df['tipDressCounter'][list_index[index]] <= self._filtered_df['tipDressCounter'][list_index[index + 1]]:
                points_applied += 1
            else:
                n_milling = self._filtered_df['tipDressCounter'][list_index[index]]
                points_applied += 1
                self._last_electrode_num += 1
                #To MyphpAdmin
                print("Points applieds: ", points_applied)#Debug print

                points_applied = 0
                
                print("next milling: ", self._filtered_df['tipDressCounter'][list_index[index + 1]])#Debug print
                print("milling: ", n_milling)#Debug print
                print("electrode numer: ", self._last_electrode_num)#Debug print
                print("electrode replacement", end="\n\n")#Debug print


        





wellding = protocol_current_values()
        

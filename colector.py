import pandas as pd
import numpy as np
from paths import path_manipulation
import csv
from SQL_manipulation import sql_manipulation

import time

class electrode_count():
    def __init__(self):
        self._path = path_manipulation()
        self._sql = sql_manipulation()

        for path_index in range(self._path.len_paths):
            self._line_name = self._path.get_line_name(path_index)

            try:
                self._df = pd.read_csv(self._path.file_path(path_index), quoting=csv.QUOTE_NONE, sep = ";")
            except:
                TypeError("CSV reading failed")

            self.__data_formatting()
            self._filtered_df = self._df

            self._list_name = self._df['timerName'].unique()

            self.__main()
            self._path.move_file(path_index)        

    def __data_formatting(self):
        """
        Fixes formatting of columns imported from CSV.
        """
        self._df.columns = self._df.columns.str.replace(r'"', '')
        self._df['timerName']= self._df['timerName'].str.replace(r'"', '')
    
    def __main(self):
        """
        Applies the filter for each existing robot in the CSV file.
        """
        for robot_name in self._list_name:
            for tool in self.__get_electrode_no(robot_name):
                self._tool_name = f"{self._line_name}_{robot_name}_{tool}"
                self._last_date = self._sql.get_last_time(self._line_name,self._tool_name)
                self._last_milling_SQL = self._sql.get_last_milling(self._line_name,self._tool_name)
                
                #filters
                df_mask_date = self._df['dateTime'] > self._last_date
                positions_date = np.flatnonzero(df_mask_date)
                self._filtered_df = self._df.iloc[positions_date]

                df_mask_names = self._filtered_df['timerName'] == robot_name
                positions_names = np.flatnonzero(df_mask_names)
                self._filtered_df = self._filtered_df.iloc[positions_names]

                df_mask_names = self._filtered_df['electrodeNo'] == tool
                positions_names = np.flatnonzero(df_mask_names)
                self._filtered_df = self._filtered_df.iloc[positions_names]

                self.__check_electrode_change(robot_name,tool)

    def __get_electrode_no(self,robot_name: str):
        """
        Get all tools from the robot.
        """
        df_mask_date = self._df['timerName'] == robot_name
        positions_date = np.flatnonzero(df_mask_date)
        aux_df = self._df.iloc[positions_date]

        return aux_df['electrodeNo'].unique()

    def __get_last_electrode(self, tool,robot_name:str):
        """
        Gets the last electrode number of the tool, recorded in the database.
        """
        return  self._sql.get_last_electrode_num(self._line_name,robot_name,int(tool))
    
    def __check_electrode_change(self, robot_name: str, tool):
        """
        Counts how many weld spots have benn applied in each milling oporation.
        """
        electrode_no = tool
        list_index = self._filtered_df.index
        len_index = len(list_index)
        count = 1 
        points_applied = 0
        n_milling = 0
        
        ### DEBUG AREA
        # print("\nLine name: ",self._line_name)
        # print("Robot name: ", robot_name)
        # print("Tool: ", tool)
        
        self._last_electrode_num = self.__get_last_electrode(electrode_no,robot_name)

        for index in range(len_index):
            # avoids looking in an index that does not exist. 
            if (count + 1) > len_index:
                break
            count += 1

            if n_milling > self._filtered_df['tipDressCounter'][list_index[index + 1]] and points_applied != 0:
                points_applied += 1
                self._last_electrode_num += 1
                time = self._filtered_df['dateTime'][list_index[index]]
                time = time[:19]

                if self._last_date != time[:19]:
                    self._sql.post_data_wellding(self._line_name,self._last_electrode_num,robot_name,points_applied, n_milling,int(tool),self._tool_name,time)

                points_applied = 0
            else:
                n_milling = int(self._filtered_df['tipDressCounter'][list_index[index + 1]]) 
                points_applied += 1



print("running program...")#Debug print
wellding = electrode_count()
print("end code")#Debug print
        

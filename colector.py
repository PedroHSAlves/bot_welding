import pandas as pd
import numpy as np
from paths import path_manipulation
import csv
from SQL_manipulation import sql_manipulation

class protocol_current_values():
    def __init__(self):
        """
        """
        self._path = path_manipulation()
        self._line_name = self._path.get_line_name
        self._sql = sql_manipulation()

        try:
            self._df = pd.read_csv(self._path.name_file(file_name="Protocolo valores de corrente"), quoting=csv.QUOTE_NONE, sep = ";")
        except:
            TypeError("CSV reading failed")

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
            self._last_date = self._sql.get_last_time(self._line_name,robot_name)
            self._last_milling_SQL = self._sql.get_last_milling(self._line_name,robot_name)
            
            #filters
            df_mask_date = self._df['dateTime'] > self._last_date
            positions_date = np.flatnonzero(df_mask_date)
            self._filtered_df = self._df.iloc[positions_date]

            df_mask_names = self._filtered_df['timerName'] == robot_name
            positions_names = np.flatnonzero(df_mask_names)
            self._filtered_df = self._filtered_df.iloc[positions_names]

            self.__check_electrode_change(robot_name)

    def __get_last_electrode(self, tools,robot_name):
            _last_electrode_num = []
            for tool in tools:
                _last_electrode_num.append(self._sql.get_last_electrode_num(self._line_name,robot_name,int(tool)))
            return _last_electrode_num
    
    def __check_electrode_change(self, robot_name):
        """
        """
        electrode_no = self._filtered_df['electrodeNo'].unique()
        len_electrode_no = len(electrode_no)
        list_index = self._filtered_df.index
        len_index = len(list_index)
        count = 1 
        points_applied = [0] * len_electrode_no
        n_milling = [0] * len_electrode_no
        
        self._last_electrode_num = self.__get_last_electrode(electrode_no,robot_name)

        for index in range(len_index):
            # avoids looking in an index that does not exist. 
            if (count + 1) > len_index:
                break
            count += 1


            electrode_no_index = np.where(electrode_no == self._filtered_df['electrodeNo'][self._filtered_df.index[index]])[0][0]

            
            #Check if you changed the clamp
            if self._filtered_df['electrodeNo'][self._filtered_df.index[index]] != self._filtered_df['electrodeNo'][self._filtered_df.index[index + 1]]:
                points_applied[electrode_no_index] += 1
                n_milling[electrode_no_index] = self._filtered_df['tipDressCounter'][list_index[index]]

                aux_index = np.where(electrode_no == self._filtered_df['electrodeNo'][self._filtered_df.index[index + 1]])[0][0]
                if n_milling[aux_index] > self._filtered_df['tipDressCounter'][list_index[index + 1]] and points_applied[aux_index] != 0:
                        points_applied[aux_index] += 1
                        self._last_electrode_num[aux_index] += 1
                        time = self._filtered_df['dateTime'][list_index[index]]
                        time = time[:19]

                        if self._last_date != time[:19]:
                            self._sql.post_data_wellding(self._line_name,self._last_electrode_num[aux_index],robot_name,points_applied[aux_index], int(n_milling[aux_index]),int(electrode_no[aux_index]),time)

                        points_applied[aux_index] = 0
                
            
            #Checks that you have applied a point
            elif self._filtered_df['tipDressCounter'][list_index[index]] <= self._filtered_df['tipDressCounter'][list_index[index + 1]]:
                points_applied[electrode_no_index] += 1

            else:
                n_milling[electrode_no_index] = self._filtered_df['tipDressCounter'][list_index[index]]
                points_applied[electrode_no_index] += 1
                self._last_electrode_num[electrode_no_index] += 1
                time = str(self._filtered_df['dateTime'][list_index[index]])
                time = time[:19]

                if self._last_date != time:
                    self._sql.post_data(self._line_name,self._last_electrode_num[electrode_no_index],robot_name,points_applied[electrode_no_index],int(n_milling[electrode_no_index]),int(electrode_no[electrode_no_index]),time)

                points_applied[electrode_no_index] = 0



wellding = protocol_current_values()
print("End code")
        

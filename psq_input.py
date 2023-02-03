import pandas as pd
import numpy as np
import csv
from paths import path_manipulation
from SQL_manipulation import sql_manipulation

class psq_update():
    def __init__(self):
        self._path = path_manipulation()
        self._sql = sql_manipulation()

        self._sql

        for path_index in range(self._path.len_paths):
            self._line_name = self._path.get_line_name(path_index)
            file_path = self._path.file_path(path_index)
            
            if 'Protocolo valores de corrente' in file_path:
                try:
                    usecols = ['"dateTime"', '"timerName"','"tipDressCounter"', '"electrodeNo"','"uirMeasuringActive"', '"uirRegulationActive"', '"uirMonitoringActive"']
                    self._df = pd.read_csv(file_path, quoting=csv.QUOTE_NONE, sep = ";", usecols = usecols)


                    self._df.dropna()
                    self._df['"dateTime"'] = pd.to_datetime(self._df['"dateTime"'])
                    self._df['"dateTime"'] = self._df['"dateTime"'].dt.strftime('%Y-%m-%d %H:%M:%S')


                except Exception as e:
                    raise TypeError(f"CSV reading failed. file Name {file_path}. {e}")

                self.__data_formatting()
                self._filtered_df =self._df

                self._list_name = self._df['timerName'].unique()

                self.__add_psq_column()
                print(f"psq - file start: {file_path}")
                self.__main()
    
    def __add_psq_column(self):
        """
        Add a column in the dataframe, with the PSQ status calculations.
        """
        is_true = lambda x:int(x==1)
        psq = lambda row: is_true(row['uirMeasuringActive']) + is_true(row['uirRegulationActive']) + is_true(row['uirMonitoringActive'])

        self._df['psq'] = self._df.apply(psq,axis=1)
    
    def __data_formatting(self):
        """
        Fixes formatting of columns imported from CSV.
        """
        self._df.columns = self._df.columns.str.replace(r'"', '')
        self._df['timerName'] = self._df['timerName'].str.replace(r'"', '')
    
    
    def __main(self):
        """
        Applies the filter for each existing robot in the CSV file.
        """

        send = 0
        for robot_name in self._list_name:
            for tool in self.__get_electrode_no(robot_name):
                tool_name = f"{self._line_name}_{robot_name}_{tool}"
                number_points = self._sql.get_num_points_psq(self._line_name,tool_name)
                num_points_psq_off = self._sql.get_num_points_psq_off(self._line_name,tool_name)
                last_update = self._sql.get_last_update_psq(self._line_name,tool_name)
                

                #filters
                df_mask_date = pd.to_datetime(self._df['dateTime']) > pd.to_datetime(last_update)
                positions_date = np.flatnonzero(df_mask_date)
                self._filtered_df = self._df.iloc[positions_date]

                df_mask_names = self._filtered_df['timerName'] == robot_name
                positions_names = np.flatnonzero(df_mask_names)
                self._filtered_df = self._filtered_df.iloc[positions_names]

                df_mask_names = self._filtered_df['electrodeNo'] == tool
                positions_names = np.flatnonzero(df_mask_names)
                self._filtered_df = self._filtered_df.iloc[positions_names]

                if not self._filtered_df.empty:
                    number_points += int(self._filtered_df['tipDressCounter'].count())
                    num_points_psq_off += self.__count_psq_off()

                    send += 1
                    self._sql.post_data_psq(self._line_name,tool_name, self.__get_last_psq(), number_points, num_points_psq_off, self.__last_update(), count = send)
    
    def __get_electrode_no(self,robot_name: str):
        """
        Get all tools from the robot.
        """
        df_mask_date = self._df['timerName'] == robot_name
        positions_date = np.flatnonzero(df_mask_date)
        aux_df = self._df.iloc[positions_date]

        return aux_df['electrodeNo'].dropna().unique().tolist()


    def __count_psq_off(self):
        """
        Counts how many points have been applied with PSQ disabled.
        """
        count_val = self._filtered_df['psq'].value_counts()
        unique_val = self._filtered_df['psq'].unique()
        psq_off = 0

        for val in unique_val:
            if val != 3:
                psq_off += int(count_val[val])

        
        return psq_off

    def __get_last_psq(self):
        """
        Gets the latest PSQ stats in CSV.
        """
        psq_status = self._filtered_df['psq'].tail(1)

        if int(psq_status) == 3:
            return 1
        else:
            return 0
    
    def __last_update(self):
        """
        Takes the time of the last weld spot applied.
        """
        date = str(self._filtered_df['dateTime'].tail(1))
        date = date.split('\n')[0]
        return date[-19:]
    

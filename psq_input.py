import pandas as pd
import numpy as np
import csv
from paths import path_manipulation
from SQL_manipulation import sql_manipulation

class psq_count():
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
    
    def __data_formatting(self):
        """
        Fixes formatting of columns imported from CSV.
        """
        self._df.columns = self._df.columns.str.replace(r'"', '')
        self._df['timerName']= self._df['timerName'].str.replace(r'"', '')
    
    def __main(self):
        for robot_name in self._list_name:
            number_points = self._sql.get_num_points_psq(self._line_name,robot_name)
            num_points_psq_off = self._sql.get_num_points_psq_off(self._line_name,robot_name)

            df_mask_date = self._df['dateTime'] > self._sql.get_last_update_psq(self._line_name,robot_name)
            positions_date = np.flatnonzero(df_mask_date)
            self._filtered_df = self._df.iloc[positions_date]

            df_mask_names = self._filtered_df['timerName'] == robot_name
            positions_names = np.flatnonzero(df_mask_names)
            self._filtered_df = self._filtered_df.iloc[positions_names]

            number_points += int(self._filtered_df['tipDressCounter'].count())
            num_points_psq_off += int(self._filtered_df.query('uirMeasuringActive == 1' or 'uirRegulationActive == 1' or 'uirMonitoringActive == 1')['tipDressCounter'].count())

            self._sql.post_data_psq()
            

psq_count()
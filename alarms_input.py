import pandas as pd
import numpy as np
import csv
from paths import path_manipulation
from SQL_manipulation import sql_manipulation


class alarms_update():
    def __init__(self):
        self._path = path_manipulation()
        self._sql = sql_manipulation()
        

        for path_index in range(self._path.len_paths):
            self._line_name = self._path.get_line_name(path_index)
            file_path = self._path.file_path(path_index)

            if'Protocolo de erros' in file_path:
                try:
                    #optimizing the reading of the csv file.
                    usecols = ['"protRecord_ID"', '"dateTime"', '"timerName"', '"errorCode1"', '"errorCode1_txt"',
                        '"Code2Interpret"', '"errorCode2"', '"errorCode2_txt"', '"isError"', '"isError_txt"']

                    self._df = pd.read_csv(file_path, quoting=csv.QUOTE_NONE, sep = ";", usecols = usecols)
                    self._df.dropna()

                    self._df['"dateTime"'] = pd.to_datetime(self._df['"dateTime"'])
                    self._df['"dateTime"'] = self._df['"dateTime"'].dt.strftime('%Y-%m-%d %H:%M:%S')
                except Exception as e:
                    raise TypeError("CSV reading failed. file Name {file_path}. {e}")

                self.__data_formatting()
                self._filtered_df = self._df
                self.__post_data()
                self._path.move_file(path_index)

    def __data_formatting(self):
        """
        Fixes formatting of columns imported from CSV.
        """
        self._df.columns = self._df.columns.str.replace(r'"', '')
        self._df['timerName'] = self._df['timerName'].str.replace(r'"', '')
        self._df['isError_txt'] = self._df['isError_txt'].str.replace(r'"', '')
        self._df['errorCode1_txt'] = self._df['errorCode1_txt'].str.replace(r'"', '')
        self._df['errorCode2_txt'] = self._df['errorCode2_txt'].str.replace(r'"', '')

    def __post_data(self):
        val = []
        list_vals = []

        df_mask_date = pd.to_datetime(self._df['dateTime']) > pd.to_datetime(self._sql.get_last_time_alarms())
        positions_date = np.flatnonzero(df_mask_date)
        self._filtered_df = self._df.iloc[positions_date]

        df_mask_names = self._filtered_df['protRecord_ID'] > self._sql.get_last_record_id_alarms()
        positions_names = np.flatnonzero(df_mask_names)
        self._filtered_df = self._filtered_df.iloc[positions_names]

        #debug area
        total_quantity = len(self._filtered_df.index)
        submitted = 0

        for index in self._filtered_df.index:
            timer_name = self._filtered_df['timerName'][index]
            if len(timer_name) > 9:
                timer_name = 'UNDEFINED'
            val.clear()
            val.append(int(self._filtered_df['protRecord_ID'][index]))
            val.append(self._filtered_df['dateTime'][index])
            val.append(timer_name)
            val.append(int(self._filtered_df['errorCode1'][index]))
            val.append(self._filtered_df['errorCode1_txt'][index])
            val.append(int(self._filtered_df['Code2Interpret'][index]))
            val.append(int(self._filtered_df['errorCode2'][index]))
            val.append(str(self._filtered_df['errorCode2_txt'][index]))
            val.append(str(self._filtered_df['isError'][index]))
            val.append(self._filtered_df['isError_txt'][index])

            list_vals.append(val)

            if len(list_vals) >= 7000:
                self._sql.post_data_alarms(list_vals)

                submitted += len(list_vals)
                print(f"{submitted} / {total_quantity} alarms")
                    
        if len(list_vals) != 0:
            self._sql.post_data_alarms(list_vals)

            submitted += len(list_vals)
            print(f"{submitted} / {total_quantity} alarms")

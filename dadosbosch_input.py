import pandas as pd
import numpy as np
import csv
from paths import path_manipulation
from SQL_manipulation import sql_manipulation

class dadosbosch_update():
    def __init__(self):
        self._path = path_manipulation()
        self._sql = sql_manipulation()

        for path_index in range(self._path.len_paths):
            self._line_name = self._path.get_line_name(path_index)
            file_path = self._path.file_path(path_index)

            if 'Protocolo valores de corrente' in file_path:
                try:
                    self._df = pd.read_csv(file_path, quoting= csv.QUOTE_NONE, sep = ";")
                except:
                    TypeError("CSV reading failed")
                
                self.__data_formatting()
                self._list_name = self._df['timerName'].unique()

                self.__add_psq_column()
                self.__add_flag_224()

                self._filtered_df = self._df
                self.__post_data()
    
    def __data_formatting(self):
        """
        Fixes formatting of columns imported from CSV.
        """
        self._df.columns = self._df.columns.str.replace(r'"', '')
        self._df['timerName'] = self._df['timerName'].str.replace(r'"', '')

    def __add_psq_column(self):
        """
        Add a column in the dataframe, with the PSQ status calculations.
        """
        is_true = lambda x:int(x == 1)
        psq = lambda row: is_true(row['uirMeasuringActive']) + is_true(row['uirRegulationActive']) + is_true(row['uirMonitoringActive'])

        self._df['psq'] = self._df.apply(psq,axis = 1)

    def __add_flag_224(self):
        """
        Add a column in the dataframe, with the PSQ status calculations.
        """
        is_224 = lambda x:int(x == 224)
        is_first = lambda y:int(y == 1)

        flag_224 = lambda row: is_224(row['progNo']) + is_first(row['tipDressCounter'])

        self._df['flag_224'] = self._df.apply(flag_224,axis=1)
    
    def __post_data(self):
        """
        """
        sql_column_name = 'prot_record_id,tool_name,line,station,model,status_psq,date_time,timer_name,prog_no,flag_224,spot_name,wear,wear_per_cent,monitor_state,monitor_state_txt,measure_state,regulation_std,i_demand_1,i_actual_1,	regulation_1,i_demand_2,i_actual_2,regulation_2,i_demand_3,i_actual_3,regulation_3,pha_std,pha_1,pha_2,pha_3,t_i_demand_std,t_actual_std,tip_dress_counter,electrode_no,voltage_actual_value,voltage_ref_value,currentActualValue,current_reference_value,weld_time_actual_value,weld_time_ref_value,energy_actual_value,energy_ref_value,power_actual_value,power_ref_value,resistance_actual_value,resistance_ref_value,pulse_width_actual_value,	pulse_width__ref_value,	stabilisation_factor_act_value,	stabilisation_factor_ref_value,uip_actual_value,uip_ref_value,uir_expulsion_time,uir_measuring_active,uir_regulation_active,uir_monitoring_active,uir_weld_time_prolongation_active' 
        val = []

        for robot_name in self._list_name:
            tool_name = f'{self._line_name}_{robot_name}'
            for index in range(len(self._filtered_df['protRecord_ID'])):
                val.append(self._filtered_df['protRecord_ID'][index])
                val.append(self._filtered_df['protRecord_ID'][index])
                val.append(self._filtered_df['protRecord_ID'][index])
                val.append(self._filtered_df['protRecord_ID'][index])
                val.append(self._filtered_df['protRecord_ID'][index])
                val.append(self._filtered_df['protRecord_ID'][index])
                val.append(self._filtered_df['protRecord_ID'][index])
                val.append(self._filtered_df['protRecord_ID'][index])

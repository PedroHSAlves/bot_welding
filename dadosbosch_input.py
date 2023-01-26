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
                    usecols = ['"protRecord_ID"','"dateTime"', '"timerName"', '"progNo"', '"spotName"', '"wear"', '"wearPerCent"', '"monitorState"', '"monitorState_txt"', '"measureState"', '"regulationStd"', '"iDemand1"', '"iActual1"', '"regulation1"', '"iDemand2"', '"iActual2"', '"regulation2"', '"iDemand3"', '"iActual3"', '"regulation3"', '"phaStd"', '"pha1"', '"pha2"', '"pha3"', '"t_iDemandStd"', '"tActualStd"', '"tipDressCounter"', '"electrodeNo"', '"voltageActualValue"', '"voltageRefValue"', '"currentActualValue"', '"currentReferenceValue"', '"weldTimeActualValue"', '"weldTimeRefValue"', '"energyActualValue"', '"energyRefValue"', '"powerActualValue"', '"powerRefValue"', '"resistanceActualValue"', '"resistanceRefValue"', '"pulseWidthActualValue"', '"pulseWidthRefValue"', '"stabilisationFactorActValue"', '"stabilisationFactorRefValue"', '"uipActualValue"', '"uipRefValue"', '"uirExpulsionTime"', '"uirMeasuringActive"', '"uirRegulationActive"', '"uirMonitoringActive"', '"uirWeldTimeProlongationActive"']
                    self._df = pd.read_csv(file_path, quoting= csv.QUOTE_NONE, sep = ";", usecols = usecols, keep_default_na = False)
                    self._df.dropna()
                except Exception as e:
                   raise TypeError(f"CSV reading failed. file Name {file_path}. {e}")
                
                self.__data_formatting()
                self._list_name = self._df['timerName'].unique()
                
                self.__add_psq_column()
                self.__add_flag_224()

                self._filtered_df = self._df
                self.__post_data()
                self._path.move_file(path_index)  
    
    def __data_formatting(self):
        """
        Fixes formatting of columns imported from CSV.
        """
        self._df.columns = self._df.columns.str.replace(r'"', '')
        self._df['timerName'] = self._df['timerName'].str.replace(r'"', '')

        self._df.columns = self._df.columns.str.replace(r'"', '')
        self._df['spotName'] = self._df['spotName'].str.replace(r'"', '')
        

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
        query = 'INSERT INTO dadosbosch (protRecord_ID,RobotName,Line,Station,Model,Status_PSQ,dateTime, timerName, progNo, Flag224, spotName, wear, wearPerCent, monitorState, monitorState_txt, measureState, regulationStd, iDemand1, iActual1, regulation1, iDemand2, iActual2, regulation2, iDemand3, iActual3, regulation3, phaStd, pha1, pha2, pha3, t_iDemandStd, tActualStd, tipDressCounter, electrodeNo, voltageActualValue, voltageRefValue, currentActualValue, currentReferenceValue, weldTimeActualValue, weldTimeRefValue, energyActualValue, energyRefValue, powerActualValue, powerRefValue, resistanceActualValue, resistanceRefValue, pulseWidthActualValue, pulseWidthRefValue, stabilisationFactorActValue, stabilisationFactorRefValue, uipActualValue, uipRefValue, uirExpulsionTime, uirMeasuringActive, uirRegulationActive, uirMonitoringActive, uirWeldTimeProlongationActive) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)' 
        val = []
        list_val = []
        send = 0

        for robot_name in self._list_name:
            for tool in self.__get_electrode_no(robot_name):
                tool_name = f'{self._line_name}_{robot_name}_{tool}'

                self.__filter_df(robot_name,tool,tool_name)
                list_index = self._filtered_df.index

                for index in range(len(list_index)):
                    val.clear()

                    model = 'n/a'

                    val.append(int(self._filtered_df['protRecord_ID'][list_index[index]]))
                    val.append(tool_name)
                    val.append(self._line_name)
                    val.append(self._filtered_df['timerName'][list_index[index]][3:-3])
                    val.append(model)
                    val.append(int(self._filtered_df['psq'][list_index[index]]))
                    val.append(self._filtered_df['dateTime'][list_index[index]])
                    val.append(self._filtered_df['timerName'][list_index[index]])
                    val.append(int(self._filtered_df['progNo'][list_index[index]]))
                    val.append(int(self._filtered_df['flag_224'][list_index[index]]))
                    val.append(self._filtered_df['spotName'][list_index[index]])
                    val.append(int(self._filtered_df['wear'][list_index[index]]))
                    val.append(int(self._filtered_df['wearPerCent'][list_index[index]]))
                    val.append(int(self._filtered_df['monitorState'][list_index[index]]))
                    val.append(self._filtered_df['monitorState_txt'][list_index[index]][1:-1])
                    val.append(int(self._filtered_df['measureState'][list_index[index]]))
                    val.append(int(self._filtered_df['regulationStd'][list_index[index]]))
                    val.append(int(self._filtered_df['iDemand1'][list_index[index]]))
                    val.append(int(self._filtered_df['iActual1'][list_index[index]]))
                    val.append(int(self._filtered_df['regulation1'][list_index[index]]))
                    val.append(int(self._filtered_df['iDemand2'][list_index[index]]))
                    val.append(int(self._filtered_df['iActual2'][list_index[index]]))
                    val.append(int(self._filtered_df['regulation2'][list_index[index]]))
                    val.append(int(self._filtered_df['iDemand3'][list_index[index]]))
                    val.append(int(self._filtered_df['iActual3'][list_index[index]]))
                    val.append(int(self._filtered_df['regulation3'][list_index[index]]))
                    val.append(int(self._filtered_df['phaStd'][list_index[index]]))
                    val.append(int(self._filtered_df['pha1'][list_index[index]]))
                    val.append(int(self._filtered_df['pha2'][list_index[index]]))
                    val.append(int(self._filtered_df['pha3'][list_index[index]]))
                    val.append(int(self._filtered_df['t_iDemandStd'][list_index[index]]))
                    val.append(int(self._filtered_df['tActualStd'][list_index[index]]))
                    val.append(int(self._filtered_df['tipDressCounter'][list_index[index]]))
                    val.append(int(self._filtered_df['electrodeNo'][list_index[index]]))
                    val.append(int(self._filtered_df['voltageActualValue'][list_index[index]]))
                    val.append(int(self._filtered_df['voltageRefValue'][list_index[index]]))
                    val.append(int(self._filtered_df['currentActualValue'][list_index[index]]))
                    val.append(int(self._filtered_df['currentReferenceValue'][list_index[index]]))
                    val.append(int(self._filtered_df['weldTimeActualValue'][list_index[index]]))
                    val.append(int(self._filtered_df['weldTimeRefValue'][list_index[index]]))
                    val.append(int(self._filtered_df['energyActualValue'][list_index[index]]))
                    val.append(int(self._filtered_df['energyRefValue'][list_index[index]]))
                    val.append(int(self._filtered_df['powerActualValue'][list_index[index]]))
                    val.append(int(self._filtered_df['powerRefValue'][list_index[index]]))
                    val.append(int(self._filtered_df['resistanceActualValue'][list_index[index]]))
                    val.append(int(self._filtered_df['resistanceRefValue'][list_index[index]]))
                    val.append(int(self._filtered_df['pulseWidthActualValue'][list_index[index]]))
                    val.append(int(self._filtered_df['pulseWidthRefValue'][list_index[index]]))
                    val.append(int(self._filtered_df['stabilisationFactorActValue'][list_index[index]]))
                    val.append(int(self._filtered_df['stabilisationFactorRefValue'][list_index[index]]))
                    val.append(int(self._filtered_df['uipActualValue'][list_index[index]]))
                    val.append(int(self._filtered_df['uipRefValue'][list_index[index]]))
                    val.append(int(self._filtered_df['uirExpulsionTime'][list_index[index]]))
                    val.append(int(self._filtered_df['uirMeasuringActive'][list_index[index]]))
                    val.append(int(self._filtered_df['uirRegulationActive'][list_index[index]]))
                    val.append(int(self._filtered_df['uirMonitoringActive'][list_index[index]]))
                    val.append(int(self._filtered_df['uirWeldTimeProlongationActive'][list_index[index]]))
                    
                    list_val.append(val)

                    if len(list_val) >= 7000:
                        send += len(list_val)
                        self._sql.post_data_dadosbosch(query,list_val, count = send)
                        list_val.clear()
        
        if len(list_val) != 0:
            send += len(list_val)
            self._sql.post_data_dadosbosch(query,list_val, count = send)
            self._sql.post_data_dadosbosch(query,list_val)
            list_val.clear()
                


    def __filter_df(self,robot_name: str, tool: int, tool_name: str):
        """
        Filters the dataframe by robot_name, tool, time.
        """
        _last_date = self._sql.get_last_time_dadosbosch(self._line_name,tool_name)

        df_mask_date = self._df['dateTime'] > _last_date
        positions_date = np.flatnonzero(df_mask_date)
        self._filtered_df = self._df.iloc[positions_date]

        df_mask_names = self._filtered_df['timerName'] == robot_name
        positions_names = np.flatnonzero(df_mask_names)
        self._filtered_df = self._filtered_df.iloc[positions_names]

        df_mask_names = self._filtered_df['electrodeNo'] == tool
        positions_names = np.flatnonzero(df_mask_names)
        self._filtered_df = self._filtered_df.iloc[positions_names]


    def __get_electrode_no(self, robot_name: str):
        """
        Get all tools from the robot_name.
        """
        df_mask_date = self._df['timerName'] == robot_name
        positions_date = np.flatnonzero(df_mask_date)
        aux_df = self._df.iloc[positions_date]

        return aux_df['electrodeNo'].unique()
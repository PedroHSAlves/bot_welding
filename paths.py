import os
#ROOT_FILE = r'D:\Perfil'
ROOT_FILE = r'W:'

csv_current_value_protocol = r'W:\Respot1OP005\Protocolo valores de corrente16_12_2022_08_25_55.txt'
line_name = r'Respot 1'

class path_manipulation():
    def __init__(self):
        self._pcs_list_dir = os.listdir(path=ROOT_FILE)
        self._list_paths = []

        for pc in self._pcs_list_dir:
            file_name = os.listdir(f'{ROOT_FILE}\{pc}')
            self._list_paths.append(f'{ROOT_FILE}\{pc}\{file_name}')

    def name_file(self,index):
        return self._list_paths[index]

    @property
    def len_paths(self):
        return len(self._list_paths)
    @property
    def len_pcs(self):
        return len(self._pcs_list_dir)
    @property
    def get_line_name(self):
        return line_name
    

#Nomes das pastas são 'linha'_PCX

path = path_manipulation()
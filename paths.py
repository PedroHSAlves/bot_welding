import os
#ROOT_FILE = r'D:\Perfil'
ROOT_FILE = r'W:'#Teste root

# csv_current_value_protocol = r'W:\Respot1OP005\Protocolo valores de corrente16_12_2022_08_25_55.txt'
# line_name = r'Respot 1'

class path_manipulation():
    def __init__(self):
        """
        Constructor method
        Creates an object to manipulate the files
        """
        self._pcs_list_dir = os.listdir(path=ROOT_FILE)
        self._list_paths = []

        for pc in self._pcs_list_dir:
            file_name = os.listdir(f'{ROOT_FILE}\{pc}')
            self._list_paths.append(f'{ROOT_FILE}\{pc}\{file_name}')

    def file_path(self,index):
        """
        Returns the address of the csv file.
        """
        return self._list_paths[index]

    @property
    def len_paths(self):
        """
        Returns the total number of CSV files found
        """
        return len(self._list_paths)
    @property
    def len_pcs(self):
        """
        Returns the number of computers in the root folder
        """
        return len(self._pcs_list_dir)
        
    def get_line_name(self,index):
        """
        Return the name of the production line
        """
        return self._pcs_list_dir[index]
    
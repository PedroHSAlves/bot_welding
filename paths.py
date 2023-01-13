import os
import shutil

#ROOT_FILE = r'D:\Perfil'
#DESTINATION_FOLDER = r'D:\Perfil2'

#Test Variables
ROOT_FILE = r'W:'#Teste root
DESTINATION_FOLDER = r'C:\Users\sc29697\Documents\UOF_PCM13'

# csv_current_value_protocol = r'W:\Respot1OP005\Protocolo valores de corrente16_12_2022_08_25_55.txt'
# line_name = r'Respot 1'

class path_manipulation():
    def __init__(self):
        self._pcs_list_dir = os.listdir(path=ROOT_FILE)
        self._list_paths = []

        for pc in self._pcs_list_dir:
            file_name = os.listdir(f'{ROOT_FILE}\{pc}')
            if len(file_name) != 0:
                for file in file_name:
                    self._list_paths.append(ROOT_FILE + "\\" + pc + "\\" + file)

    def file_path(self,index:int):
        """
        Returns the address of the csv file.
        """
        return self._list_paths[index]
    
    def move_file(self, index:int):
        """
        Relocates already used files.
        """
        path = self._list_paths[index]
        folder_name = path[3:path.find('PC')+3]
        
        try:
            shutil.move(path, f'{DESTINATION_FOLDER}\{folder_name}')
        except:
            raise TypeError("Error when moving the directory file")

    def get_line_name(self,index:int):
        """
        Return the name of the production line
        """
        path = self._list_paths[index]
        return path[3:path.find('PC')]

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
        
    
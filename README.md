# WELDING BOT CODE DOCUMENTATION
# SUMMARY
- [Imported Libraries](#imported-libraries)
- [authentication.py](#authentication)

- [paths.py](#paths)
  - [class path_manipulation()](#class-path_manipulation)

      - [\__init\__](#_init_)

      - [file_path(self,index:int)](#file_pathselfindexint)

      - [move_file(self,index:int)](#move_fileselfindexint)

      - [get_line_name(self,index:int)](#get_line_nameselfindexint)

      - [len_paths](#len_paths)

      - [len_pcs](#len_pcs)
      
# IMPORTED LIBRARIES
# AUTHENTICATION

This code defines two variables `_user` and `_passaword`. These variables are used for authentication and for security reasons, they should not be uploaded to a GitHub repository. Put another way, this means that the user and password are kept private and should not be shared with others or stored in a public place like a GitHub repository.

# PATHS
## class path_manipulation():

### \__init\__
This method is called when an instance of the class is created. It initializes the instance variables `_pcs_list_dir` and `_list_paths`. `_pcs_list_dir` is a list of the directories in the root file, and `_list_paths` is a list of the file paths for each file in those directories.

### file_path(self,index:int)

This method takes an index as input and returns the address of the corresponding csv file from the `_list_paths` instance variable.


### move_file(self,index:int)

This method takes an index as input and relocates the corresponding file from the `_list_paths` instance variable to a new destination folder. If the folder does not exist, it is created.

### get_line_name(self,index:int)

This method takes an index as input and returns the name of the production line.

### len_paths

This property returns the total number of CSV files found.

### len_pcs

This property returns the number of computers in the root folder.

# PSQ_INPUT
## class psq_update():

This code is responsible for handling the processing of the data from the CSV file and updating the data in the database.

### \_\_init\_\_(self)

This method is called when an instance of the class is created. It initializes the instance variable `_path` which is an instance of the class.

### __add_psq_column(self)

This method adds a new column to the dataframe, called 'psq', which calculates the PSQ status. It does this by applying a lambda function to each row that adds the values of the 'uirMeasuringActive', 'uirRegulationActive', and 'uirMonitoringActive' columns together, and returns 1 if the sum is equal to 3, otherwise it returns 0. 

The status of the PSQ some will be considered active, when the three columns mentioned above have their values equal to 1.

### __data_formatting(self)

This method fixes the formatting of the columns in the dataframe by removing the double quotes from the column names and the 'timerName' column.

### __main(self)

This is the main method of the class, which applies filters to the dataframe for each existing robot in the CSV file. It iterates through each unique robot name in the dataframe, and for each tool of that robot, it gets the current number of points, PSQ off points, and the last update time from the SQL database. Then it applies filters to the dataframe for the robot name, tool number, and dateTime, and if the filtered dataframe is not empty, it counts the number of points and PSQ off points, gets the last PSQ status and update time from the filtered dataframe, and sends that information to the SQL database using the sql_manipulation class.

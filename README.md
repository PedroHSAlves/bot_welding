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
 
 - [psq_input.py](#psq_input)
    - [class psq_upadate()](#class-psq_update)
      
# IMPORTED LIBRARIES
# AUTHENTICATION

This code defines two variables `_user` and `_passaword`. These variables are used for authentication and for security reasons, they should not be uploaded to a GitHub repository. Put another way, this means that the user and password are kept private and should not be shared with others or stored in a public place like a GitHub repository.

# DADOSBOSCH_INPUT
## class dadosbosch_update()
### \_\_init\_\_()

This method initializes an instance of the class `dadosbosch_update`. It creates instance of two other classes, `path_manipulation` and `sql_manipulation`, and store them in the instance variables `_path` and `_sql` respectively. It then iterates over the paths returned by the `_path.len_paths` and reads the data from the CSV files located at those paths. If the file cannot be read, it raises an error. The method then calls several other methods to format the data, add new columns, and finally post the data to an external system.

### \_\_data\_formatting(self)

This method formats the data contained in the dataframe `_df` by fixing the formatting of columns imported from the CSV file, converting the datetime column to the required format, removing rows with empty values, and formatting the `timerName` and `spotName` columns.

### \_\_add\_psq\_column(self)

This method adds a new column to the dataframe `_df` to calculate the PSQ status. It uses the lambda function `psq` to  add status to the `psq` column in the dataframe.

### \_\_add\_flag\_224(self)

This method adds a new column to the dataframe `_df` to flag values of 224. It uses the lambda function `flag_224` to add the flag to the `flag_224` column in the dataframe. The flag_224 is considered active only when the value of the tipDressCounter column is equal to 1 and the value of the progNo column is equal to 224.

### \_\_post\_data(self)

This method posts the processed data to an external system.

 
 ### \_\_filter\_df(self,robot_name: str, tool: int, tool_name: str)
 
This method filters a dataframe basede on specified conditions. It takes a dataframe and a dictionary of column names and values as input. The dataframe is filtered such that the resulting dataframe contains only the rows where the value in the specified column matches the value in the dictionary.

### \_\_get\_electrode\_no(self, robot\_name: str)

This method extracts the electrode number from a string. It takes a string as input and returns the value of the electrode nuber contained within the string.
 
# MAIN

This code calls the functions [alarms_update()](#), [psq_update()](#psq_input), [electrode_update()](#wellding_input), and [dadosbosch_update()](#). And finally shows the total execution time of the code.

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

This method adds a new column to the dataframe, called `psq`, which calculates the PSQ status. It does this by applying a lambda function to each row that adds the values of the `uirMeasuringActive`, `uirRegulationActive`, and `uirMonitoringActive` columns together, and returns 1 if the sum is equal to 3, otherwise it returns 0. 

The status of the PSQ some will be considered active, when the three columns mentioned above have their values equal to 1.

### __data_formatting(self)

This method fixes the formatting of the columns in the dataframe by removing the double quotes from the column names and the `timerName` column.

### __main(self)

This is the main method of the class, which applies filters to the dataframe for each existing robot in the CSV file. It iterates through each unique robot name in the dataframe, and for each tool of that robot, it gets the current number of points, PSQ off points, and the last update time from the SQL database. Then it applies filters to the dataframe for the robot name, tool number, and dateTime, and if the filtered dataframe is not empty, it counts the number of points and PSQ off points, gets the last PSQ status and update time from the filtered dataframe, and sends that information to the SQL database using the sql_manipulation class.

### __get_electrode_no(self,robot_name: str)

This method returns a list of all the tools associated with a specific robot. It filters the data for the given `robot_name` and returns the unique values in the "eletrodeNo" column.

### __count_psq_off(self)

This method counts the number of rows in the filtered dataframe where the value in the "psq" column is equal to 0.

### __get_last_psq(self)

This method returns the last value in the "psq" column of the filtered daframe.

### __last_update(self)

This method returns the last value in the "dataTime" column of the filtered dataframe. 



# SQL_MANIPULATION
## class sql_manipulation()
### \_\_init\_\_(self)

This method is the constructor of the class, it initializes a connection to a MySQL database with the give host, user, password, and databese name.

### post_data_wellding(self, vals, count = 0)

This method accepts a list of values `vals` and a `count` value, and performs a bulk data commit to the `wellding` database. The data is inserted into the database using the "excutemany" method and the provided SQL statement. The numeber of records inserted is printed as output.

### post_data_psq(self,line_name: str, robot_name: str, status_psq: int, number_points: int, num_points_psq_off: int, last_update, count = 0)

This method accepts line `line name`, `robot name`, `status psq`, `number os points applied`, `number of points of PSQ off`, and `last update values`. It first calls the [del_data_psq](#del_data_psqself-line_name-str-robot_name-str) method to delete any existing data in the database, and then inserts the new data into the `psq` database. The number of records inserted is printed as output. 

### post_data_dadosbosch(self, sql, vals, count = 0)

This method accepts an SQL statement and a list of values `vals`, and performs a bulk data commit to the `dadosbosch` database. The data is inserted into the database using the "executemany" method and the provided SQL statement. The number of records inserted is printed as output.

### post_data_alarms(self,val)

This method accepts a list of values and inserts them into the `alarms` database. The data is inserted into the database using the "executemany" method and a provided SQL statement.

### del_data_psq(self, line_name: str, robot_name: str)

This method accepts `line name`  and `robot name` and deletes the corresponding data from the `psq` database if it exists.

### get_last_time_wellding(self,line_name: str,tool_name: str)

This method accepts `line name` and  `tool name`, and returns the last time recorded in the `wellding` database for the specified line and tool.

### get_last_electrode_num(self,line_name: str,robot_name: str, tool: int)

This method accepts `line name`, `robot name`, and `tool` and returns the last registered electrode numeber in the `wellding` database for the specified line, robot, and tool.

### get_last_milling(line_name: str, tool_name: str)

This method retrieves the last milling number recorded in the `wellding` table for a given line and tool. If there are no records for the specified line and tool, the method returns 0.

### get_num_points_psq(line_name: str, robot_name: str)

This method retrieves the number of points applied from the `psq` table for a given line and robot. If there are no records for the specified line and robot, the method returns 0.

### get_num_points_psq_off(line_name: str, robot_name: str)

This method retrives the number of points applied with PSQ disabled from the `psq` table for a given line and robot. If there are no records for the specified line and robot, the method returns 0.

### get_last_update_psq(line_name: str, robot_name: str)

This method retrives the last time the last applied weld spot was counted from the `psq` table for a given line and robot. IF there are no records for the specified line and robot, the method returns the default time "2000-01-01 00:00:00".

### get_last_time_dadosbosch(line_name: str, tool_name: str)

This method retrieves the last delta time recorded in the `dadosbosch` table for a given line and tool. If there are no records for the specified line and tool, the method returns the default time "2000-01-01 00:00:00".

### get_last_time_alarms() 

This method retrives the last delta time recorded in the `alarms` table. If there are no records in the table, the method returns the default time "2000-01-01 00:00:00"

### get_last_record_id_alarms()

This method retrives the last "ProtrecordId" recorded in the `alarms` table. If there are no records in the table, the method returns the default value of 0.



# WELLDING_INPUT
## class electrode_update()

This class is designed to process data related to welding operations performed by robots. The class perferms several operations such as reading data form CSV files, cleaning and formatting data, and storing the data in a database. The class contains several methods to perform the folwuin tasks:

### \_\_init\_\_()

This is the constructor method that initializes the class by calling methods from the [path_manipulation](paths) and [sql_manipulation](#sql_manipulation) class. It reads the data from the CSV file, formats the data, and calls the [\_\_main](#main) method to perform the required operations.

### \_\_data_formatting()

This method is used to format the columns impoted from the CSV file.

### \_\_main()

This method is the main method that filters the data and performs the required operations. It filters the data for each existing robot in CSV file, checks for electrode changes and counts the number of weld spots applied in each milling operation.

### \_\_get\_electrode\_no(self,robot\_name: str)

This method is used to get all tools used by a robot.

### \_\_get\_last\_electrode(self, tool,robot\_name:str)

This method is used to get the last electrode number of weld spots applied in the database.

### \_\_check\_electrode\_change(self, robot\_name: str, tool)

This method is used to count the number of weld spots applied in each milling operation.

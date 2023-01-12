import mysql.connector
import authentication as auth

class sql_manipulation():
    def __init__(self) -> None:
        try:
            self._mydb = mysql.connector.connect(
                host = "172.20.233.63",
                user = auth._user,
                password = auth._password,
                # database = "perfil"
                database = "teste"
            )
        except:
            TypeError("database connection failure.")
        
        self._mycursor = self._mydb.cursor()

    def post_data_wellding(self, line_name: str,electrode_num: int, name_robot: str, n_points_applied: int, n_millins: int,electrode_no: int,tool_name: str, time: str):
        """
        Realizes a data commit to the wellding database.
        """
        sql = "INSERT INTO wellding (line,electrode_num, name_robot, n_points_applied, n_millins,tool, tool_name, time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (line_name,electrode_num, name_robot, n_points_applied, n_millins,electrode_no, tool_name, time)  
        self._mycursor.execute(sql,val)

        self._mydb.commit()
        print(self._mycursor.rowcount, "record inserted.") 

    def post_data_psq(self):
        pass

    def post_data_dadosbosch(self):
        pass
       
    def get_last_time(self,line_name: str,tool_name: str):
        """
        Get the last delta time recorded in the database.
        """
        sql = "SELECT `tool_name`,`line`,`time` FROM `wellding` WHERE `line` = %s AND `tool_name` = %s ORDER BY `time` DESC LIMIT 1"
        val = (line_name, tool_name)

        self._mycursor.execute(sql,val)
        result = self._mycursor.fetchall()

        if len(result) == 0:
            return  '2000-01-01 00:00:00'#default time
        else:
            return str(result[0][2])

    def get_last_electrode_num(self,line_name: str,robot_name: str, tool: int):
        """
        Get the last registered electrode number in the database.
        """
        sql = "SELECT `name_robot`,`line`,`time`,`electrode_num`,`tool` FROM `wellding` WHERE `line` = %s AND `name_robot` = %s  AND `tool` = %s ORDER BY `time` DESC LIMIT 1"
        val = (line_name, robot_name, tool)

        self._mycursor.execute(sql,val)
        result = self._mycursor.fetchall()

        if len(result) == 0:
            return  0 #electrode default
        else:
            return result[0][3]

    def get_last_milling(self,line_name: str,tool_name: str):
        """
        Get the last milling number resgistered in the database.
        """
        sql = "SELECT `tool_name`,`line`,`time`,`n_millins` FROM `wellding` WHERE `line` = %s AND `tool_name` = %s ORDER BY `time` DESC LIMIT 1"
        val = (line_name, tool_name)
        self._mycursor.execute(sql,val)

        result = self._mycursor.fetchall()

        if len(result) == 0:
            return  0 #milling default
        else:
            return result[0][3]
    
    def get_num_points_psq(self, line_name: str, robot_name: str):
        """
        gets the value of the number of points applied, if the robot already exists in the database.
        """
        sql = "SELECT `line`,`timer_name`,`number_points` FROM `psq` WHERE `line` = %s AND `timer_name` = %s"
        val = (line_name, robot_name)
        self._mycursor.execute(sql,val)
        
        result = self._mycursor.fetchall()

        if len(result) == 0:
            return  0 
        else:
            return result[0][2]
    
    def get_num_points_psq_off(self, line_name: str, robot_name: str):
        """
        gets the value of the number of points applied with psq disabled, if the robot already exists in the database.
        """
        sql = "SELECT `line`,`timer_name`,`num_points_psq_off` FROM `psq` WHERE `line` = %s AND `timer_name` = %s"
        val = (line_name, robot_name)
        self._mycursor.execute(sql,val)
        
        result = self._mycursor.fetchall()

        if len(result) == 0:
            return  0 
        else:
            return result[0][2]

    def get_last_update_psq(self, line_name: str, robot_name: str):
        """
        get the last time of the last applied weld spot counted (last_update)
        """
        sql = "SELECT `line`,`timer_name`,`last_update` FROM `psq` WHERE `line` = %s AND `timer_name` = %s"
        val = (line_name, robot_name)
        self._mycursor.execute(sql,val)
        
        result = self._mycursor.fetchall()

        if len(result) == 0:
            return  '2000-01-01 00:00:00'#default time
        else:
            return str(result[0][2])



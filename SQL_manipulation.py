import mysql.connector
import authentication as auth

class sql_manipulation():
    def __init__(self) -> None:
        try:
            self._mydb = mysql.connector.connect(
                host = "172.20.233.63",
                user = auth._user,
                password = auth._password,
                database = "perfil"
            )
        except:
            TypeError("database connection failure.")
        
        self._mycursor = self._mydb.cursor()

    def post_data(self, electrode_num: int, name_robot: str, n_points_applied: int, n_millins: int,electrode_no: int, time: str):
        sql = "INSERT INTO wellding (electrode_num, name_robot, n_points_applied, n_millins,tool, time) VALUES (%s,%s,%s,%s,%s,%s)"
        val = (electrode_num, name_robot, n_points_applied, n_millins,electrode_no, time)  
        self._mycursor.execute(sql,val)

        self._mydb.commit()
        print(self._mycursor.rowcount, "record inserted.") 
    
    def get_last_time(self,robot_name):
        return "2020-12-15 12:57:13"

    def get_last_electrode_num(self,robot_name):
        return 1

    def get_last_milling(self,robot_name):
        return 50

    def get_last_point_applied(self):
        return

    def revemove_line_in_SQL(self):
        return

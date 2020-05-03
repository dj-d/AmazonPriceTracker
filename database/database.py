import mysql.connector as mysql
import json


class Database:
    """
    Provide methods fom MariaDB connection
    """

    def __init__(self):
        with open('credentials.json') as json_file:
            file = json.load(json_file)
            self.credential = file["db"]

        self.conn = mysql.connect(host="db", database=self.credential["db_name"], user=self.credential["user"], password=self.credential["user_password"])

    def get_conn(self):
        return self.conn

from utility.config_manager import db_config
import mysql.connector


class db_connection:
    
    def __init__(self):
        self.db = mysql.connector.connect(**db_config(), autocommit=True)
        self.cursor = self.db.cursor()

    def __enter__(self):
            return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
            self.db.close()
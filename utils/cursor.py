import json

import mysql.connector
import mysql.connector.cursor

with open("etc/config.json", 'r') as config_file:
    config = json.load(config_file)

host = config['db']['host']
port = config['db']['port']
user = config['db']['user']
password = config['db']['password']
database = config['db']['database']

class Cursor:
    def __init__(self, dictmode=True):
        self.connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor(
            dictionary=dictmode)  # type: mysql.connector.cursor.MySQLCursor | mysql.connector.cursor.MySQLCursorDict

    def __enter__(self):
        return self.cursor

    def __exit__(self, ext_type, exc_value, traceback):
        self.cursor.close()
        if isinstance(exc_value, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()

    def __iter__(self):
        for i in self.cursor:
            yield 
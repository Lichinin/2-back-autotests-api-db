import mysql.connector
from mysql.connector import Error
import os

from dotenv import load_dotenv


load_dotenv()


class DatabaseHelper:
    def __init__(
        self,
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=os.getenv("DB_PORT")
    ):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            return self
        except Error as e:
            raise Exception(f"Ошибка подключения к БД: {e}")

    def execute_query(self, query, params=None):
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            result = cursor.fetchone()
            return result
        except Error as e:
            cursor.close()
            raise Exception(f"Ошибка выполнения запроса: {e}")

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

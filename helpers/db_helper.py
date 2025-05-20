# db_helper.py

import mysql.connector
from mysql.connector import Error


class DatabaseHelper:
    def __init__(self, host='localhost', user='wordpress', password='wordpress', database='wordpress', port=3306):
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
        """Закрывает соединение с БД."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Соединение с БД закрыто")

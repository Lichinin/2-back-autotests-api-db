import os

import mysql.connector
from dotenv import load_dotenv
from mysql.connector import DatabaseError, InterfaceError, ProgrammingError

load_dotenv()


class DatabaseHelper:
    def __init__(
        self,
        host=None,
        user=None,
        password=None,
        database=None,
        port=None
    ):
        self.host = os.getenv("DB_HOST")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_NAME")
        self.port = os.getenv("DB_PORT")
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
        except InterfaceError as e:
            raise ConnectionError(f"Не удалось подключиться к MySQL: {e}") from e
        except DatabaseError as e:
            raise RuntimeError(f"Ошибка базы данных: {e}") from e

    def execute_query(self, query: str, params=None):
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            result = cursor.fetchone()
            return result
        except ProgrammingError as e:
            cursor.close()
            raise ValueError(f"Некорректный SQL-запрос: {e}") from e
        except DatabaseError as e:
            raise RuntimeError(f"Ошибка базы данных: {e}") from e

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

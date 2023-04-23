import sqlite3
from sqlite3 import Connection, Cursor
from abc import ABC


class Data(ABC):
    """Common class for database operation"""


class DataSQLite(Data):
    """Main class for database operation with sqlite engine"""

    def __init__(self, db_name):
        self.engine = 'SQLite'
        self.connection = self._create_connection(db_name)

    @staticmethod
    def _create_connection(db_name: str) -> Connection:
        con = sqlite3.connect(db_name)
        return con

    def _create_cursor(self) -> Cursor:
        cur = self.connection.cursor()
        return cur

    def execute_sql_command(self, sql_command: str) -> None:
        cur = self._create_cursor()
        cur.execute(sql_command)
        cur.fetchone()







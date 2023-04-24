import sqlite3
import logging
from sqlite3 import Connection, Cursor
from abc import ABC
from db.sql_command.sql import InitDatabaseCommand, SQLCookie


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

    def create_cursor(self) -> Cursor:
        cur = self.connection.cursor()
        return cur

    def init_db(self):

        cur = self.create_cursor()

        cur.execute(InitDatabaseCommand.init_table)
        cur.executemany(SQLCookie.insert_cookie_row, InitDatabaseCommand.init_data)
        self.connection.commit()

        logging.info("Database initialized successfully")









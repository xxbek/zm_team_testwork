import datetime
import sqlite3
import logging
from sqlite3 import Connection
from abc import ABC, abstractmethod
from db.sql_command.sql import InitDatabaseCommand, SQLCookie


class DataConnection(ABC):
    """Common class for database operation"""

    @abstractmethod
    def init_db(self, initial_cookie_columns_number):
        pass

    @abstractmethod
    def get_cookie_info_by_id(self, id_cookie):
        pass

    @abstractmethod
    def update_cookie_record(self, id_cookie: int, data: tuple):
        pass


class DataSQLite(DataConnection):
    """Main class for database operation with sqlite engine"""

    def __init__(self, db_path: str):
        self._db_path = db_path

    def _create_connection(self) -> Connection:
        conn = None
        try:
            conn = sqlite3.connect(self._db_path)
        except sqlite3.Error as e:
            logging.error(e)

        return conn

    def init_db(self, initial_columns_number: int) -> None:
        """Initialize test database"""
        with self._create_connection() as con:
            cur = con.cursor()
            cur.execute(InitDatabaseCommand.create_cookie_table)
            cur.executemany(SQLCookie.insert_cookie_row, InitDatabaseCommand.create_init_data(initial_columns_number))
            con.commit()

        logging.info("Database initialized successfully")

    def get_cookie_info_by_id(self, id_cookie: int) -> list:
        """Return a list with cookie, scraping_number_amount and last_scraping_date from Cookie table"""
        with self._create_connection() as con:
            cur = con.cursor()
            cur.execute(SQLCookie.get_cookie_info_by_id, (str(id_cookie),))
            return cur.fetchone()

    def update_cookie_record(self, id_cookie: int, data: list) -> None:
        """Update single record in cookie table"""
        with self._create_connection() as con:
            cur = con.cursor()
            # TODO fix shit
            cur.executemany(SQLCookie.update_cookie_row_by_id, [data[0] + (str(id_cookie),)])
            con.commit()

    def select_all_from_cookie(self) -> list:
        with self._create_connection() as con:
            cur = con.cursor()
            cur.execute(SQLCookie.select_all)
            return cur.fetchall()

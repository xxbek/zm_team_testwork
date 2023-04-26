from utils.utils import get_current_time


class InitDatabaseCommand:
    """Class for collecting initialization sql"""

    _initial_cookie_columns_number = 15

    create_cookie_table = """CREATE TABLE `Cookie` (
  `id` INT NOT NULL,
  `creation_date` DATE NOT NULL,
  `cookie` TEXT NULL,
  `scraping_number_amount` INT DEFAULT 0,
  `last_scraping_date` DATETIME NULL,
  PRIMARY KEY (`id`));"""

    @staticmethod
    def create_init_data(initial_cookie_columns_number):
        """Initial test data"""
        return [(i + 1, get_current_time(), None, 0, None) for i in range(initial_cookie_columns_number)]


class SQLCookie:
    """Class for sql command with Cookie table"""
    get_cookie_info_by_id = """SELECT cookie, scraping_number_amount, last_scraping_date FROM Cookie WHERE id = ?;"""

    insert_cookie_row = """INSERT INTO Cookie VALUES(?, ?, ?, ?, ?);"""

    update_cookie_row_by_id = """
    UPDATE Cookie SET cookie = ?, scraping_number_amount = scraping_number_amount + 1, last_scraping_date = ? 
    WHERE id = ?;"""

    select_all = """SELECT * FROM Cookie"""


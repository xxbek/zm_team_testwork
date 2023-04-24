from datetime import datetime
from datetime import timezone

DATE_NOW = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')


class InitDatabaseCommand:
    """Class for collecting initialization sql"""

    _initial_cookie_columns_number = 15

    init_table = """CREATE TABLE `Cookie` (
  `id` INT NOT NULL,
  `creation_date` DATE NOT NULL,
  `cookie` TEXT NULL,
  `scraping_number_amount` INT DEFAULT 0,
  `last_scraping_date` DATETIME NULL,
  PRIMARY KEY (`id`));"""

    init_data = data = [(i + 1, DATE_NOW, None, 0, None) for i in range(_initial_cookie_columns_number)]


class SQLCookie:
    """Class for sql command with Cookie table"""
    insert_cookie_row = """INSERT INTO Cookie VALUES(?, ?, ?, ?, ?)"""

    update_cookie_row = ...

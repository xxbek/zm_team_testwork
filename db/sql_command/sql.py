class InitDatabaseCommand:
    """Class for collecting sql scripts"""

    init_table = """CREATE TABLE `Cookie` (
  `id` INT NOT NULL,
  `creation_date` DATETIME NOT NULL,
  `cookie` TEXT NULL,
  `scraping_number_amount` INT NULL,
  `last_scraping_date` DATETIME NULL,
  PRIMARY KEY (`id`));"""

    insert_row = ...

    update_row = ...

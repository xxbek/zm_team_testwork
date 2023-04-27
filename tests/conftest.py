import pytest
import logging
from db.database import DataSQLite
from utils.utils import get_file_name_with_date, remove_file

TEST_DB = 'tests/test.db'
LOG_PATH = 'tests/log/log'

log_name = get_file_name_with_date(LOG_PATH)

logging.basicConfig(
    format='%(asctime)s: %(process)d-%(levelname)s: %(message)s',
    level=logging.INFO,
    filemode='w',
    filename=log_name
)

INITIAL_COLUMNS_NUMBER = 15

PROXY_TEST_MODE = False


@pytest.fixture(scope="function")
def connection():
    logging.info("Start test DB connection..")

    con = DataSQLite(TEST_DB)
    con.init_db(INITIAL_COLUMNS_NUMBER)
    yield con

    logging.info("Clear test DB..")
    remove_file(TEST_DB)





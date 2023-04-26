import pytest
import logging
import os
from db.database import DataSQLite


TEST_DB = 'test.db'


@pytest.fixture(scope="function")
def connection():
    logging.info("\nStart test DB connection..")

    open(TEST_DB, 'w').close()
    con = DataSQLite(TEST_DB)

    yield con

    logging.info("\nClear test DB..")
    os.remove(TEST_DB)



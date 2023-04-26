import string
import random
from utils.utils import get_current_time


INITIAL_COLUMNS_NUMBER = 20


def test_db_init(connection):
    connection.init_db(INITIAL_COLUMNS_NUMBER)
    data = connection.select_all_from_cookie()

    assert len(data) == INITIAL_COLUMNS_NUMBER


def test_update_single_cookie_record(connection):
    connection.init_db(INITIAL_COLUMNS_NUMBER)

    updatable_cookie_id = random.randint(1, INITIAL_COLUMNS_NUMBER)
    old_data = connection.get_cookie_info_by_id(updatable_cookie_id)

    update_data = [("'foo': 'bar'", get_current_time())]
    connection.update_cookie_record(updatable_cookie_id, update_data)

    updated_row = connection.get_cookie_info_by_id(updatable_cookie_id)

    assert old_data != updated_row






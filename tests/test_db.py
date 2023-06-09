import random
from tests.conftest import INITIAL_COLUMNS_NUMBER
from utils.utils import get_current_time


def test_db_init(connection):
    data = connection.select_all_from_cookie()

    assert len(data) == INITIAL_COLUMNS_NUMBER


def test_get_cookie_by_id(connection):
    test_cookie_id = random.randint(1, INITIAL_COLUMNS_NUMBER)
    old_data = connection.get_cookie_info_by_id(test_cookie_id)
    update_data = ("'foo': 'bar'", get_current_time(), )
    connection.update_cookie_record(test_cookie_id, update_data)

    new_data = connection.get_cookie_info_by_id(test_cookie_id)

    assert old_data[0] is None
    assert old_data[0] != new_data[0]
    assert new_data[0] == update_data[0]


def test_update_single_cookie_record(connection):

    updatable_cookie_id = random.randint(1, INITIAL_COLUMNS_NUMBER)
    old_data = connection.get_cookie_info_by_id(updatable_cookie_id)

    update_data = ("'foo': 'bar'", get_current_time(), )
    connection.update_cookie_record(updatable_cookie_id, update_data)

    updated_row = connection.get_cookie_info_by_id(updatable_cookie_id)

    assert old_data != updated_row


def test_select_all_from_cookie(connection):
    rows = connection.select_all_from_cookie()

    assert len(rows) == INITIAL_COLUMNS_NUMBER




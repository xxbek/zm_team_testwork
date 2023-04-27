import pytest
from multiprocess.pool import PoolProcess
from multiprocess.runner import SeleniumRunner
from request.parse import NewsRequest
from _runner_test import TestRunner
from tests.conftest import INITIAL_COLUMNS_NUMBER, PROXY_TEST_MODE
from utils.utils import get_shuffle_list, get_random_string_list

TEST_URL_LIST = (
    'http://news.google.com',
    'http://lenta.ru'
)

TEST_URL = TEST_URL_LIST[1]

ACTIVE_PROCESS_NUMBER = 5


def test_pool_work_with_test_runner():
    test_url = get_random_string_list()
    runner = TestRunner()

    pool = PoolProcess(
        runner=runner,
        links_list=test_url
    )

    pool.start_pool()
    assert runner.check_pool_work(), 'Error in Pool or Runner work'


# @pytest.mark.skip(reason='Heavy test with Selemium')
def test_pool_work_with_database_and_test_url(connection):
    with open('tests/_test_links.txt', 'r') as f:
        test_links = [i.strip() for i in f]

    test_links_number = INITIAL_COLUMNS_NUMBER
    initial_db_rows = connection.select_all_from_cookie()

    test_links = get_shuffle_list(test_links, test_links_number)
    runner = SeleniumRunner(connection=connection, proxy=PROXY_TEST_MODE)
    pool = PoolProcess(runner=runner, links_list=test_links, process_limit=ACTIVE_PROCESS_NUMBER)
    pool.start_pool()

    updated_db_rows = connection.select_all_from_cookie()

    assert_cookie_after_test(initial_db_rows, updated_db_rows)


@pytest.mark.main_run_test
# @pytest.mark.skip(reason='Heavy test with Selemium')
def test_pool_work_with_database_and_real_url(connection):
    initial_db_rows = connection.select_all_from_cookie()

    request = NewsRequest(TEST_URL, proxy=PROXY_TEST_MODE)
    links = request.news_extraction()
    shuffle_links = get_shuffle_list(links, INITIAL_COLUMNS_NUMBER)

    runner = SeleniumRunner(connection=connection, proxy=PROXY_TEST_MODE)
    pool = PoolProcess(runner=runner, links_list=shuffle_links, process_limit=ACTIVE_PROCESS_NUMBER)
    pool.start_pool()

    updated_db_rows = connection.select_all_from_cookie()

    assert_cookie_after_test(initial_db_rows, updated_db_rows)


def assert_cookie_after_test(initial_db_rows: list, updated_db_rows: list):
    assert len(initial_db_rows) == len(updated_db_rows)

    for start_row, result_row in zip(initial_db_rows, updated_db_rows):
        # row[2] is cookie
        assert start_row[2] is None
        assert start_row[2] != result_row[2]




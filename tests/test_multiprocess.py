import string
from multiprocess.pool import PoolProcess
from multiprocess.runner import Runner, SeleniumRunner
import random


with open('_test_links.txt', 'r') as f:
    TEST_LINKS = [i.strip() for i in f]


def get_random_string_list():
    return [i+i+i for i in random.sample(string.ascii_letters, 15)]


def test_pool_work_with_test_runner():
    test_url = get_random_string_list()
    runner = TestRunner()

    pool = PoolProcess(
        runner=runner,
        links_list=test_url
    )

    pool.start_pool()
    assert runner.check_pool_work(), 'Error in Pool or Runner work'


def test_pool_work_with_database_and_news_url(connection):
    test_links_number = 1
    connection.init_db(initial_columns_number=test_links_number)
    start_db_data = connection.select_all_from_cookie()
    test_links = random.sample(TEST_LINKS, test_links_number)
    runner = SeleniumRunner(connection=connection, proxy=True)
    pool = PoolProcess(runner=runner, links_list=test_links, process_limit=1)
    pool.start_pool()

    result_db_data = connection.select_all_from_cookie()

    assert len(start_db_data) == len(result_db_data)

    for start_row, result_row in zip(start_db_data, result_db_data):
        # row[2] is cookie
        assert start_row[2] is None
        assert start_row[2] != result_row[2]


class TestRunner(Runner):
    """Test Runner Class for checking pool and runner work"""
    def __init__(self):
        self._final_data = []

    def start(self, id_link_mapping: tuple) -> tuple:
        """Work in single process"""
        id_cookie, url = id_link_mapping
        process_result = (id_cookie, "Success!", url)

        return process_result

    def end(self, response: tuple) -> None:
        """Work after the end of all processes. Save tested data in runner to check after"""
        self._final_data = response

    def check_pool_work(self):
        """"""
        for elem in self._final_data:
            if len(elem) != 3:
                return False
        return True

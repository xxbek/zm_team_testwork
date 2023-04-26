import string
import random
import os.path
from multiprocess.pool import PoolProcess
from multiprocess.runner import SeleniumRunner
from db.database import DataSQLite


def get_random_url_list():
    return [i+i+i for i in random.sample(string.ascii_letters, 15)]


def test_pool_work():
    path_to_db = '../test.db'
    con = DataSQLite(path_to_db)
    con.init_db()

    assert os.path.exists(path_to_db)


    # runner = SeleniumRunner(con)
    # pool = PoolProcess(
    #     runner=runner,
    #     links_list=[i for i in get_random_url_list()]
    # )
    #
    # pool.start_pool()


if __name__ == '__main__':
    test_pool_work()

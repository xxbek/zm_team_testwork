import json
import logging
import time
from controller.controller import parse_args
from multiprocess.pool import PoolProcess
from multiprocess.runner import SeleniumRunner
from utils.utils import get_sleep_time, get_shuffle_list, get_file_name_with_date, is_file_exists
from db.database import DataSQLite
from request.parse import NewsRequest


LOG_PATH = './app_log/log'


logging.basicConfig(
    format='%(asctime)s: %(process)d-%(levelname)s: %(message)s',
    level=logging.INFO,
    filemode='w',
    filename=get_file_name_with_date(LOG_PATH)
)


def _get_links(url, proxy):
    request = NewsRequest(url=url, proxy=proxy)
    links = request.news_extraction()
    return links


def _main_process(connection, links, proxy, pool_process_limit):
    single_process_runner = SeleniumRunner(connection=connection, proxy=proxy)
    process_pool = PoolProcess(
        runner=single_process_runner,
        links_list=links,
        process_limit=pool_process_limit)
    process_pool.start_pool()

    # Write result in .txt file
    # output_result('output_result.txt', connection)


if __name__ == "__main__":
    args = parse_args()

    with open(args.setting_path) as f:
        settings = json.load(f)

    frequency = settings['run_per_day']
    db_setting = settings['database']

    path_to_db, db_init_row = db_setting['path_to_db'], db_setting['db_init_row']
    sleep_time = get_sleep_time(frequency)
    try:
        conn = DataSQLite(path_to_db)
        if not is_file_exists(path_to_db):
            conn.init_db(db_init_row)

        news_links = _get_links(url=settings['url'], proxy=settings['proxy'], )
        shuffle_links = get_shuffle_list(news_links, output_list_len=db_init_row)
        while True:
            _main_process(
                connection=conn,
                links=shuffle_links,
                proxy=settings['proxy'],
                pool_process_limit=settings['pool_process_limit']
            )
            time.sleep(sleep_time)
    except KeyboardInterrupt:
        logging.info("Crawling is stopped by user.")



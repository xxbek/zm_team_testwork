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


def main_process(url, proxy, init_rows_number, path_to_db, pool_process_limit):
    connection = DataSQLite(path_to_db)
    if not is_file_exists(path_to_db):
        connection.init_db(init_rows_number)
    request = NewsRequest(url=url, proxy=proxy)
    links = request.news_extraction()
    shuffle_links = get_shuffle_list(links, output_list_len=init_rows_number)

    single_process_runner = SeleniumRunner(connection=connection, proxy=proxy)
    process_pool = PoolProcess(
        runner=single_process_runner,
        links_list=shuffle_links,
        process_limit=pool_process_limit)
    process_pool.start_pool()

    # TODO Написать тест на то, что куки будут перезаписываться. Сделать тут нормальный вывод
    with open('run_db_result.txt', 'a') as file:
        result = connection.select_all_from_cookie()
        file.write(str(result))


if __name__ == "__main__":
    args = parse_args()

    with open(args.setting_path) as f:
        settings = json.load(f)

    frequency = settings['run_per_day']
    db_setting = settings['database']
    sleep_time = get_sleep_time(frequency)

    try:
        while True:
            main_process(
                url=settings['url'],
                proxy=bool(settings['proxy']),
                init_rows_number=db_setting['db_init_row'],
                path_to_db=db_setting['path_to_db'],
                pool_process_limit=settings['pool_process_limit']
            )
            time.sleep(sleep_time)
    except KeyboardInterrupt:
        logging.info("Crawling is stopped by user.")









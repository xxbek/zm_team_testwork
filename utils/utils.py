import string
from datetime import datetime, timedelta
import random
import os


def get_current_time():
    """Utils function for getting current time"""
    return datetime.now().strftime('%Y-%m-%d_%H:%M:%S')


def get_sleep_time(frequency):
    now = datetime.today()
    next_run_time = now + timedelta(days=1)
    delta = next_run_time - now
    sleep_time = delta.total_seconds() / frequency
    return sleep_time


def get_shuffle_list(input_list: list, output_list_len: int) -> list:
    return random.sample(input_list, output_list_len)


def get_file_name_with_date(file_path):
    return datetime.now().strftime(f'{file_path}_{get_current_time()}.log')


def remove_file(path_to_file: str) -> None:
    os.remove(path_to_file)


def is_file_exists(path: str) -> bool:
    return os.path.exists(path)


def get_random_string_list():
    return [i+i+i for i in random.sample(string.ascii_letters, 15)]


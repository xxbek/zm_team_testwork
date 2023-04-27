import multiprocessing
import random
import string
from sqlite3 import Connection
from multiprocess.runner import Runner, SeleniumRunner


class PoolProcess:
    """Class for multiprocessing pool logic"""
    def __init__(self, runner: Runner, links_list: list, process_limit=5):
        self._runner = runner
        self._process_limit = process_limit
        self._random_links_list = random.sample(links_list, len(links_list))

        self._id_cookie_link_mapping = self.create_cookie_and_url_tuple()

    def create_cookie_and_url_tuple(self):
        """Link the id in the database and a specific site url:
        (id_cookie, news_url)
        """
        return [(i + 1, link) for i, link in enumerate(self._random_links_list)]

    def start_pool(self):
        """In pool every runner runs function `start`, which launches selenium."""
        with multiprocessing.Pool(self._process_limit) as p:
            p.map_async(self._runner.start, self._id_cookie_link_mapping, callback=self._runner.end)
            p.close()
            p.join()



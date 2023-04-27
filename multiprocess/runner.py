from abc import ABC, abstractmethod
from db.database import DataConnection
from webdriver.browser import SeleniumPage, get_default_web_driver_type
from utils.utils import get_current_time


class Runner(ABC):
    """Interface for all runners. Runners start in every single process"""
    @abstractmethod
    def start(self, id_cookie_and_link):
        pass

    @abstractmethod
    def end(self, response):
        pass


class SeleniumRunner(Runner):
    """Runner that work with Selenium web driver
    Function `start` saves cookie and returns a tuple(id_cookie, cookie)
    Function `end` collects all tuples from every process and save data in DB.
    """
    def __init__(self,  connection: DataConnection, web_driver: SeleniumPage = None, proxy: bool = False, delay=None):
        self._connection = connection
        self._web_driver_type = web_driver or get_default_web_driver_type()
        self._selenium_page = None
        self._proxy = proxy
        self._delay = delay

    def start(self, id_link_mapping: tuple) -> tuple:
        id_cookie, url = id_link_mapping
        db_cookie = self._connection.get_cookie_info_by_id(id_cookie)[0]

        self._selenium_page = self._web_driver_type(url=url, cookie=db_cookie, proxy=self._proxy, delay=self._delay)
        url_cookie = self._selenium_page.get_cookie_from_link()
        id_cookie_mapping = (id_cookie, url_cookie)
        return id_cookie_mapping

    def end(self, response: list[int, list]) -> None:
        for id_cookie, cookie in response:
            update_info = (str(cookie), get_current_time())
            self._connection.update_cookie_record(id_cookie, update_info)





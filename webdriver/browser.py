import logging
from abc import ABC, abstractmethod
from seleniumwire import webdriver
from selenium.common import exceptions
from request.proxy import Proxy, ScrapingBeeProxy


class SeleniumPage(ABC):
    @abstractmethod
    def get_cookie_from_link(self):
        pass


class ChromePage:
    """Class for Selenium web browser manipulation"""

    def __init__(self, url, timeout=5, proxy: bool = False, cookie=None):
        self._proxy_url = ScrapingBeeProxy.PROXIES_URL if proxy else dict()
        self._browser = webdriver.Chrome(seleniumwire_options={'proxy': self._proxy_url})
        self.url = url
        self._browser.implicitly_wait(timeout)
        self._cookie = cookie

        # TODO implement connection for delay and speed
        self._delay = 7

    def _open_url(self) -> None:
        self._browser.get(self.url)

    def _set_cookie(self) -> None:
        try:
            self._browser.add_cookie(self._cookie)
        except exceptions.InvalidCookieDomainException as e:
            logging.error(e)

    def get_cookie_from_link(self, delay):
        if self._cookie is not None:
            self._set_cookie()
        self._open_url()
        self._scroll_page(speed=self._delay)
        self._browser.close()
        return self._browser.get_cookies()

    def _scroll_page(self, speed=8):
        current_position, new_height = 0, 1
        while current_position <= new_height:
            current_position += speed
            self._browser.execute_script("window.scrollTo(0, {});".format(current_position))
            new_height = self._browser.execute_script("return document.body.scrollHeight")

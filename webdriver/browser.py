import logging
import random
import time
from abc import ABC, abstractmethod
from seleniumwire import webdriver
from selenium.common import exceptions
from request.proxy import get_proxy_object
from selenium.common.exceptions import TimeoutException


def get_default_web_driver_type():
    return ChromePage


class SeleniumPage(ABC):
    @abstractmethod
    def get_cookie_from_link(self):
        pass


class ChromePage(SeleniumPage):
    """Class for Selenium web browser manipulation"""

    def __init__(self, url, timeout=20, proxy: bool = False, cookie=None, delay=None):
        self.url = url
        self._cookie = cookie
        self._proxy_object = get_proxy_object(proxy)
        self._proxy_urls = self._proxy_object.PROXY_URLS if self._proxy_object else {}
        self._browser = webdriver.Chrome(seleniumwire_options={'proxy': self._proxy_urls})
        self._browser.set_page_load_timeout(timeout)

        # Random by default
        self._delay = delay or random.randint(1, 5)

    def _open_url(self) -> None:
        self._browser.get(self.url)

    def _set_cookie(self) -> None:
        try:
            self._browser.add_cookie(self._cookie)
        except exceptions.InvalidCookieDomainException as e:
            logging.error(e)

    def get_cookie_from_link(self):
        """In case of TimeoutException return empty cookie"""

        # TODO При наличии куки он их переиспользует, а нужно обновлять!
        if self._cookie is not None:
            self._set_cookie()
        try:
            self._open_url()
            self._scroll_page()
        except TimeoutException:
            logging.error(f'Failed to get information from the site {self.url}')
            return []

        cookie = self._browser.get_cookies()
        return cookie

    def _scroll_page(self, speed=8):
        current_position, new_height = 0, 1
        timer = time.monotonic()
        while current_position <= new_height:
            current_position += speed
            self._browser.execute_script("window.scrollTo(0, {});".format(current_position))
            new_height = self._browser.execute_script("return document.body.scrollHeight")

            if time.monotonic() - timer > self._delay:
                break

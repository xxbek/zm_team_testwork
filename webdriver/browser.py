from seleniumwire import webdriver
from selenium.common import exceptions
import logging
import random


class ChromePage:
    """Class for Selenium web browser manipulation"""
    def __init__(self, url, browser=None, timeout=5, cookie=None, proxy=None):

        # TODO find optional way to implement proxy
        # self._proxy = proxy if proxy else ''
        # self._browser = browser or webdriver.Chrome(options=Options().add_argument('--proxy-server=%s' % self._proxy))

        self._proxy = proxy if proxy else ''
        self._browser = browser or webdriver.Chrome(seleniumwire_options=proxy)
        self.url = url
        self._browser.implicitly_wait(timeout)
        self._cookie = cookie or None

    def open_url(self):
        self._browser.get(self.url)

    def _set_cookie(self):
        try:
            self._browser.add_cookie(self._cookie)
        except exceptions.InvalidCookieDomainException as e:
            logging.error(e)

    def get_cookie_from_link(self, delay):
        if self._cookie is not None:
            self._set_cookie()
        self.open_url()
        self._scroll_page(delay)
        return self._browser.get_cookies()

    def _scroll_page(self, speed=8):
        current_position, new_height = 0, 1
        while current_position <= new_height:
            current_position += speed
            self._browser.execute_script("window.scrollTo(0, {});".format(current_position))
            new_height = self._browser.execute_script("return document.body.scrollHeight")



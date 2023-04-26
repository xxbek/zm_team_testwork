from webdriver.browser import ChromePage

TEST_URL = 'https://dzen.ru/'


def test_cookie_getting_from_chrome_page():
    page = ChromePage(url=TEST_URL, proxy=False)
    cookie = page.get_cookie_from_link()

    assert isinstance(cookie, list) or isinstance(cookie, dict)
    assert len(cookie) > 0




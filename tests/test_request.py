from request.parse import NewsRequest
from tests.conftest import PROXY_TEST_MODE

TEST_URL = 'http://news.google.com', 'http://lenta.ru'


def test_google_news_request():
    req = NewsRequest(TEST_URL[1], proxy=PROXY_TEST_MODE)
    links = req.news_extraction()

    assert len(links) > 0

    for link in links:
        assert isinstance(link, str)
        assert 'http' in link
        # assert requests.get(link).status_code == '200'



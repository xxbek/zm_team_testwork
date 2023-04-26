import logging

from request.parse import NewsRequest


TEST_URL = 'https://news.google.com'


def test_google_news_request():
    req = NewsRequest(TEST_URL, proxy=False)
    links = req.news_extraction()

    assert len(links) > 0



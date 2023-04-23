import requests
from requests import Response
from request.extraction import RegExpressionExtraction
from request.proxy import Proxy


class NewsRequest:
    """Class for news site parsing.
    :param url: main URL for news site.
    :param proxy_object: (optional) Mapping class to the URL of the proxy.
    """

    def __init__(self, url, proxy_object=Proxy):
        self.url = url
        self.proxy_object = proxy_object

    def _get_response_object(self, url=None) -> Response:
        response = requests.get(
            url=url or self.url,
            proxies=self.proxy_object.PROXIES_URL,
            verify=False if self.proxy_object else True,
        )

        return response

    def _create_absolute_link(self, relative_link: str) -> str:
        return self.url + relative_link

    def news_extraction(self, extraction_method=RegExpressionExtraction) -> list:
        """Extract links to another news sites from news aggregator"""
        response = self._get_response_object()
        body_str = response.content.decode()
        extractor = extraction_method(body_str)
        article_link = extractor.extract_article_urls()
        article_abs_link = [self._create_absolute_link(relative_link) for relative_link in article_link]

        return article_abs_link

import logging
import requests
from requests import Response
from request.extraction import PREFERRED_EXTRACTION_URL_METHOD_MAPPING
from request.proxy import get_proxy_object


class NewsRequest:
    """Class for news site parsing.
    :param url: main URL for news site.
    :param proxy: (optional) Key for proxy using.
    """
    def __init__(self, url, proxy: bool = False):
        self.url = url
        self._proxy_object = get_proxy_object(proxy)
        self._proxy_urls = self._proxy_object.PROXY_URLS if self._proxy_object else {}
        self._extractor = self._get_extractor

    def _get_response_object(self) -> Response:
        response = ''
        try:
            response = requests.get(
                url=self.url,
                proxies=self._proxy_urls,
                verify=False
            )
        except requests.exceptions.HTTPError as errh:
            logging.error(f"Http Error: {errh}", )
        except requests.exceptions.ConnectionError as errc:
            logging.error(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            logging.error(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            logging.error(f"OOps: Something Else {err}")
        except Exception as e:
            logging.error(f"Exception: {e}")

        return response

    def _create_absolute_link(self, relative_link: str) -> str:
        return self.url + relative_link

    def _get_extractor(self, body_html):
        extraction_method = PREFERRED_EXTRACTION_URL_METHOD_MAPPING.get(self.url)
        assert extraction_method is not None, \
            'The site is not in the list of available sites.' \
            'Check request.extraction.PREFERRED_EXTRACTION_URL_METHOD_MAPPING'

        return extraction_method(body_html)

    def news_extraction(self) -> list:
        """Extract links to another news sites from news aggregator"""
        response = self._get_response_object()
        body_html = response.content.decode() if response else ''
        extractor = self._get_extractor(body_html)
        article_link = extractor.extract_article_urls()
        article_abs_link = [self._create_absolute_link(relative_link) for relative_link in article_link]

        return article_abs_link

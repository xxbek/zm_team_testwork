import re
from abc import ABC, abstractmethod

AVAILABLE_SITES = (
    "https://news.google.com",
    "https://dzen.ru/news"
)


class ExtractionMethod(ABC):
    """Common class for all parsing methods"""

    def __init__(self, initial_html: str):
        self.initial_html = initial_html

    @abstractmethod
    def extract_article_urls(self):
        pass


class REGoogleNewsExtraction(ExtractionMethod):
    """A method for html extraction using regular expression for news.google.com

        ### lxml library is preferred, but it's outside the standard library
        """

    def _get_article_tags_body(self) -> list:
        articles_list_body = re.findall('<article(.*?)</article>', self.initial_html)
        return articles_list_body

    @staticmethod
    def _get_tag_a_from_article(article_body_list: list):
        list_tags_a = [re.search('<a(.*?)</a>', article).group() for article in article_body_list]
        return list_tags_a

    @staticmethod
    def _get_article_link_from_tag_a(a_body_list: list):
        article_link_list = [re.findall(r'href=.[\'"]?([^\'" >]+)', tag_a)[0] for tag_a in a_body_list]
        return article_link_list

    @staticmethod
    def fix_article_links(article_links: list) -> list:
        return [link.replace(";", "&") for link in article_links]

    def extract_article_urls(self) -> list:
        """Extract links from html"""

        article_tag_list = self._get_article_tags_body()
        tag_a_list = self._get_tag_a_from_article(article_tag_list)
        article_link = self._get_article_link_from_tag_a(tag_a_list)

        return self.fix_article_links(article_link)


PREFERRED_METHODS = {
    "https://news.google.com": REGoogleNewsExtraction,
    "https://dzen.ru/news": ExtractionMethod,
}


EXTRACTION_URL_METHOD_MAPPING = {
    site: PREFERRED_METHODS[site] for site in AVAILABLE_SITES
}



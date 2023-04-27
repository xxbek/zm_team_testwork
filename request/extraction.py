import re
from abc import ABC, abstractmethod


class ExtractionMethod(ABC):
    """Common class for all parsing methods"""

    def __init__(self, initial_html: str):
        self.initial_html = initial_html

    @abstractmethod
    def extract_article_urls(self):
        pass


class LXMLExtraction(ExtractionMethod):
    """lxml library is preferred, but it's outside the standard library"""
    def extract_article_urls(self):
        pass


class REExtraction(ExtractionMethod):
    def _get_inner_tags_body(self, tag_name) -> list:
        """Return list with elements inside all `tag_name` body

        <tag_name>123</tag_name> ... <tag_name>456</tag_name> ---> [123, 456]
        """

        tag_list_body = re.findall(f'<{tag_name}(.*?)</{tag_name}>', self.initial_html)
        return tag_list_body

    @staticmethod
    def fix_article_links(article_links: list) -> list:
        """Fix error in URL link when it is `;` instead `&`"""
        return [link.replace(";", "&") for link in article_links]

    @staticmethod
    def _get_link_from_tag_a_list(a_body_list: list) -> list:
        """  [<a> href="foo.com" </a>, ] ---> [ "foo.com", ]"""
        article_link_list = [re.findall(r'href=.[\'"]?([^\'" >]+)', tag_a)[0] for tag_a in a_body_list]
        return article_link_list

    def extract_article_urls(self):
        pass


class REGoogleNewsExtraction(REExtraction):
    """A method for html extraction using regular expression for news.google.com"""

    @staticmethod
    def _get_tag_a_from_article(article_body_list: list) -> list:
        """[<article> <a href="" /a> </<article>] ---> [ href="" ]"""
        list_tags_a = [re.search('<a(.*?)/a>', article).group() for article in article_body_list]
        return list_tags_a

    def extract_article_urls(self) -> list:
        """Extract links from html"""

        article_tag_list = self._get_inner_tags_body('article')
        tag_a_list = self._get_tag_a_from_article(article_tag_list)
        article_link = self._get_link_from_tag_a_list(tag_a_list)

        return self.fix_article_links(article_link)


class RELentaExtraction(REExtraction):
    @staticmethod
    def _get_link_from_section(section_body_list: list) -> list:
        """ [<section>  <a href="/news/20..."/a>  </section>] --->   [/news/20..., ]"""
        pattern = '/news/'
        row_article_link_list = [re.findall(r'href="/news.[\'"]?([^\'" >]+)', tag_a) for tag_a in section_body_list]
        united_article_list = sum(row_article_link_list, [])
        article_link_list = [pattern + link for link in united_article_list]

        return article_link_list

    def extract_article_urls(self):
        main_page_sections_list = self._get_inner_tags_body("section")
        article_link = self._get_link_from_section(main_page_sections_list)
        return article_link


# TODO find better way to map
PREFERRED_EXTRACTION_URL_METHOD_MAPPING = {
    "https://news.google.com": REGoogleNewsExtraction,
    "http://news.google.com": REGoogleNewsExtraction,
    "http://lenta.ru": RELentaExtraction,
}




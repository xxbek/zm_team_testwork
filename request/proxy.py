from abc import ABC


class Proxy(ABC):
    """Common class for proxy. Using when proxy=False and return empty proxy_url"""
    API_KEY = str()
    PROXY_URLS = dict()


class ScrapingBeeProxy(Proxy):
    """ScrapingBeeProxy proxy class.
    https://app.scrapingbee.com
    """

    API_KEY = '***'

    PROXY_URLS = {
        "http": f"http://{API_KEY}:render_js=False&premium_proxy=True@proxy.scrapingbee.com:8886",
        "https": f"https://{API_KEY}:render_js=False&premium_proxy=True@proxy.scrapingbee.com:8886",
        "verify_ssl": False,
    }


def get_proxy_object(key: bool) -> type(Proxy):
    """The app proxy is specified here"""
    return ScrapingBeeProxy if key else Proxy


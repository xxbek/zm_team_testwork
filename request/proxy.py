from abc import ABC


class Proxy(ABC):
    """Common class for proxy"""
    API_KEY = str()
    PROXY_URLS = dict()


class ScrapingBeeProxy(Proxy):
    """ScrapingBeeProxy proxy class.
    https://app.scrapingbee.com
    """

    API_KEY = 'RELSTBLAYI3SBC0PGSQ7PE8GP8J75JP1SN6H3B67D09NZ0O6PG191D2MLC3XAPHIJLUX8PWVMKJZWXCY'

    PROXY_URLS = {
        "http": f"http://{API_KEY}:render_js=False&premium_proxy=True@proxy.scrapingbee.com:8886",
        "https": f"https://{API_KEY}:render_js=False&premium_proxy=True@proxy.scrapingbee.com:8886",
        "verify_ssl": False,
    }


def get_proxy_object(key: bool) -> type(Proxy):
    """The app proxy is specified here"""
    return ScrapingBeeProxy if key else Proxy


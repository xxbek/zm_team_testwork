from abc import ABC


class Proxy(ABC):
    """Common class for proxy"""
    API_KEY = str
    PROXY_URLS = dict


def get_proxy_object() -> Proxy:
    return ScrapingBeeProxy()


class ScrapingBeeProxy(Proxy):
    """ScrapingBeeProxy proxy class.
    https://app.scrapingbee.com
    """
    # API_KEY = '03JU6ZYBH4FUDZZFE42GTWNMC8JU52G4643OQ2OSHK6HSP4707OEQ57ZVRYT54XVUGZ1JF8QO8KWF475'
    API_KEY = 'RELSTBLAYI3SBC0PGSQ7PE8GP8J75JP1SN6H3B67D09NZ0O6PG191D2MLC3XAPHIJLUX8PWVMKJZWXCY'

    PROXY_URLS = {
        "http": f"http://{API_KEY}:render_js=False&premium_proxy=True@proxy.scrapingbee.com:8886",
        "https": f"https://{API_KEY}:render_js=False&premium_proxy=True@proxy.scrapingbee.com:8886",
        "verify_ssl": False,
    }



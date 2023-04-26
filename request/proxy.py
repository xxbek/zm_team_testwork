from abc import ABC


class Proxy(ABC):
    """Common class for proxy"""
    API_KEY = str
    PROXIES_URL = dict


class ScrapingBeeProxy(Proxy):
    """ScrapingBeeProxy proxy class.
    https://app.scrapingbee.com
    """
    API_KEY = '03JU6ZYBH4FUDZZFE42GTWNMC8JU52G4643OQ2OSHK6HSP4707OEQ57ZVRYT54XVUGZ1JF8QO8KWF475'

    PROXIES_URL = {
        "http": f"http://{API_KEY}:render_js=False&premium_proxy=True@proxy.scrapingbee.com:8886",
        # "verify_ssl": False,
    }



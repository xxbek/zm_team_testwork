import random
from request.parse import NewsRequest
from request.proxy import ScrapingBeeProxy
from webdriver.browser import ChromePage
URL = "https://news.google.com"


# links = NewsRequest(url=URL, proxy_object=ScrapingBeeProxy).news_extraction()

# link = random.choice(links)
link = 'https://ru.wikipedia.org/wiki'
news_page = ChromePage(url=link, proxy=False)
delay = 3
cookie = news_page.get_cookie_from_link(delay)






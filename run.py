from request.parse import NewsRequest
from request.proxy import ScrapingBeeProxy

URL = "https://news.google.com"


links = NewsRequest(URL, ScrapingBeeProxy).news_extraction()

print()


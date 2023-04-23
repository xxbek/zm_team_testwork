from request.parse import NewsRequest
from request.proxy import ScrapingBeeProxy

url = "https://news.google.com"


links = NewsRequest(url, ScrapingBeeProxy).news_extraction()

print()


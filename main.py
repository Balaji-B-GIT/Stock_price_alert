import requests
import os
from dotenv import load_dotenv
from newsapi import NewsApiClient
load_dotenv("C:/Python/Environmental variables/.env")
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_URL = "https://www.alphavantage.co/query"
parameters = {
    "function" : "TIME_SERIES_DAILY",
    "symbol" : STOCK,
    "apikey":os.getenv("stock_api_key"),
    "outputsize":"compact"
}


response = requests.get(url = STOCK_URL,params=parameters)
response.raise_for_status()
data = response.json()

newsapi = NewsApiClient(api_key=os.getenv("news_api_key"))
top_headlines = newsapi.get_top_headlines(q="Microsoft")
print(top_headlines)



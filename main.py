import requests
import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv("C:/Python/Environmental variables/.env")
STOCK = "TSLA"
COMPANY_NAME = "Tesla"
STOCK_URL = "https://www.alphavantage.co/query"

stock_parameters = {
    "function" : "TIME_SERIES_DAILY",
    "symbol" : STOCK,
    "apikey":os.getenv("stock_api_key"),
    "outputsize":"compact"
}

stock_response = requests.get(url = STOCK_URL,params=stock_parameters)
stock_response.raise_for_status()
stock_data = stock_response.json()
data = stock_data["Time Series (Daily)"]
listed_data = list(data.values())
day1_close = float(listed_data[0]["4. close"])
day2_close = float(listed_data[1]["4. close"])

change_percentage = round((day1_close-day2_close)/day1_close * 100)

print(change_percentage)
if change_percentage > 0:
    indicator = "🔺"
else:
    indicator = "🔻"

if abs(change_percentage) >= 5:
    news_parameters = {
        "apikey": os.getenv("news_api_key"),
        "q": COMPANY_NAME,
        "language":"en",
    }
    news_response = requests.get(url="https://newsapi.org/v2/everything", params=news_parameters)
    news_response.raise_for_status()
    news_data = news_response.json()
    news = news_data["articles"][:3]
    top_three_news = [f"{COMPANY_NAME} {change_percentage}{indicator}. \nTitle : {article['title']}.\n"
                       f"Brief : {article['description']}" for article in news]

    for article in top_three_news:
        print(article)
        client = Client(os.getenv("account_sid"), os.getenv("auth_token"))
        message = client.messages.create(
            from_=os.getenv("from_"),
            to=os.getenv("to"),
            body = article
        )
# newsapi_fetcher.py

import os
import requests
from datetime import datetime
import pytz

def fetch_newsapi_articles(query="nifty OR sensex OR bank nifty", limit=5):
    api_key = os.getenv("NEWSAPI_KEY")
    if not api_key:
        print("❌ NEWSAPI_KEY not found in environment.")
        return []

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": limit,
        "apiKey": api_key,
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        tz = pytz.timezone("Asia/Kolkata")
        articles = []
        for article in data.get("articles", []):
            published_at = datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
            published_at = published_at.replace(tzinfo=pytz.utc).astimezone(tz)

            articles.append({
                "title": article["title"],
                "link": article["url"],
                "source": article["source"]["name"],
                "timestamp": published_at
            })

        return articles

    except Exception as e:
        print(f"❌ NewsAPI fetch error: {e}")
        return []

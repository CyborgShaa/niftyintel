# nifty_news_fetcher.py

import feedparser
from datetime import datetime
import pytz

# RSS feed sources (feel free to expand)
NIFTY_RSS_FEEDS = [
    "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
    "https://www.moneycontrol.com/rss/MCtopnews.xml",
    "https://www.livemint.com/rss/markets",
]

def fetch_nifty_news(limit_per_feed=5):
    all_articles = []
    tz = pytz.timezone("Asia/Kolkata")

    for url in NIFTY_RSS_FEEDS:
        feed = feedparser.parse(url)

        for entry in feed.entries[:limit_per_feed]:
            try:
                published = entry.get("published", "") or entry.get("updated", "")
                timestamp = datetime.strptime(published, "%a, %d %b %Y %H:%M:%S %Z")
                timestamp = tz.localize(timestamp)
            except Exception:
                timestamp = datetime.now(tz)

            article = {
                "title": entry.title,
                "link": entry.link,
                "source": feed.feed.get("title", "Unknown"),
                "timestamp": timestamp
            }

            all_articles.append(article)

    return all_articles

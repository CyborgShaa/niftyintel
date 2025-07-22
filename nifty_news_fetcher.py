# news_fetcher.py

import feedparser
from datetime import datetime
import pytz

tz = pytz.timezone("Asia/Kolkata")

# ✅ Reliable sources for Indian market/index news
RSS_FEEDS = {
    "Economic Times Markets": "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
    "Moneycontrol Markets": "https://www.moneycontrol.com/rss/MCtopnews.xml",
    "Business Standard": "https://www.business-standard.com/rss/markets-106.rss",
    "Livemint Markets": "https://www.livemint.com/rss/market",
    "Bloomberg Quint": "https://www.bqprime.com/markets/rss",
    "CNBC TV18": "https://www.cnbctv18.com/rss/marketnews.xml",
    "Zee Business": "https://zeenews.india.com/rss/business.xml",
    "https://www.thehindubusinessline.com/markets/rss/",
    "https://in.investing.com/rss/market_overview.rss",
    "https://www.financialexpress.com/market/feed/",
    "Google News": "https://news.google.com/rss/search?q=nifty+stock+market+india"
}

# ✅ Only accept news that includes these keywords
NIFTY_KEYWORDS = [
    "nifty", "nifty50", "nifty 50", "bank nifty", "sensex", "index",
    "indices", "market crash", "bull market", "bear market", "india vix",
    "gap up", "gap down", "SGX Nifty", "fii", "dii", "option chain",
    "futures", "expiry", "rbi", "inflation", "repo rate", "gdp", "bond yield",
    "us inflation", "global cues", "fomc"
]

def fetch_nifty_news(limit_per_feed=5):
    all_articles = []

    for source, url in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:limit_per_feed]:
                title = entry.title.strip()
                link = entry.link.strip()
                published = entry.get("published", "") or entry.get("pubDate", "")
                description = entry.get("summary", "").strip()

                # Convert to datetime object
                try:
                    timestamp = datetime(*entry.published_parsed[:6], tzinfo=pytz.utc).astimezone(tz)
                except Exception:
                    continue  # skip if time can't be parsed

                # ✅ Keyword filtering
                if any(keyword in title.lower() for keyword in NIFTY_KEYWORDS):
                    all_articles.append({
                        "title": title,
                        "link": link,
                        "timestamp": timestamp,
                        "description": description,
                        "source": source
                    })

        except Exception as e:
            print(f"❌ Failed to parse {source}: {e}")

    return all_articles

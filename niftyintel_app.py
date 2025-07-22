# niftyintel_app.py

import streamlit as st
from datetime import datetime
import pytz
import time

from nifty_news_fetcher import fetch_nifty_news
from summarizer import analyze_news
from telegram_alerts import send_telegram_alert

# Timezone for India
tz = pytz.timezone("Asia/Kolkata")
current_time = datetime.now(tz).strftime('%b %d, %I:%M %p')

# Streamlit app setup
st.set_page_config(page_title="NiftyIntel News Engine", layout="centered")
st.title("📈 NiftyIntel - Index Market News")
st.markdown("Get live and impactful Nifty-related market news in one place.")
st.caption(f"🔄 Last updated: {current_time}")
st.divider()

# How old news can be (in minutes)
NEWS_AGE_LIMIT = 60
AUTO_REFRESH_MINUTES = 5

# Fetch and sort news
news_data = fetch_nifty_news(limit_per_feed=5)
news_data = sorted(news_data, key=lambda x: x["timestamp"], reverse=True)

# Filter recent articles
news_data = [
    n for n in news_data
    if (datetime.now(tz) - n["timestamp"]).total_seconds() <= NEWS_AGE_LIMIT * 60
]

# Track alerts
if "alerted_titles" not in st.session_state:
    st.session_state.alerted_titles = set()

# Emoji for sentiment
impact_emojis = {
    "Bullish": "🟢",
    "Bearish": "🔴",
    "Neutral": "⚪"
}

# Display & alert
for news in news_data:
    summary, impact = analyze_news(news["title"])

    if news["title"] not in st.session_state.alerted_titles:
        message = (
            f"📣 *{news['title']}*\n"
            f"🧠 {summary or 'No summary'}\n"
            f"{impact_emojis.get(impact, '⚪')} *Impact*: {impact or 'Neutral'}\n"
            f"🕒 {news['timestamp'].strftime('%b %d, %I:%M %p')} | 📰 {news['source']}\n"
            f"🔗 {news['link']}"
        )
        send_telegram_alert(message)
        st.session_state.alerted_titles.add(news["title"])

    # Show in UI
    st.markdown(f"### {impact_emojis.get(impact, '⚪')} [{news['title']}]({news['link']})")
    st.caption(f"🕒 {news['timestamp'].strftime('%b %d, %I:%M %p')} | 📰 {news['source']}")
    st.markdown(f"**Summary**: {summary or 'N/A'}")
    st.markdown("---")

# Manual alert button
if st.button("Send Test Alert"):
    send_telegram_alert("📣 Test alert from NiftyIntel")

# Auto refresh every X mins
time.sleep(AUTO_REFRESH_MINUTES * 60)
st.experimental_rerun()

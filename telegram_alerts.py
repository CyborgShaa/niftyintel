# telegram_alerts.py

import os
import requests
from dotenv import load_dotenv

# Load environment variables (for local testing or secrets)
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_alert(message: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Telegram credentials missing.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print(f"✅ Alert sent to Chat ID: {TELEGRAM_CHAT_ID}")
        else:
            print(f"❌ Telegram Error: {response.status_code} → {response.text}")
    except Exception as e:
        print(f"❌ Exception sending alert: {e}")

# telegram_alerts.py

import os
import requests
from dotenv import load_dotenv

# Load env vars (for local testing or secrets)
load_dotenv()

def send_telegram_alert(message: str):
    for i in [1, 2, 3]:  # Supports up to 3 bot+chat combos
        token = os.getenv(f"TELEGRAM_BOT_TOKEN_{i}")
        chat_id = os.getenv(f"TELEGRAM_CHAT_ID_{i}")

        if not token or not chat_id:
            print(f"⚠️ Bot {i} not configured. Skipping.")
            continue

        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }

        try:
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                print(f"✅ Alert sent via Bot {i}")
            else:
                print(f"❌ Telegram Error (Bot {i}): {response.text}")
        except Exception as e:
            print(f"❌ Exception for Bot {i}: {e}")

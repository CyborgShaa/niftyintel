# summarizer.py

import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_news(title, description=None):
    prompt = f"""
You are a stock market analyst. Analyze the following headline and give:
1. A one-line summary of the event.
2. Its expected impact on Nifty 50 (Bullish / Bearish / Neutral).

Title: "{title}"
Description: "{description or 'N/A'}"

Respond in this exact format:
Summary: <short summary>
Impact: <Bullish/Bearish/Neutral>
"""

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        output = response.text.strip()

        summary_line = ""
        impact_tag = "Neutral"

        for line in output.splitlines():
            if line.lower().startswith("summary"):
                summary_line = line.split(":", 1)[1].strip()
            elif line.lower().startswith("impact"):
                impact_tag = line.split(":", 1)[1].strip().capitalize()

        return summary_line, impact_tag

    except Exception as e:
        print(f"❌ Gemini AI summarization failed: {e}")
        return None, "Neutral"

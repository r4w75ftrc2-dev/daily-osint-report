import json
import os
import requests

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def load_articles():
    with open(
        "classified_articles_v2.json",
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)


articles = load_articles()

high = sum(
    1 for a in articles
    if a.get("risk_level") == "HIGH"
)

uav = sum(
    1 for a in articles
    if (
        a.get("region") == "EUROPE"
        and "UAV" in a.get("categories", [])
    )
)

aviation = sum(
    1 for a in articles
    if "AVIATION" in a.get("categories", [])
)

czech = sum(
    1 for a in articles
    if "CZECH" in a.get("categories", [])
)

highest = None

if articles:
    highest = max(
        articles,
        key=lambda x: x.get("risk_score", 0)
    )

headline = ""

if highest:
    headline = highest.get("title", "")

message = f"""🛡 DAILY SECURITY OSINT

🔴 HIGH RISK: {high}
🚁 EU UAV: {uav}
✈️ Aviation: {aviation}
🇨🇿 Czech: {czech}

Nejvýznamnější událost:
{headline}
"""

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

response = requests.post(
    url,
    json={
        "chat_id": CHAT_ID,
        "text": message
    }
)

response.raise_for_status()

print("Telegram notification sent.")

import json
import os
import glob
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


headline = "Bez významné události"

if highest:
    headline = highest.get("title", headline)

try:
    with open(
        "stats.json",
        "r",
        encoding="utf-8"
    ) as f:
        stats = json.load(f)

except Exception:
    stats = {}


collected = stats.get(
    "collected",
    "?"
)

classified = stats.get(
    "classified",
    "?"
)

skipped = stats.get(
    "skipped",
    "?"
)

message = f"""🛡 DAILY SECURITY OSINT
📊 Processing:
RSS articles: {collected}
Classified: {classified}
Skipped: {skipped}

🔴 HIGH RISK: {high}
🚁 EU UAV: {uav}
✈️ Aviation: {aviation}
🇨🇿 Czech: {czech}

Nejvýznamnější událost:
{headline}
"""


# Najde poslední PDF report

pdf_files = glob.glob(
    "reports/*.pdf"
)

pdf_file = None

if pdf_files:
    pdf_file = max(
        pdf_files,
        key=os.path.getmtime
    )


# Odešle text

requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    json={
        "chat_id": CHAT_ID,
        "text": message
    }
).raise_for_status()


# Odešle PDF

if pdf_file:

    with open(pdf_file, "rb") as document:

        response = requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendDocument",
            data={
                "chat_id": CHAT_ID
            },
            files={
                "document": document
            }
        )

        response.raise_for_status()

else:

    print(
        "PDF report nebyl nalezen. "
        "Odeslán pouze textový briefing."
    )


print("Telegram message and PDF sent.")

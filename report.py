import json
from datetime import datetime


def load_articles():
    with open(
        "classified_articles_v2.json",
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)


def create_report(articles):

    today = datetime.now().strftime("%d.%m.%Y")

    report = []

    report.append(
        "# Daily Security OSINT Report\n"
    )

    report.append(
        f"Datum: {today}\n"
    )

    report.append(
        "## HIGH RISK EVENTS\n"
    )

    for article in articles:
        if article.get("risk_level") == "HIGH":

            report.append(
                f"""
### {article['title']}

Kategorie:
{', '.join(article.get('categories', []))}

Klíčová slova:
{', '.join(article.get('keywords', []))}

Zdroj:
{article['link']}

---
"""
            )

    report.append(
        "\n## EUROPE UAV MONITORING\n"
    )

    for article in articles:

        if (
            article.get("region") == "EUROPE"
            and "UAV" in article.get("categories", [])
        ):

            report.append(
                f"""
### {article['title']}

Typ:
{article.get('incident_type', 'UAV')}

Riziko:
{article.get('risk_level', '')}

Skóre:
{article.get('risk_score', '')}

Zdroj:
{article.get('link', '')}

---
"""
            )

    for article in articles:

        report.append(
    f"- {article['title']}\n"
    f"  Kategorie: {', '.join(article.get('categories', []))}\n"
    f"  Riziko: {article.get('risk_level', 'UNKNOWN')}\n"
    f"  Region: {article.get('region', 'UNKNOWN')}\n"
    f"  Zdroj: {article.get('link', '')}\n\n"
)

    with open(
        "daily_report.md",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(
            "\n".join(report)
        )


if __name__ == "__main__":

    articles = load_articles()

    create_report(articles)

    print(
        "Report created: daily_report.md"
    )

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
        "\n## ALL CATEGORIES\n"
    )

    for article in articles:

        report.append(
            f"- {article['title']} "
            f"({', '.join(article.get('categories', []))})\n"
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

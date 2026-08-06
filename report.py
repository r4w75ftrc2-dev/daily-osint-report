import json
from datetime import datetime
from translator import translate_article


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

    report.append("# Daily Security OSINT Report\n")
    report.append(f"Datum: {today}\n")
    
    # ==========================
    # EXECUTIVE SUMMARY
    # ==========================

    high_count = sum(
        1 for a in articles
        if a.get("risk_level") == "HIGH"
    )

    uav_count = sum(
        1 for a in articles
        if (
            a.get("region") == "EUROPE"
            and "UAV" in a.get("categories", [])
        )
    )

    aviation_count = sum(
        1 for a in articles
        if "AVIATION" in a.get("categories", [])
    )

    czech_count = sum(
        1 for a in articles
        if "CZECH" in a.get("categories", [])
    )


    report.append(
        """
## EXECUTIVE SUMMARY

"""
    )

    report.append(
        f"""
🔴 HIGH RISK EVENTS:
{high_count}

🚁 EUROPE UAV MONITORING:
{uav_count}

✈️ AVIATION EVENTS:
{aviation_count}

🇨🇿 CZECH EVENTS:
{czech_count}

"""
    )


    # Nejvýznamnější událost

    highest = None

    if articles:
        highest = max(
            articles,
            key=lambda x: x.get(
                "risk_score",
                0
            )
        )

    if highest:

        highest = translate_article(highest)

        report.append(
            f"""
### Nejvýznamnější událost

{highest.get('title_cs', highest.get('title', ''))}

Riziko:
{highest.get('risk_level', '')}

Skóre:
{highest.get('risk_score', '')}

Zdroj:
{highest.get('link', '')}

---
"""
        )


    # ==========================
    # HIGH RISK
    # ==========================

    report.append(
        "\n## HIGH RISK EVENTS\n"
    )

    high_found = False

    for article in articles:

        if article.get("risk_level") == "HIGH":

            high_found = True

            article = translate_article(article)

            report.append(
                f"""
### {article.get('title_cs', article.get('title', ''))}

Originál:
{article.get('title', '')}

Kategorie:
{', '.join(article.get('categories', []))}

Typ incidentu:
{article.get('incident_type', 'N/A')}

Riziko:
{article.get('risk_level', '')}

Skóre:
{article.get('risk_score', '')}

Region:
{article.get('region', '')}

Zdroj:
{article.get('link', '')}

---
"""
            )

    if not high_found:
        report.append(
            "\nŽádné události s vysokým rizikem.\n"
        )


    # ==========================
    # EUROPE UAV MONITORING
    # ==========================

    report.append(
        "\n## EUROPE UAV MONITORING\n"
    )

    uav_found = False

    for article in articles:

        if (
            article.get("region") == "EUROPE"
            and "UAV" in article.get("categories", [])
        ):

            uav_found = True

            article = translate_article(article)

            report.append(
                f"""
### {article.get('title_cs', article.get('title', ''))}

Originál:
{article.get('title', '')}

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

    if not uav_found:
        report.append(
            "\nŽádné evropské UAV události.\n"
        )


    # ==========================
    # ALL ARTICLES
    # ==========================

    report.append(
        "\n## ALL CATEGORIES\n"
    )

    for article in articles:

        report.append(
            f"""
### {article.get('title', '')}

Kategorie:
{', '.join(article.get('categories', []))}

Riziko:
{article.get('risk_level', '')}

Region:
{article.get('region', '')}

Zdroj:
{article.get('link', '')}

---
"""
        )


        report_text = "\n".join(report)


    # Aktuální report

    with open(
        "daily_report.md",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(report_text)


    # Archivní kopie

    import os

    os.makedirs(
        "reports",
        exist_ok=True
    )

    archive_name = (
        f"reports/"
        f"{datetime.now().strftime('%Y-%m-%d')}"
        f"_report.md"
    )


    with open(
        archive_name,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(report_text)


if __name__ == "__main__":

    articles = load_articles()

    create_report(articles)

    print(
        "Report created: daily_report.md"
    )

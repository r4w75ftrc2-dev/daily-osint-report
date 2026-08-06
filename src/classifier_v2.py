import json
from config import CATEGORIES


EUROPE = [
    "europe",
    "eu",
    "germany",
    "france",
    "poland",
    "austria",
    "slovakia",
    "czech",
    "czech republic",
    "prague",
    "praha",
    "italy",
    "spain",
    "netherlands",
    "belgium",
    "sweden",
    "norway",
    "finland",
    "denmark",
    "uk",
    "united kingdom"
]


UAV_TERMS = [
    "drone",
    "uav",
    "uas",
    "unmanned",
    "quadcopter"
]


AIRPORT_TERMS = [
    "airport",
    "airfield",
    "runway",
    "flight",
    "airspace",
    "aviation"
]


def analyze_article(article):

    text = (
        article.get("title", "")
        + " "
        + article.get("link", "")
    ).lower()

    categories = []
    keywords = []

    score = 0

    # Kategorie
    for category, terms in CATEGORIES.items():
        for term in terms:
            if term.lower() in text:
                categories.append(category)
                keywords.append(term)

    # Evropa
    if any(term in text for term in EUROPE):
        score += 3
        region = "EUROPE"
    else:
        region = "OTHER"

    # UAV incident
    uav = any(term in text for term in UAV_TERMS)
    airport = any(term in text for term in AIRPORT_TERMS)

    if uav:
        categories.append("UAV")

    if uav and airport:
        score += 5
        incident_type = "UAV_AIRPORT_INCIDENT"

    elif uav:
        score += 2
        incident_type = "UAV"

    else:
        incident_type = None


    # Bezpečnost
    if "SECURITY" in categories:
        score += 3


    # Geopolitika
    if "GEOPOLITICS" in categories:
        score += 2


    # Riziko
    if score >= 7:
        risk = "HIGH"

    elif score >= 4:
        risk = "MEDIUM"

    else:
        risk = "LOW"


    article["categories"] = list(set(categories))
    article["keywords"] = list(set(keywords))
    article["region"] = region
    article["incident_type"] = incident_type
    article["risk_score"] = score
    article["risk_level"] = risk

    return article



def main():

    with open(
        "articles.json",
        "r",
        encoding="utf-8"
    ) as f:
        articles = json.load(f)


    result = []

    for article in articles:
        result.append(
            analyze_article(article)
        )


    with open(
        "classified_articles_v2.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            result,
            f,
            ensure_ascii=False,
            indent=4
        )


    print(
        f"Analyzed articles: {len(result)}"
    )


if __name__ == "__main__":
    main()

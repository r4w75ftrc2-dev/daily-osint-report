import json
from config import CATEGORIES


def classify_article(article):
    """
    Přidá kategorii a riziko k jednomu článku.
    """

    text = (
        article.get("title", "") + " "
        + article.get("link", "")
    ).lower()

    categories = []
    matched_keywords = []

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword.lower() in text:
                categories.append(category)
                matched_keywords.append(keyword)

    # odstranění duplicit
    categories = list(set(categories))

    # základní hodnocení rizika
    if "UAV" in categories or "SECURITY" in categories:
        risk = "HIGH"
    elif "AVIATION" in categories or "GEOPOLITICS" in categories:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    article["categories"] = categories
    article["risk_level"] = risk
    article["keywords"] = list(set(matched_keywords))

    return article


def main():

    with open(
        "articles.json",
        "r",
        encoding="utf-8"
    ) as f:
        articles = json.load(f)

    classified = []

    for article in articles:
        classified.append(
            classify_article(article)
        )

    with open(
        "classified_articles.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            classified,
            f,
            ensure_ascii=False,
            indent=4
        )

    print(
        f"Zpracováno článků: {len(classified)}"
    )


if __name__ == "__main__":
    main()

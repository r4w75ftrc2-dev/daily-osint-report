import feedparser

def load_sources(file_path="sources.txt"):
    """Načte RSS adresy ze souboru."""
    sources = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                sources.append(line)
    return sources

def fetch_articles(sources):
    """Stáhne články ze všech RSS zdrojů."""
    articles = []

    for source in sources:
        print(f"Načítám: {source}")
        feed = feedparser.parse(source)

        for entry in feed.entries:
            articles.append({
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
                "source": source
            })

    return articles

if __name__ == "__main__":
    sources = load_sources()
    articles = fetch_articles(sources)

    print("\n==========================")
    print(f"Nalezeno článků: {len(articles)}")
    print("==========================\n")

    for article in articles[:20]:
        print(article["published"])
        print(article["title"])
        print(article["link"])
        print("-" * 60)

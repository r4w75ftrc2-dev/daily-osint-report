import feedparser
import json
from datetime import datetime


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

        try:
            feed = feedparser.parse(source)

            if not hasattr(feed, "entries"):
                print(
                    f"⚠️ Zdroj neobsahuje články: {source}"
                )
                continue

            for entry in feed.entries:
                articles.append({
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "source": source,
                    "collected": datetime.now().isoformat()
                })

        except Exception as e:
            print(
                f"⚠️ Chyba při načítání zdroje {source}: {e}"
            )
            continue

    return articles

import json
from datetime import datetime


def save_stats(count):
    """Uloží statistiku sběru."""

    print(">>> SPOUSTIM save_stats")

    stats = {
        "collected": count,
        "date": datetime.now().strftime("%d.%m.%Y")
    }

    with open(
        "stats.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            stats,
            f,
            ensure_ascii=False,
            indent=4
        )

    print(">>> stats.json ulozen")

def save_articles(articles, filename="articles.json"):
    """Uloží články do JSON souboru."""

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(
            articles,
            f,
            ensure_ascii=False,
            indent=4
        )
    stats = {
        "collected": len(articles),
        "date": datetime.now().strftime("%d.%m.%Y")
    }

    with open(
        "stats.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            stats,
            f,
            ensure_ascii=False,
            indent=4
        )
     print(">>> articles.json ulozen")   
def save_stats(count):
    """Uloží statistiku sběru."""

    stats = {
        "collected": count,
        "date": datetime.now().strftime("%d.%m.%Y")
    }

    with open(
        "stats.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            stats,
            f,
            ensure_ascii=False,
            indent=4
        )
        
if __name__ == "__main__":

    sources = load_sources()

    articles = fetch_articles(sources)

    save_articles(articles)
    
    save_stats(len(articles))
    
    print("\n==========================")
    print(f"Nalezeno článků: {len(articles)}")
    print("Uloženo do articles.json")
    print("==========================")

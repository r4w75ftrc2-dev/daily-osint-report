from deep_translator import GoogleTranslator


def translate_text(text):

    if not text:
        return ""

    try:
        translated = GoogleTranslator(
            source="auto",
            target="cs"
        ).translate(text)

        return translated

    except Exception as e:
        print(
            f"Translation error: {e}"
        )
        return text


def translate_article(article):

    article["title_cs"] = translate_text(
        article.get("title", "")
    )

    return article

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from datetime import datetime
import os


# ==========================
# FONT
# ==========================

pdfmetrics.registerFont(
    TTFont(
        "DejaVu",
        "fonts/DejaVuSans.ttf"
    )
)


def create_pdf():

    date = datetime.now().strftime("%Y-%m-%d")

    os.makedirs(
        "reports",
        exist_ok=True
    )

    filename = (
        f"reports/"
        f"Daily_Security_OSINT_Report_{date}.pdf"
    )


    doc = SimpleDocTemplate(
        filename
    )


    styles = getSampleStyleSheet()

    for style in styles.byName.values():
        style.fontName = "DejaVu"


    story = []


    with open(
        "daily_report.md",
        "r",
        encoding="utf-8"
    ) as f:

        content = f.read()


    for line in content.split("\n"):

        line = line.strip()

        if not line:
            continue


        if line.startswith("#"):

            text = (
                line
                .replace("#", "")
                .strip()
            )

            story.append(
                Paragraph(
                    text,
                    styles["Heading2"]
                )
            )

        else:

            story.append(
                Paragraph(
                    line,
                    styles["BodyText"]
                )
            )


        story.append(
            Spacer(1, 8)
        )


    doc.build(
        story
    )


    print(
        f"PDF created: {filename}"
    )


if __name__ == "__main__":

    create_pdf()

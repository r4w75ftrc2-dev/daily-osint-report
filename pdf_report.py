from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from datetime import datetime
import json
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


def load_articles():

    with open(
        "classified_articles_v2.json",
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



def create_pdf():

    date = datetime.now().strftime("%d.%m.%Y")

    os.makedirs(
        "reports",
        exist_ok=True
    )


    filename = (
        "reports/"
        f"Daily_Security_OSINT_Report_{date}.pdf"
    )


    doc = SimpleDocTemplate(
        filename,
        pagesize=A4
    )


    styles = getSampleStyleSheet()

    for style in styles.byName.values():
        style.fontName = "DejaVu"


    story = []


    articles = load_articles()


    # ==========================
    # TITULNÍ STRANA
    # ==========================

    story.append(
        Paragraph(
            "DAILY SECURITY OSINT REPORT",
            styles["Title"]
        )
    )

    story.append(
        Spacer(1,20)
    )


    story.append(
        Paragraph(
            f"Datum: {date}",
            styles["Heading2"]
        )
    )


    story.append(
        Paragraph(
            "Aviation Security & UAV Monitoring",
            styles["Heading3"]
        )
    )


    story.append(
        Spacer(1,30)
    )


    # ==========================
    # STATISTIKA
    # ==========================

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


    table_data = [
        ["Kategorie", "Počet"],
        ["HIGH RISK", str(high)],
        ["EUROPE UAV", str(uav)],
        ["AVIATION", str(aviation)]
    ]


    table = Table(
        table_data,
        colWidths=[200,80]
    )


    table.setStyle(
        TableStyle(
            [
                ("FONT", (0,0), (-1,-1), "DejaVu"),
                ("GRID", (0,0), (-1,-1), 0.5, None),
            ]
        )
    )


    story.append(table)

    story.append(
        PageBreak()
    )


    # ==========================
    # OBSAH REPORTU
    # ==========================

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
                .replace("#","")
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
            Spacer(1,8)
        )


    doc.build(
        story
    )


    print(
        f"PDF created: {filename}"
    )



if __name__ == "__main__":

    create_pdf()

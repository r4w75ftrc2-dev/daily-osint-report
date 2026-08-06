from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from datetime import datetime

from reportlab.pdfbase import pdfmetrics

from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(
    TTFont(
        "DejaVu",
        "DejaVuSans.ttf"
    )
)

def create_pdf():

    date = datetime.now().strftime("%Y-%m-%d")

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

        if line.startswith("#"):

            text = line.replace("#", "").strip()

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


    doc.build(story)


    print(
        f"PDF created: {filename}"
    )


if __name__ == "__main__":

    create_pdf()

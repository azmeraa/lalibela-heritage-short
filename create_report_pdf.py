
import os
import re
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    HRFlowable, Table, TableStyle, KeepTogether
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(BASE_DIR, "FINAL_REPORT.md")
OUTPUT = os.path.join(BASE_DIR, "outputs", "Lalibela_Final_Report.pdf")

os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

if not os.path.exists(SOURCE):
    raise FileNotFoundError("FINAL_REPORT.md was not found.")

# PURPLE AND PINK COLOR THEME
PURPLE = colors.HexColor("#51266F")
DARK_PURPLE = colors.HexColor("#35164D")
PINK = colors.HexColor("#D66A9F")
LAVENDER = colors.HexColor("#F1E8F7")
PALE_PINK = colors.HexColor("#FCEEF4")
DARK_GREY = colors.HexColor("#3F3744")
MID_GREY = colors.HexColor("#786D7D")
WHITE = colors.white

styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    name="CoverTitle",
    fontName="Helvetica-Bold",
    fontSize=27,
    leading=34,
    alignment=TA_CENTER,
    textColor=DARK_PURPLE,
    spaceAfter=10
))

styles.add(ParagraphStyle(
    name="CoverSubtitle",
    fontName="Helvetica",
    fontSize=14,
    leading=20,
    alignment=TA_CENTER,
    textColor=PURPLE
))

styles.add(ParagraphStyle(
    name="SectionHeading",
    fontName="Helvetica-Bold",
    fontSize=15,
    leading=20,
    textColor=PURPLE,
    spaceBefore=12,
    spaceAfter=7,
    keepWithNext=True
))

styles.add(ParagraphStyle(
    name="SubHeading",
    fontName="Helvetica-Bold",
    fontSize=11,
    leading=15,
    textColor=PINK,
    spaceBefore=8,
    spaceAfter=5,
    keepWithNext=True
))

styles.add(ParagraphStyle(
    name="ReportBody",
    fontName="Helvetica",
    fontSize=9.5,
    leading=14,
    textColor=DARK_GREY,
    spaceAfter=7
))

styles.add(ParagraphStyle(
    name="ReportBullet",
    fontName="Helvetica",
    fontSize=9.5,
    leading=14,
    leftIndent=17,
    firstLineIndent=-10,
    textColor=DARK_GREY,
    spaceAfter=5
))

styles.add(ParagraphStyle(
    name="CoverInfo",
    fontName="Helvetica",
    fontSize=9.5,
    leading=14,
    textColor=DARK_PURPLE
))


def inline_format(text):
    text = escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)
    return text


def draw_page(canvas, doc):
    canvas.saveState()
    page_width, page_height = A4

    # Purple top band and pink accent
    canvas.setFillColor(DARK_PURPLE)
    canvas.rect(0, page_height - 7 * mm, page_width, 7 * mm,
                fill=1, stroke=0)

    canvas.setFillColor(PINK)
    canvas.rect(0, page_height - 8 * mm, page_width, 1 * mm,
                fill=1, stroke=0)

    if doc.page > 1:
        canvas.setFont("Helvetica-Bold", 8)
        canvas.setFillColor(PURPLE)
        canvas.drawString(
            22 * mm, page_height - 15 * mm,
            "LALIBELA | HERITAGE SHORT PROJECT"
        )

        canvas.setStrokeColor(LAVENDER)
        canvas.line(
            22 * mm, page_height - 18 * mm,
            page_width - 22 * mm, page_height - 18 * mm
        )

    # Footer
    canvas.setStrokeColor(LAVENDER)
    canvas.line(
        22 * mm, 17 * mm,
        page_width - 22 * mm, 17 * mm
    )

    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MID_GREY)
    canvas.drawString(
        22 * mm, 11 * mm,
        "Lalibela: A Story Carved in Stone"
    )

    canvas.drawRightString(
        page_width - 22 * mm, 11 * mm,
        f"Page {doc.page}"
    )

    canvas.restoreState()


# Read report
with open(SOURCE, "r", encoding="utf-8") as file:
    lines = file.readlines()


# Find the beginning of the numbered report sections.
# This prevents the title and metadata from being repeated.
start_index = None

for i, raw_line in enumerate(lines):
    line = raw_line.strip()

    if re.match(r"^#{1,3}\s+\d+[\.)]\s+", line):
        start_index = i
        break

# Fallback if the report uses headings without section numbers.
if start_index is None:
    heading_positions = [
        i for i, raw_line in enumerate(lines)
        if raw_line.strip().startswith("#")
    ]

    if len(heading_positions) >= 2:
        start_index = heading_positions[1] + 1
    else:
        start_index = 0

report_lines = lines[start_index:]


# BUILD COVER PAGE
story = []

story.append(Spacer(1, 16 * mm))

story.append(Paragraph(
    "ETHIOPIAN CULTURAL HERITAGE",
    ParagraphStyle(
        "Eyebrow",
        fontName="Helvetica-Bold",
        fontSize=10,
        alignment=TA_CENTER,
        textColor=PINK,
        spaceAfter=10
    )
))

story.append(HRFlowable(
    width="35%",
    thickness=3,
    color=PINK,
    hAlign="CENTER",
    spaceBefore=2,
    spaceAfter=14
))

story.append(Paragraph(
    "Lalibela: A Story<br/>Carved in Stone",
    styles["CoverTitle"]
))

story.append(Paragraph(
    "AI-Generated Heritage Short<br/>Final Project Report",
    styles["CoverSubtitle"]
))

story.append(Spacer(1, 12 * mm))

cover_data = [
    [Paragraph("<b>Project</b>", styles["CoverInfo"]),
     Paragraph("AI-Content Generation – The Heritage Short",
               styles["CoverInfo"])],
    [Paragraph("<b>Location</b>", styles["CoverInfo"]),
     Paragraph("Ethiopia", styles["CoverInfo"])],
    [Paragraph("<b>Project date</b>", styles["CoverInfo"]),
     Paragraph("November 2026", styles["CoverInfo"])],
    [Paragraph("<b>Duration</b>", styles["CoverInfo"]),
     Paragraph("Approximately 89 seconds", styles["CoverInfo"])],
    [Paragraph("<b>Formats</b>", styles["CoverInfo"]),
     Paragraph("Horizontal and vertical video", styles["CoverInfo"])]
]

cover_table = Table(
    cover_data,
    colWidths=[42 * mm, 105 * mm]
)

cover_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), LAVENDER),
    ("BACKGROUND", (0, 0), (0, -1), PALE_PINK),
    ("BOX", (0, 0), (-1, -1), 0.8, PINK),
    ("INNERGRID", (0, 0), (-1, -1), 0.4, WHITE),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ("TOPPADDING", (0, 0), (-1, -1), 7),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
]))

story.append(cover_table)
story.append(Spacer(1, 12 * mm))

story.append(Paragraph(
    "A short journey into the history, architecture,<br/>"
    "faith, and shared heritage of Lalibela, Ethiopia.",
    ParagraphStyle(
        "CoverMessage",
        fontName="Helvetica-Oblique",
        fontSize=11,
        leading=17,
        alignment=TA_CENTER,
        textColor=PURPLE
    )
))

# Start report on page two
story.append(PageBreak())


# BUILD REPORT CONTENT
for raw_line in report_lines:
    line = raw_line.strip()

    if not line:
        story.append(Spacer(1, 2))
        continue

    if line == "---":
        story.append(HRFlowable(
            width="100%",
            thickness=1,
            color=PINK,
            spaceBefore=6,
            spaceAfter=8
        ))
        continue

    if line.startswith("### "):
        story.append(Paragraph(
            inline_format(line[4:]),
            styles["SubHeading"]
        ))
        continue

    if line.startswith("## "):
        heading = Paragraph(
            inline_format(line[3:]),
            styles["SectionHeading"]
        )
        divider = HRFlowable(
            width="100%",
            thickness=1.3,
            color=PINK,
            spaceBefore=1,
            spaceAfter=8
        )
        story.append(KeepTogether([heading, divider]))
        continue

    if line.startswith("# "):
        story.append(Paragraph(
            inline_format(line[2:]),
            styles["SectionHeading"]
        ))
        continue

    if line.startswith("- "):
        story.append(Paragraph(
            '<font color="#D66A9F"><b>•</b></font> '
            + inline_format(line[2:]),
            styles["ReportBullet"]
        ))
        continue

    story.append(Paragraph(
        inline_format(line),
        styles["ReportBody"]
    ))


# CREATE PDF
document = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    rightMargin=22 * mm,
    leftMargin=22 * mm,
    topMargin=24 * mm,
    bottomMargin=24 * mm,
    title="Lalibela: A Story Carved in Stone - Final Project Report",
    author="Lalibela Heritage Short Project",
    subject="AI-generated Ethiopian cultural heritage film"
)

document.build(
    story,
    onFirstPage=draw_page,
    onLaterPages=draw_page
)

print("PURPLE AND PINK PDF REPORT CREATED SUCCESSFULLY!")
print("Output:", OUTPUT)
print("File size:", os.path.getsize(OUTPUT), "bytes")

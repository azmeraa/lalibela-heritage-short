
import os
import re
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    HRFlowable, Table, TableStyle, KeepTogether
)

# ---------------------------------------------------------
# PROJECT PATHS
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(BASE_DIR, "FINAL_REPORT.md")
OUTPUT = os.path.join(BASE_DIR, "outputs", "Lalibela_Final_Report.pdf")

os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

if not os.path.exists(SOURCE):
    raise FileNotFoundError("FINAL_REPORT.md was not found.")

# ---------------------------------------------------------
# MODERN COLOUR PALETTE
# ---------------------------------------------------------

NAVY = colors.HexColor("#21152F")
PURPLE = colors.HexColor("#593477")
PINK = colors.HexColor("#D66A9F")
LAVENDER = colors.HexColor("#F2ECF7")
PALE_PINK = colors.HexColor("#FDF1F6")
LIGHT_BG = colors.HexColor("#FAF8FC")
DARK_TEXT = colors.HexColor("#302A36")
BODY_TEXT = colors.HexColor("#514A58")
MUTED = colors.HexColor("#817889")
WHITE = colors.white
BORDER = colors.HexColor("#E7DFEC")

# ---------------------------------------------------------
# FONT SETUP
# Use Segoe UI on Windows, with Helvetica fallback.
# ---------------------------------------------------------

FONT_REGULAR = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
FONT_ITALIC = "Helvetica-Oblique"

font_dir = r"C:\Windows\Fonts"

font_files = {
    "SegoeUI": os.path.join(font_dir, "segoeui.ttf"),
    "SegoeUI-Bold": os.path.join(font_dir, "segoeuib.ttf"),
    "SegoeUI-Italic": os.path.join(font_dir, "segoeuii.ttf"),
}

if all(os.path.exists(path) for path in font_files.values()):
    for font_name, font_path in font_files.items():
        pdfmetrics.registerFont(TTFont(font_name, font_path))

    pdfmetrics.registerFontFamily(
        "SegoeUI",
        normal="SegoeUI",
        bold="SegoeUI-Bold",
        italic="SegoeUI-Italic",
        boldItalic="SegoeUI-Bold"
    )

    FONT_REGULAR = "SegoeUI"
    FONT_BOLD = "SegoeUI-Bold"
    FONT_ITALIC = "SegoeUI-Italic"

# ---------------------------------------------------------
# DOCUMENT STYLES
# ---------------------------------------------------------

styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    name="CoverEyebrow",
    fontName=FONT_BOLD,
    fontSize=9,
    leading=13,
    textColor=PINK,
    alignment=TA_CENTER,
    spaceAfter=15,
    tracking=1.5
))

styles.add(ParagraphStyle(
    name="CoverTitle",
    fontName=FONT_BOLD,
    fontSize=31,
    leading=38,
    textColor=NAVY,
    alignment=TA_CENTER,
    spaceAfter=12
))

styles.add(ParagraphStyle(
    name="CoverSubtitle",
    fontName=FONT_REGULAR,
    fontSize=13,
    leading=20,
    textColor=PURPLE,
    alignment=TA_CENTER
))

styles.add(ParagraphStyle(
    name="CoverDescription",
    fontName=FONT_ITALIC,
    fontSize=10.5,
    leading=17,
    textColor=BODY_TEXT,
    alignment=TA_CENTER
))

styles.add(ParagraphStyle(
    name="CoverInfo",
    fontName=FONT_REGULAR,
    fontSize=9.5,
    leading=15,
    textColor=DARK_TEXT
))

styles.add(ParagraphStyle(
    name="SectionHeading",
    fontName=FONT_BOLD,
    fontSize=16,
    leading=21,
    textColor=PURPLE,
    spaceBefore=15,
    spaceAfter=8,
    keepWithNext=True
))

styles.add(ParagraphStyle(
    name="SubHeading",
    fontName=FONT_BOLD,
    fontSize=11.5,
    leading=16,
    textColor=PINK,
    spaceBefore=10,
    spaceAfter=5,
    keepWithNext=True
))

styles.add(ParagraphStyle(
    name="MinorHeading",
    fontName=FONT_BOLD,
    fontSize=10.5,
    leading=15,
    textColor=NAVY,
    spaceBefore=8,
    spaceAfter=4,
    keepWithNext=True
))

styles.add(ParagraphStyle(
    name="ReportBody",
    fontName=FONT_REGULAR,
    fontSize=10.2,
    leading=15.5,
    textColor=BODY_TEXT,
    alignment=TA_LEFT,
    spaceAfter=8,
    allowWidows=0,
    allowOrphans=0
))

styles.add(ParagraphStyle(
    name="ReportBullet",
    fontName=FONT_REGULAR,
    fontSize=10,
    leading=15,
    leftIndent=16,
    firstLineIndent=-10,
    textColor=BODY_TEXT,
    spaceAfter=5
))

styles.add(ParagraphStyle(
    name="ReportNumber",
    fontName=FONT_REGULAR,
    fontSize=10,
    leading=15,
    leftIndent=19,
    firstLineIndent=-16,
    textColor=BODY_TEXT,
    spaceAfter=5
))

styles.add(ParagraphStyle(
    name="Callout",
    fontName=FONT_ITALIC,
    fontSize=10,
    leading=15,
    textColor=PURPLE,
    leftIndent=5,
    rightIndent=5
))

# ---------------------------------------------------------
# MARKDOWN INLINE FORMATTING
# ---------------------------------------------------------

def inline_format(text):
    text = escape(text)

    # Bold
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)

    # Italic
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)

    # Inline code
    text = re.sub(
        r"`([^`]+)`",
        r'<font color="#593477">\1</font>',
        text
    )

    return text


# ---------------------------------------------------------
# PAGE HEADER AND FOOTER
# ---------------------------------------------------------

def draw_page(canvas, doc):
    canvas.saveState()

    page_width, page_height = A4

    # Top colour band
    canvas.setFillColor(NAVY)
    canvas.rect(
        0, page_height - 7 * mm,
        page_width, 7 * mm,
        fill=1, stroke=0
    )

    # Pink accent line
    canvas.setFillColor(PINK)
    canvas.rect(
        0, page_height - 8 * mm,
        page_width, 1 * mm,
        fill=1, stroke=0
    )

    if doc.page > 1:
        canvas.setFont(FONT_BOLD, 8)
        canvas.setFillColor(PURPLE)
        canvas.drawString(
            22 * mm,
            page_height - 15 * mm,
            "LALIBELA | HERITAGE SHORT PROJECT"
        )

        canvas.setFont(FONT_REGULAR, 8)
        canvas.setFillColor(MUTED)
        canvas.drawRightString(
            page_width - 22 * mm,
            page_height - 15 * mm,
            "FINAL PROJECT REPORT"
        )

        canvas.setStrokeColor(BORDER)
        canvas.setLineWidth(0.6)
        canvas.line(
            22 * mm, page_height - 18 * mm,
            page_width - 22 * mm, page_height - 18 * mm
        )

    # Footer line
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.6)
    canvas.line(
        22 * mm, 17 * mm,
        page_width - 22 * mm, 17 * mm
    )

    canvas.setFont(FONT_REGULAR, 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(
        22 * mm, 11 * mm,
        "Lalibela: A Story Carved in Stone"
    )

    canvas.drawRightString(
        page_width - 22 * mm, 11 * mm,
        f"Page {doc.page}"
    )

    canvas.restoreState()


# ---------------------------------------------------------
# READ REPORT CONTENT
# ---------------------------------------------------------

with open(SOURCE, "r", encoding="utf-8") as file:
    lines = file.readlines()

# Skip the Markdown title and subtitle on the cover.
start_index = None

for i, raw_line in enumerate(lines):
    line = raw_line.strip()

    if re.match(r"^#{1,3}\s+\d+[\.)]\s+", line):
        start_index = i
        break

if start_index is None:
    heading_positions = [
        i for i, raw_line in enumerate(lines)
        if raw_line.strip().startswith("#")
    ]

    start_index = (
        heading_positions[1] + 1
        if len(heading_positions) >= 2
        else 0
    )

report_lines = lines[start_index:]


# ---------------------------------------------------------
# BUILD COVER PAGE
# ---------------------------------------------------------

story = []

story.append(Spacer(1, 22 * mm))

story.append(Paragraph(
    "ETHIOPIAN CULTURAL HERITAGE",
    styles["CoverEyebrow"]
))

story.append(HRFlowable(
    width="28%",
    thickness=3,
    color=PINK,
    hAlign="CENTER",
    spaceBefore=2,
    spaceAfter=19
))

story.append(Paragraph(
    "Lalibela: A Story<br/>Carved in Stone",
    styles["CoverTitle"]
))

story.append(Paragraph(
    "AI-Generated Heritage Short",
    styles["CoverSubtitle"]
))

story.append(Paragraph(
    "FINAL PROJECT REPORT",
    ParagraphStyle(
        "CoverLabel",
        fontName=FONT_BOLD,
        fontSize=9,
        leading=14,
        alignment=TA_CENTER,
        textColor=PINK,
        spaceBefore=7
    )
))

story.append(Spacer(1, 17 * mm))

cover_data = [
    [
        Paragraph("<b>PROJECT</b>", styles["CoverInfo"]),
        Paragraph("AI-Content Generation – The Heritage Short",
                  styles["CoverInfo"])
    ],
    [
        Paragraph("<b>LOCATION</b>", styles["CoverInfo"]),
        Paragraph("Ethiopia", styles["CoverInfo"])
    ],
    [
        Paragraph("<b>PROJECT DATE</b>", styles["CoverInfo"]),
        Paragraph("November 2026", styles["CoverInfo"])
    ],
    [
        Paragraph("<b>FILM DURATION</b>", styles["CoverInfo"]),
        Paragraph("Approximately 89 seconds", styles["CoverInfo"])
    ],
    [
        Paragraph("<b>VIDEO FORMATS</b>", styles["CoverInfo"]),
        Paragraph("Horizontal 16:9 and vertical 9:16", styles["CoverInfo"])
    ]
]

cover_table = Table(
    cover_data,
    colWidths=[43 * mm, 105 * mm],
    hAlign="CENTER"
)

cover_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
    ("BACKGROUND", (0, 0), (0, -1), LAVENDER),
    ("BOX", (0, 0), (-1, -1), 0.8, BORDER),
    ("INNERGRID", (0, 0), (-1, -1), 0.5, WHITE),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 11),
    ("RIGHTPADDING", (0, 0), (-1, -1), 11),
    ("TOPPADDING", (0, 0), (-1, -1), 9),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
]))

story.append(cover_table)
story.append(Spacer(1, 20 * mm))

story.append(Paragraph(
    "A short journey into the history, architecture, "
    "faith, and shared heritage of Lalibela, Ethiopia.",
    styles["CoverDescription"]
))

story.append(Spacer(1, 12 * mm))

story.append(HRFlowable(
    width="55%",
    thickness=1,
    color=PINK,
    hAlign="CENTER"
))

story.append(PageBreak())


# ---------------------------------------------------------
# BUILD REPORT BODY
# ---------------------------------------------------------

for raw_line in report_lines:
    line = raw_line.strip()

    if not line:
        story.append(Spacer(1, 3))
        continue

    if line == "---":
        story.append(HRFlowable(
            width="100%",
            thickness=0.8,
            color=BORDER,
            spaceBefore=8,
            spaceAfter=10
        ))
        continue

    # Main sections
    if line.startswith("## "):
        heading = Paragraph(
            inline_format(line[3:]),
            styles["SectionHeading"]
        )

        divider = HRFlowable(
            width="100%",
            thickness=1.2,
            color=PINK,
            spaceBefore=1,
            spaceAfter=8
        )

        story.append(KeepTogether([heading, divider]))
        continue

    # Subsections
    if line.startswith("### "):
        story.append(Paragraph(
            inline_format(line[4:]),
            styles["SubHeading"]
        ))
        continue

    # Smaller headings
    if line.startswith("# "):
        story.append(Paragraph(
            inline_format(line[2:]),
            styles["MinorHeading"]
        ))
        continue

    # Bullet points
    if line.startswith("- "):
        story.append(Paragraph(
            '<font color="#D66A9F"><b>●</b></font> '
            + inline_format(line[2:]),
            styles["ReportBullet"]
        ))
        continue

    # Numbered lists
    number_match = re.match(r"^(\d+)\.\s+(.*)", line)

    if number_match:
        number = number_match.group(1)
        content = number_match.group(2)

        story.append(Paragraph(
            f'<font color="#593477"><b>{number}.</b></font> '
            + inline_format(content),
            styles["ReportNumber"]
        ))
        continue

    # Highlighted quotations or callouts
    if line.startswith("> "):
        callout = Table(
            [[Paragraph(
                inline_format(line[2:]),
                styles["Callout"]
            )]],
            colWidths=[155 * mm]
        )

        callout.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), LAVENDER),
            ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
            ("LINEBEFORE", (0, 0), (0, -1), 3, PINK),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ("TOPPADDING", (0, 0), (-1, -1), 9),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ]))

        story.append(callout)
        story.append(Spacer(1, 7))
        continue

    # Standard paragraphs
    story.append(Paragraph(
        inline_format(line),
        styles["ReportBody"]
    ))


# ---------------------------------------------------------
# GENERATE PDF
# ---------------------------------------------------------

document = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    rightMargin=22 * mm,
    leftMargin=22 * mm,
    topMargin=25 * mm,
    bottomMargin=24 * mm,
    title="Lalibela: A Story Carved in Stone - Final Project Report",
    author="Lalibela Heritage Short Project",
    subject="AI-generated Ethiopian cultural heritage film",
    pageCompression=1
)

document.build(
    story,
    onFirstPage=draw_page,
    onLaterPages=draw_page
)

print("MODERN PDF REPORT CREATED SUCCESSFULLY!")
print("Font:", FONT_REGULAR)
print("Output:", OUTPUT)
print("File size:", os.path.getsize(OUTPUT), "bytes")

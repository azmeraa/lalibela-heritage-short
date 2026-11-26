from pathlib import Path
import re

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

BASE = Path(__file__).resolve().parent
SOURCE = BASE / "FINAL_REPORT.md"
OUTPUT = BASE / "outputs" / "Lalibela_Final_Report.docx"

PURPLE = "51266F"
DARK_PURPLE = "35164D"
PINK = "D66A9F"
LAVENDER = "F1E8F7"
PALE_PINK = "FCEEF4"
DARK_GREY = "3F3744"

if not SOURCE.exists():
    raise FileNotFoundError("FINAL_REPORT.md was not found.")

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

doc = Document()
section = doc.sections[0]
section.top_margin = Inches(0.85)
section.bottom_margin = Inches(0.75)
section.left_margin = Inches(0.9)
section.right_margin = Inches(0.9)

# Default document typography
normal = doc.styles["Normal"]
normal.font.name = "Segoe UI"
normal.font.size = Pt(12)
normal.font.color.rgb = RGBColor.from_string(DARK_GREY)
normal.paragraph_format.space_after = Pt(9)
normal.paragraph_format.line_spacing = 1.25

for style_name, size, color in [
    ("Heading 1", 19, DARK_PURPLE),
    ("Heading 2", 16, PURPLE),
    ("Heading 3", 13, PINK),
]:
    style = doc.styles[style_name]
    style.font.name = "Segoe UI"
    style.font.size = Pt(size)
    style.font.bold = True
    style.font.color.rgb = RGBColor.from_string(color)
    style.paragraph_format.space_before = Pt(15)
    style.paragraph_format.space_after = Pt(7)
    style.paragraph_format.keep_with_next = True

def shade_cell(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)

def set_cell_text(cell, text, bold=False, color=DARK_PURPLE):
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(3)
    run = p.add_run(text)
    run.bold = bold
    run.font.name = "Segoe UI"
    run.font.size = Pt(10.5)
    run.font.color.rgb = RGBColor.from_string(color)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER

def add_formatted_text(paragraph, text):
    # Support bold, italic, and inline code.
    pattern = r"(\*\*.*?\*\*|\*.*?\*|`.*?`)"
    parts = re.split(pattern, text)

    for part in parts:
        if not part:
            continue

        if part.startswith("**") and part.endswith("**"):
            run = paragraph.add_run(part[2:-2])
            run.bold = True
        elif part.startswith("*") and part.endswith("*"):
            run = paragraph.add_run(part[1:-1])
            run.italic = True
        elif part.startswith("`") and part.endswith("`"):
            run = paragraph.add_run(part[1:-1])
            run.font.name = "Consolas"
            run.font.size = Pt(10)
        else:
            run = paragraph.add_run(part)

        if not (part.startswith("`") and part.endswith("`")):
            run.font.name = "Segoe UI"
            run.font.size = Pt(12)
            run.font.color.rgb = RGBColor.from_string(DARK_GREY)

# Header
header = section.header
header_p = header.paragraphs[0]
header_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
header_run = header_p.add_run("LALIBELA  |  HERITAGE SHORT PROJECT")
header_run.font.name = "Segoe UI"
header_run.font.size = Pt(8)
header_run.font.bold = True
header_run.font.color.rgb = RGBColor.from_string(PURPLE)

# Footer with automatic page number
footer = section.footer
footer_p = footer.paragraphs[0]
footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
footer_run = footer_p.add_run("Lalibela: A Story Carved in Stone  |  Page ")
footer_run.font.name = "Segoe UI"
footer_run.font.size = Pt(9)
footer_run.font.color.rgb = RGBColor.from_string(PURPLE)

field = OxmlElement("w:fldSimple")
field.set(qn("w:instr"), "PAGE")
footer_p._p.append(field)

# Cover page
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(65)
r = p.add_run("ETHIOPIAN CULTURAL HERITAGE")
r.bold = True
r.font.name = "Segoe UI"
r.font.size = Pt(12)
r.font.color.rgb = RGBColor.from_string(PINK)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(28)
p.paragraph_format.space_after = Pt(12)
r = p.add_run("Lalibela: A Story\nCarved in Stone")
r.bold = True
r.font.name = "Segoe UI"
r.font.size = Pt(30)
r.font.color.rgb = RGBColor.from_string(DARK_PURPLE)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("AI-Generated Heritage Short\nFinal Project Report")
r.font.name = "Segoe UI"
r.font.size = Pt(16)
r.font.color.rgb = RGBColor.from_string(PURPLE)

doc.add_paragraph()

cover_rows = [
    ("Project", "AI-Content Generation – The Heritage Short"),
    ("Location", "Ethiopia"),
    ("Project date", "November 2026"),
    ("Duration", "Approximately 89 seconds"),
    ("Formats", "Horizontal and vertical video"),
]

table = doc.add_table(rows=0, cols=2)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
table.autofit = False
table.columns[0].width = Inches(1.45)
table.columns[1].width = Inches(4.9)

for label, value in cover_rows:
    cells = table.add_row().cells
    cells[0].width = Inches(1.45)
    cells[1].width = Inches(4.9)
    shade_cell(cells[0], PALE_PINK)
    shade_cell(cells[1], LAVENDER)
    set_cell_text(cells[0], label, bold=True, color=DARK_PURPLE)
    set_cell_text(cells[1], value, color=DARK_GREY)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(35)
r = p.add_run(
    "A short journey into the history, architecture,\n"
    "faith, and shared heritage of Lalibela, Ethiopia."
)
r.italic = True
r.font.name = "Segoe UI"
r.font.size = Pt(13)
r.font.color.rgb = RGBColor.from_string(PURPLE)

doc.add_page_break()

# Read report and start at the numbered report sections.
lines = SOURCE.read_text(encoding="utf-8").splitlines()
start = 0

for i, line in enumerate(lines):
    if re.match(r"^#{1,3}\s+\d+[\.)]\s+", line.strip()):
        start = i
        break

lines = lines[start:]

# Convert Markdown content into editable Word paragraphs.
for raw in lines:
    line = raw.strip()

    if not line:
        continue

    if line == "---":
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(5)
        p.paragraph_format.space_after = Pt(8)
        pPr = p._p.get_or_add_pPr()
        borders = OxmlElement("w:pBdr")
        bottom = OxmlElement("w:bottom")
        bottom.set(qn("w:val"), "single")
        bottom.set(qn("w:sz"), "8")
        bottom.set(qn("w:color"), PINK)
        borders.append(bottom)
        pPr.append(borders)
        continue

    if line.startswith("### "):
        p = doc.add_paragraph(style="Heading 3")
        add_formatted_text(p, line[4:])
        continue

    if line.startswith("## "):
        p = doc.add_paragraph(style="Heading 2")
        add_formatted_text(p, line[3:])
        continue

    if line.startswith("# "):
        p = doc.add_paragraph(style="Heading 1")
        add_formatted_text(p, line[2:])
        continue

    if line.startswith("- "):
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.2
        add_formatted_text(p, line[2:])
        continue

    numbered = re.match(r"^\d+[\.)]\s+(.*)", line)
    if numbered:
        p = doc.add_paragraph(style="List Number")
        p.paragraph_format.space_after = Pt(6)
        add_formatted_text(p, numbered.group(1))
        continue

    p = doc.add_paragraph()
    p.paragraph_format.widow_control = True
    add_formatted_text(p, line)

doc.core_properties.title = "Lalibela: A Story Carved in Stone - Final Project Report"
doc.core_properties.subject = "AI-generated Ethiopian cultural heritage film"
doc.core_properties.author = "Lalibela Heritage Short Project"

doc.save(OUTPUT)

print("EDITABLE WORD REPORT CREATED SUCCESSFULLY!")
print("Output:", OUTPUT)
print("File size:", OUTPUT.stat().st_size, "bytes")

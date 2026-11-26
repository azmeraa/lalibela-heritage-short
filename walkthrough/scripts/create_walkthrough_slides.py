from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "walkthrough" / "generated" / "slides"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1920, 1080
FONT = "/c/Windows/Fonts/arial.ttf"
BOLD = "/c/Windows/Fonts/arialbd.ttf"

slides = [
    {
        "title": "Lalibela: A Story Carved in Stone",
        "subtitle": "An AI-assisted heritage film production pipeline",
        "bullets": [
            "A bilingual heritage story about Lalibela, Ethiopia",
            "Amharic and English narration",
            "A reproducible workflow built with AI and Python"
        ],
        "footer": "PROJECT WALKTHROUGH"
    },
    {
        "title": "01 — From storyboard to film",
        "subtitle": "The storyboard is the central source of production information.",
        "bullets": [
            "Eight scenes with timing, visual prompts and narration",
            "JSON Schema and Python validation before production",
            "Creative purpose documented for every shot",
            "Separate creative source and production scripts"
        ],
        "footer": "STORYBOARD • VALIDATION • PRODUCTION"
    },
    {
        "title": "02 — Building the visual story",
        "subtitle": "FLUX.2 Klein 4B generated the documentary-style keyframes.",
        "bullets": [
            "Eight planned scenes introduce Lalibela and its heritage",
            "Consistent visual direction across the sequence",
            "FFmpeg adds slow pan-and-zoom movement to still images"
        ],
        "image": ROOT / "walkthrough" / "evidence" / "keyframe_contact_sheet.jpg",
        "footer": "AI-GENERATED KEYFRAMES"
    },
    {
        "title": "03 — Narration, music and sound",
        "subtitle": "Separate audio elements are combined during post-production.",
        "bullets": [
            "Gemini text-to-speech generates Amharic and English narration",
            "ACE-Step 1.5 generates original background music",
            "FFmpeg combines narration and music with audio ducking",
            "English subtitles support accessibility"
        ],
        "footer": "AUDIO PRODUCTION • MIXING • SUBTITLES"
    },
    {
        "title": "04 — A practical engineering decision",
        "subtitle": "Choosing a reliable workflow within the available time.",
        "bullets": [
            "Wan 2.2 image-to-video was considered",
            "FFmpeg pan-and-zoom was selected for this implementation",
            "Three earlier S01 API requests returned HTTP 400 errors",
            "The failures and later successful generation remain in the run log"
        ],
        "footer": "EXPERIMENTATION • TRADE-OFFS • TROUBLESHOOTING"
    },
    {
        "title": "05 — Selective regeneration demonstrated",
        "subtitle": "One prompt change. One selected scene. One new successful model call.",
        "bullets": [
            "Added a traditional Ethiopian highland footpath to the S01 prompt",
            "REGENERATE_ONLY = {\"S01\"}",
            "Storyboard validation passed before generation",
            "S01 regenerated successfully in 14.1 seconds",
            "S02–S08 were not selected and remained untouched"
        ],
        "image": ROOT / "assets" / "images" / "S01.jpg",
        "footer": "LATEST RUN • SEED 406106886 • LOGGED"
    },
    {
        "title": "06 — Audience feedback and learning",
        "subtitle": "Feedback is part of the design process, not just a final check.",
        "bullets": [
            "A Python and Tkinter application collects structured responses",
            "Near-final feedback informed review of visuals, narration and music",
            "The radio-cut test still needs two more real participants",
            "Test records are kept separate from genuine participant feedback"
        ],
        "footer": "AUDIENCE TESTING • ITERATION • HONEST EVIDENCE"
    },
    {
        "title": "07 — Final outputs and reflection",
        "subtitle": "One heritage story, delivered in two formats.",
        "bullets": [
            "Horizontal: 1920 × 1080 (16:9)",
            "Vertical: 1080 × 1920 (9:16)",
            "Both videos: H.264 video, AAC audio, approximately 89 seconds",
            "Both outputs passed FFprobe checks and full FFmpeg decoding",
            "The project combines storytelling, automation, validation and learning"
        ],
        "footer": "LALIBELA: A STORY CARVED IN STONE"
    }
]

def font(path, size):
    return ImageFont.truetype(path, size)

def draw_wrapped(draw, text, xy, max_chars, fnt, fill, spacing=16):
    x, y = xy
    for line in textwrap.wrap(text, width=max_chars):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y

for i, item in enumerate(slides, 1):
    im = Image.new("RGB", (W, H), "#101d2b")
    d = ImageDraw.Draw(im)

    d.rectangle((0, 0, 18, H), fill="#c89b55")
    d.text((100, 75), "LALIBELA HERITAGE SHORT", font=font(BOLD, 25), fill="#c89b55")
    d.text((100, 155), item["title"], font=font(BOLD,  fifty :=  fifty if False else  fifty if False else  fifty if False else 50), fill="#ffffff")

    d.text((105, 245), item["subtitle"], font=font(FONT, 29), fill="#d7e0e8")

    text_x, text_y = 115, 355
    max_width = 850 if item.get("image") else 1550
    max_chars = 48 if item.get("image") else 78

    for bullet in item["bullets"]:
        d.ellipse((text_x, text_y + 12, text_x + 13, text_y + 25), fill="#c89b55")
        text_y = draw_wrapped(
            d, bullet, (text_x + 35, text_y),
            max_chars, font(FONT, 27), "#ffffff", 13
        ) + 25

    if item.get("image"):
        path = item["image"]
        if path.exists():
            pic = Image.open(path).convert("RGB")
            pic.thumbnail((820, 650))
            px = W - pic.width - 95
            py = 330 + max(0, (650 - pic.height) // 2)
            im.paste(pic, (px, py))
            d.rectangle((px - 3, py - 3, px + pic.width + 3, py + pic.height + 3), outline="#c89b55", width=3)
        else:
            d.text((1100, 500), "Project image not found", font=font(FONT, 28), fill="#ffcc99")

    d.line((100, 970, 1820, 970), fill="#536475", width=2)
    d.text((105, 990), item["footer"], font=font(BOLD, 19), fill="#c89b55")
    d.text((1740, 990), f"{i:02d} / 08", font=font(FONT, 19), fill="#d7e0e8")

    target = OUT / f"slide_{i:02d}.png"
    im.save(target)
    print("[CREATED]", target)

print(f"\n[SUCCESS] Created {len(slides)} walkthrough slides in {OUT}")

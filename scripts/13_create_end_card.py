
#!/usr/bin/env python3
"""Create the Lalibela heritage short end card."""

import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PROJECT = Path(__file__).resolve().parent.parent
VALIDATOR = PROJECT / "scripts" / "01_validate_storyboard.py"
OUTPUT = PROJECT / "assets" / "images" / "end_card.jpg"

WIDTH, HEIGHT = 1920, 1080


def validate_storyboard():
    """Stop if the storyboard does not pass validation."""
    print("\nValidating storyboard...")

    result = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=PROJECT,
        check=False
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Storyboard validation failed. End-card creation stopped."
        )

    print("[PASS] Storyboard validation completed.")


def load_font(size, bold=False):
    """Load a suitable font with cross-platform fallbacks."""
    if sys.platform == "win32":
        candidates = [
            Path("C:/Windows/Fonts/arialbd.ttf" if bold
                 else "C:/Windows/Fonts/arial.ttf")
        ]
    else:
        candidates = [
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
                 if bold else
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
            Path("/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"
                 if bold else
                 "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf")
        ]

    for path in candidates:
        if path.is_file():
            try:
                return ImageFont.truetype(str(path), size)
            except OSError:
                continue

    return ImageFont.load_default()


def main():
    validate_storyboard()

    print("\nCreating the end card...")

    image = Image.new("RGB", (WIDTH, HEIGHT), (15, 25, 38))
    draw = ImageDraw.Draw(image)

    # Deep navy background with subtle gradient.
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(15 + t * 12)
        g = int(25 + t * 17)
        b = int(38 + t * 22)
        draw.line((0, y, WIDTH, y), fill=(r, g, b))

    title_font = load_font(100, True)
    subtitle_font = load_font(43)
    message_font = load_font(39, True)
    amharic_font = load_font(43)
    small_font = load_font(30)

    def centered_text(text, y, font, fill):
        box = draw.textbbox((0, 0), text, font=font)
        x = (WIDTH - (box[2] - box[0])) // 2
        draw.text((x, y), text, font=font, fill=fill)

    GOLD = (255, 198, 92)
    WHITE = (248, 249, 246)
    TURQUOISE = (87, 220, 205)
    PALE_GOLD = (255, 222, 160)
    SOFT_WHITE = (215, 226, 232)

    # Decorative gold lines.
    draw.line((590, 265, 1330, 265), fill=GOLD, width=4)
    draw.ellipse((945, 251, 975, 281), fill=GOLD)

    centered_text("LALIBELA", 325, title_font, GOLD)
    centered_text("A Story Carved in Stone", 450, subtitle_font, WHITE)

    centered_text(
        "Different people. Different cultures.",
        585, message_font, TURQUOISE
    )
    centered_text(
        "One shared heritage.",
        640, message_font, TURQUOISE
    )

    centered_text(
        "ላሊበላ፡ በድንጋይ የተቀረፀ ታሪክ",
        735, amharic_font, PALE_GOLD
    )

    draw.line((650, 830, 1270, 830), fill=GOLD, width=2)

    centered_text(
        "An AI-assisted heritage film",
        865, small_font, WHITE
    )
    centered_text(
        "Created with artificial intelligence tools",
        915, small_font, SOFT_WHITE
    )

    draw.ellipse((950, 990, 970, 1010), fill=TURQUOISE)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT, quality=95)

    if not OUTPUT.is_file() or OUTPUT.stat().st_size == 0:
        raise RuntimeError("End-card image was not saved successfully.")

    with Image.open(OUTPUT) as check:
        if check.size != (WIDTH, HEIGHT):
            raise RuntimeError("End-card dimensions are incorrect.")

    print("\n[PASS] End card created and verified.")
    print("Output:", OUTPUT)
    print("Image size:", WIDTH, "x", HEIGHT)


if __name__ == "__main__":
    main()

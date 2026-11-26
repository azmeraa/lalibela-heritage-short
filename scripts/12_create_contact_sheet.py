
#!/usr/bin/env python3
"""Create a contact sheet from the eight Lalibela keyframes."""

import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

PROJECT_DIR = Path(__file__).resolve().parent.parent
VALIDATOR = PROJECT_DIR / "scripts" / "01_validate_storyboard.py"
IMAGE_DIR = PROJECT_DIR / "assets" / "images"
OUTPUT_FILE = IMAGE_DIR / "contact_sheet.jpg"

THUMB_WIDTH = 480
THUMB_HEIGHT = 270
LABEL_HEIGHT = 40
COLUMNS = 2
EXPECTED_IMAGES = 8


def validate_storyboard():
    print("\nValidating storyboard...")

    result = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=PROJECT_DIR,
        check=False
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Storyboard validation failed. Contact sheet creation stopped."
        )

    print("[PASS] Storyboard validation completed.")


def main():
    validate_storyboard()

    if not IMAGE_DIR.is_dir():
        raise FileNotFoundError(
            f"Image directory not found: {IMAGE_DIR}"
        )

    files = sorted(IMAGE_DIR.glob("S*.jpg"))

    if len(files) != EXPECTED_IMAGES:
        raise RuntimeError(
            f"Expected {EXPECTED_IMAGES} JPEG images, found {len(files)}"
        )

    rows = (len(files) + COLUMNS - 1) // COLUMNS

    sheet = Image.new(
        "RGB",
        (
            COLUMNS * THUMB_WIDTH,
            rows * (THUMB_HEIGHT + LABEL_HEIGHT)
        ),
        "white"
    )

    draw = ImageDraw.Draw(sheet)

    for index, path in enumerate(files):
        print(f"[CHECK] {path.name}")

        try:
            with Image.open(path) as original:
                original.verify()

            with Image.open(path) as original:
                image = original.convert("RGB")
                image.thumbnail((THUMB_WIDTH, THUMB_HEIGHT))

        except Exception as error:
            raise RuntimeError(
                f"Unable to read image {path.name}: {error}"
            ) from error

        x = (index % COLUMNS) * THUMB_WIDTH
        y = (index // COLUMNS) * (THUMB_HEIGHT + LABEL_HEIGHT)

        sheet.paste(image, (x, y))

        draw.text(
            (x + 10, y + THUMB_HEIGHT + 10),
            path.stem,
            fill="black"
        )

    sheet.save(OUTPUT_FILE, format="JPEG", quality=90)

    if not OUTPUT_FILE.is_file() or OUTPUT_FILE.stat().st_size == 0:
        raise RuntimeError("Contact sheet output was not created correctly.")

    print("\n[SUCCESS] Contact sheet created and verified.")
    print(f"Output: {OUTPUT_FILE}")
    print(f"Images included: {len(files)}")
    print(
        f"Dimensions: {sheet.width} x {sheet.height}"
    )

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:
        print(f"\n[ERROR] {error}")
        sys.exit(1)

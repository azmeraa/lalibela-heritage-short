
#!/usr/bin/env python3
"""Validate storyboard and inspect generated image file formats."""

import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
VALIDATOR = PROJECT_DIR / "scripts" / "01_validate_storyboard.py"
IMAGE_DIR = PROJECT_DIR / "assets" / "images"

SIGNATURES = {
    "JPEG": lambda data: data.startswith(bytes.fromhex("FFD8FF")),
    "PNG": lambda data: data.startswith(bytes.fromhex("89504E470D0A1A0A")),
    "WebP": lambda data: (
        len(data) >= 12
        and data[0:4] == b"RIFF"
        and data[8:12] == b"WEBP"
    ),
}


def validate_storyboard():
    print("\nValidating storyboard...")

    result = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=PROJECT_DIR,
        check=False
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Storyboard validation failed. Image inspection stopped."
        )

    print("[PASS] Storyboard validation completed.")


def detect_format(data):
    for image_format, check in SIGNATURES.items():
        if check(data):
            return image_format

    return "UNKNOWN"


def main():
    validate_storyboard()

    if not IMAGE_DIR.is_dir():
        raise FileNotFoundError(
            f"Image directory not found: {IMAGE_DIR}"
        )

    # Inspect generated scene images with common image extensions.
    extensions = ("*.jpg", "*.jpeg", "*.png", "*.webp")
    image_files = sorted(
        path
        for pattern in extensions
        for path in IMAGE_DIR.glob(pattern)
        if path.stem.startswith("S")
    )

    if not image_files:
        print("[FAILURE] No scene images found.")
        return 1

    print("\nIMAGE FILE VALIDATION")
    print("=" * 60)

    all_valid = True

    for path in image_files:
        try:
            data = path.read_bytes()
            detected = detect_format(data)

            expected = {
                ".jpg": "JPEG",
                ".jpeg": "JPEG",
                ".png": "PNG",
                ".webp": "WebP",
            }.get(path.suffix.lower())

            valid = (
                len(data) > 0
                and detected != "UNKNOWN"
                and detected == expected
            )

            status = "PASS" if valid else "FAIL"
            print(f"[{status}] {path.name}")
            print(f"       Detected format: {detected}")
            print(f"       File size: {len(data):,} bytes")

            if not valid:
                all_valid = False

        except OSError as error:
            print(f"[FAIL] {path.name}: {error}")
            all_valid = False

    print("=" * 60)
    print(f"Images inspected: {len(image_files)}")

    if all_valid:
        print("[SUCCESS] All inspected images passed signature checks.")
        return 0

    print("[FAILURE] One or more images need attention.")
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:
        print(f"\n[ERROR] {error}")
        sys.exit(1)

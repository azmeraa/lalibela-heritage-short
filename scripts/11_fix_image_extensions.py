
#!/usr/bin/env python3
"""Safely correct image extensions when PNG-named files contain JPEG data."""

import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
VALIDATOR = PROJECT_DIR / "scripts" / "01_validate_storyboard.py"
IMAGE_DIR = PROJECT_DIR / "assets" / "images"


def validate_storyboard():
    print("\nValidating storyboard...")

    result = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=PROJECT_DIR,
        check=False
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Storyboard validation failed. Image correction stopped."
        )

    print("[PASS] Storyboard validation completed.")


def detect_format(data):
    if data.startswith(bytes.fromhex("FFD8FF")):
        return "JPEG"

    if data.startswith(bytes.fromhex("89504E470D0A1A0A")):
        return "PNG"

    if (
        len(data) >= 12
        and data[0:4] == b"RIFF"
        and data[8:12] == b"WEBP"
    ):
        return "WebP"

    return "UNKNOWN"


def main():
    validate_storyboard()

    if not IMAGE_DIR.is_dir():
        raise FileNotFoundError(
            f"Image directory not found: {IMAGE_DIR}"
        )

    renamed = 0
    skipped = 0
    failed = 0

    for path in sorted(IMAGE_DIR.glob("S*.png")):
        try:
            data = path.read_bytes()
            actual_format = detect_format(data)

            if actual_format == "PNG":
                print(f"[SKIP] {path.name}: already a PNG.")
                skipped += 1
                continue

            if actual_format != "JPEG":
                print(
                    f"[SKIP] {path.name}: "
                    f"unsupported or unknown format."
                )
                skipped += 1
                continue

            new_path = path.with_suffix(".jpg")

            if new_path.exists():
                print(
                    f"[ERROR] Cannot rename {path.name}: "
                    f"{new_path.name} already exists."
                )
                failed += 1
                continue

            path.rename(new_path)
            print(
                f"[RENAMED] {path.name} -> {new_path.name}"
            )
            renamed += 1

        except OSError as error:
            print(f"[ERROR] {path.name}: {error}")
            failed += 1

    print("\nIMAGE EXTENSION CORRECTION SUMMARY")
    print(f"Renamed: {renamed}")
    print(f"Skipped: {skipped}")
    print(f"Failed: {failed}")

    if failed:
        return 1

    print("[SUCCESS] Image extension check completed.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:
        print(f"\n[ERROR] {error}")
        sys.exit(1)

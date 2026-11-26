
#!/usr/bin/env python3
"""Create the 9:16 vertical film from the horizontal master."""

import argparse
import subprocess
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent

FFMPEG = Path(
    r"C:\ffmpeg\ffmpeg-9.1-essentials_build\bin\ffmpeg.exe"
)

VALIDATOR = PROJECT / "scripts" / "01_validate_storyboard.py"
INPUT = PROJECT / "outputs" / "lalibela_horizontal.mp4"
OUTPUT = PROJECT / "outputs" / "lalibela_vertical.mp4"


def validate_storyboard():
    """Validate the storyboard before processing."""
    print("\nValidating storyboard...")

    result = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=PROJECT,
        check=False
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Storyboard validation failed. Vertical assembly stopped."
        )

    print("[PASS] Storyboard validation completed.")


def main():
    parser = argparse.ArgumentParser(
        description="Create the 9:16 vertical Lalibela film."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Regenerate the vertical video even if it already exists."
    )
    args = parser.parse_args()

    validate_storyboard()

    if not FFMPEG.is_file():
        raise FileNotFoundError(f"FFmpeg not found: {FFMPEG}")

    if not INPUT.is_file():
        raise FileNotFoundError(f"Horizontal film not found: {INPUT}")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    if OUTPUT.exists() and not args.force:
        print("\nVertical film already exists.")
        print("Skipping to preserve the completed output.")
        print("Use --force only when you intentionally want to rebuild it.")
        print("Output:", OUTPUT)
        return

    print("\nCreating vertical film...")
    print("Resolution: 1080x1920")
    print("Aspect ratio: 9:16")
    print("Frame rate: 25 fps")

    filter_complex = (
        "[0:v]split=2[background][foreground];"
        "[background]"
        "scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,"
        "boxblur=20:10[background_blurred];"
        "[foreground]"
        "scale=1080:1920:force_original_aspect_ratio=decrease"
        "[foreground_scaled];"
        "[background_blurred][foreground_scaled]"
        "overlay=(W-w)/2:(H-h)/2,"
        "format=yuv420p[video]"
    )

    command = [
        str(FFMPEG),
        "-y",
        "-i", str(INPUT),
        "-filter_complex", filter_complex,
        "-map", "[video]",
        "-map", "0:a:0",
        "-r", "25",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-movflags", "+faststart",
        str(OUTPUT)
    ]

    subprocess.run(command, check=True, cwd=PROJECT)

    if not OUTPUT.is_file() or OUTPUT.stat().st_size == 0:
        raise RuntimeError("Vertical film was not created successfully.")

    print("\nVERTICAL FILM CREATED SUCCESSFULLY!")
    print("Output:", OUTPUT)


if __name__ == "__main__":
    main()


#!/usr/bin/env python3
"""Create the 9:16 vertical film from the horizontal master."""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent

FFMPEG = os.getenv("FFMPEG_PATH") or shutil.which("ffmpeg")

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


def is_valid_video(path):
    """Check whether an MP4 file can be decoded by FFmpeg."""
    if not path.is_file() or path.stat().st_size == 0:
        return False

    result = subprocess.run(
        [
            FFMPEG,
            "-v", "error",
            "-i", str(path),
            "-f", "null",
            "-"
        ],
        cwd=PROJECT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False
    )

    return result.returncode == 0


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

    if not FFMPEG:
        raise FileNotFoundError(
            "FFmpeg not found. Install FFmpeg and add it to PATH, "
            "or set the FFMPEG_PATH environment variable."
        )

    if not INPUT.is_file():
        raise FileNotFoundError(
            f"Horizontal film not found: {INPUT}"
        )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    if is_valid_video(OUTPUT) and not args.force:
        print("\n[CACHE] Existing vertical film is valid.")
        print("Skipping to preserve the completed output.")
        print("Use --force only when you intentionally want to rebuild it.")
        print("Output:", OUTPUT)
        return

    print("\nCreating vertical film...")
    print("Resolution: 1080x1920")
    print("Aspect ratio: 9:16")
    print("Frame rate: 25 fps")

    temporary_output = OUTPUT.with_name(
        "lalibela_vertical.tmp.mp4"
    )
    temporary_output.unlink(missing_ok=True)

    filter_complex = (
        "[0:v]split=2[background][foreground];"
        "[background]"
        "scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,"
        "boxblur=8:4,eq=brightness=-0.10:saturation=0.75[background_blurred];"
        "[foreground]"
        "scale=1080:1920:force_original_aspect_ratio=decrease"
        "[foreground_scaled];"
        "[background_blurred][foreground_scaled]"
        "overlay=(W-w)/2:(H-h)/2,"
        "format=yuv420p[video]"
    )

    command = [
        FFMPEG,
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
        str(temporary_output)
    ]

    try:
        subprocess.run(
            command,
            check=True,
            cwd=PROJECT
        )

        if not is_valid_video(temporary_output):
            raise RuntimeError(
                "Generated vertical video failed FFmpeg validation."
            )

        temporary_output.replace(OUTPUT)

    except Exception:
        temporary_output.unlink(missing_ok=True)
        raise

    print("\nVERTICAL FILM CREATED SUCCESSFULLY!")
    print("Output:", OUTPUT)
    print("Resolution: 1080x1920")
    print("Aspect ratio: 9:16")


if __name__ == "__main__":
    main()

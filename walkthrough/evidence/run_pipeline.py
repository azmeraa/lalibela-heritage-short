#!/usr/bin/env python3
"""Rebuild the Lalibela heritage films from committed production assets."""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

PROJECT = Path(__file__).resolve().parent
load_dotenv(PROJECT / ".env")

FFMPEG = os.getenv("FFMPEG_PATH") or shutil.which("ffmpeg")

IMAGES_DIR = PROJECT / "assets" / "images"
AUDIO_DIR = PROJECT / "assets" / "audio"
MUSIC_FILE = AUDIO_DIR / "music" / "lalibela_music.wav"
FINAL_MIX = AUDIO_DIR / "final_mix.wav"

MOVING_SHOTS_DIR = PROJECT / "assets" / "video" / "moving_shots"
END_CARD_VIDEO = PROJECT / "assets" / "video" / "end_card.mp4"

HORIZONTAL = PROJECT / "outputs" / "lalibela_horizontal.mp4"
VERTICAL = PROJECT / "outputs" / "lalibela_vertical.mp4"


def run_step(script_name):
    """Run one pipeline stage and stop if it fails."""
    script = PROJECT / "scripts" / script_name

    print("\n" + "=" * 65)
    print(f"RUNNING: {script_name}")
    print("=" * 65)

    subprocess.run(
        [sys.executable, str(script)],
        cwd=PROJECT,
        check=True
    )


def validate_audio(path):
    """Check that an audio file can be decoded by FFmpeg."""
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

    if result.returncode != 0:
        raise RuntimeError(f"Audio file is invalid: {path}")


def check_source_assets():
    """Check all pre-generated assets required for video assembly."""
    if not FFMPEG:
        raise FileNotFoundError(
            "FFmpeg was not found. Install FFmpeg and add it to PATH, "
            "or set FFMPEG_PATH in your environment."
        )

    if not Path(FFMPEG).is_file():
        raise FileNotFoundError(
            f"FFmpeg executable not found: {FFMPEG}"
        )

    required_files = [
        PROJECT / "storyboard.json",
        PROJECT / "storyboard.schema.json",
        AUDIO_DIR / "narration_script.json",
        MUSIC_FILE,
        FINAL_MIX,
    ]

    for path in required_files:
        if not path.is_file() or path.stat().st_size == 0:
            raise FileNotFoundError(
                f"Required project asset is missing or empty: {path}"
            )

    for number in range(1, 9):
        image = IMAGES_DIR / f"S{number:02d}.jpg"

        if not image.is_file() or image.stat().st_size == 0:
            raise FileNotFoundError(
                f"Missing keyframe image: {image}"
            )

    print("[PASS] Required storyboard and keyframe assets found.")

    validate_audio(MUSIC_FILE)
    validate_audio(FINAL_MIX)

    print("[PASS] Original music and final audio mix are readable.")


def clear_derived_outputs():
    """Remove generated video outputs when --force is requested."""
    print("\n[FORCE] Clearing derived video outputs...")

    if MOVING_SHOTS_DIR.exists():
        for path in MOVING_SHOTS_DIR.glob("*.mp4"):
            path.unlink()

    for path in [
        END_CARD_VIDEO,
        HORIZONTAL,
        VERTICAL,
    ]:
        path.unlink(missing_ok=True)

    print("[PASS] Derived video outputs cleared.")


def main():
    parser = argparse.ArgumentParser(
        description="Rebuild the Lalibela heritage films."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Rebuild derived videos instead of reusing valid cached files."
    )
    args = parser.parse_args()

    print("\nLALIBELA HERITAGE FILM PIPELINE")
    print("Rebuilding videos from existing AI-generated assets.")

    check_source_assets()

    if args.force:
        clear_derived_outputs()

    # Stage 1: Validate the storyboard and schema.
    run_step("01_validate_storyboard.py")

    # Stage 2: Prepare English subtitles from the narration script.
    run_step("04_prepare_narration.py")

    # Stage 3: Create the end card only if it is missing.
    end_card_image = IMAGES_DIR / "end_card.jpg"

    if not end_card_image.is_file():
        run_step("13_create_end_card.py")
    else:
        print("\n[CACHE] Reusing existing end-card image.")

    # Stage 4: Create or reuse the eight moving shots.
    run_step("14_create_moving_shots.py")

    # Stage 5: Assemble the horizontal film.
    run_step("15_assemble_horizontal.py")

    # Stage 6: Create or reuse the vertical film.
    run_step("15_assemble_vertical.py")

    print("\n" + "=" * 65)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 65)
    print("Horizontal film:", HORIZONTAL)
    print("Vertical film:  ", VERTICAL)
    print("\nExisting AI-generated images, narration and music were reused.")
    print("No AI generation API calls were required for this rebuild.")


if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, RuntimeError, subprocess.CalledProcessError) as error:
        print(f"\n[PIPELINE FAILED] {error}")
        sys.exit(1)

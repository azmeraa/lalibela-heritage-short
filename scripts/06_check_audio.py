
#!/usr/bin/env python3
"""Inspect narration WAV files for validity and scene duration."""

import json
import subprocess
import sys
import wave
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent

VALIDATOR = PROJECT_DIR / "scripts" / "01_validate_storyboard.py"
AUDIO_DIR = PROJECT_DIR / "assets" / "audio"
SCRIPT_FILE = AUDIO_DIR / "narration_script.json"


def validate_storyboard():
    """Validate the storyboard before checking audio."""
    print("\nValidating storyboard...")

    result = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=PROJECT_DIR,
        check=False
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Storyboard validation failed. Audio inspection stopped."
        )

    print("[PASS] Storyboard validation completed.")


def main():
    validate_storyboard()

    if not SCRIPT_FILE.is_file():
        raise FileNotFoundError(
            f"Narration script not found: {SCRIPT_FILE}"
        )

    with SCRIPT_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    print("\nAUDIO QUALITY AND DURATION CHECK")
    print("=" * 65)

    total_audio_duration = 0
    all_valid = True
    checked_files = 0

    for scene in data["scenes"]:
        scene_id = scene["scene_id"]
        language = scene["language"]
        filename = f"{scene_id}_{language}.wav"
        audio_file = AUDIO_DIR / filename

        planned_duration = scene["end"] - scene["start"]

        if not audio_file.is_file():
            print(f"[MISSING] {filename}")
            all_valid = False
            continue

        try:
            with wave.open(str(audio_file), "rb") as wav:
                frames = wav.getnframes()
                sample_rate = wav.getframerate()
                channels = wav.getnchannels()
                sample_width = wav.getsampwidth()

                if frames == 0 or sample_rate == 0:
                    raise ValueError("Audio file is empty or invalid.")

                duration = frames / sample_rate

            checked_files += 1
            total_audio_duration += duration

            status = (
                "FITS"
                if duration <= planned_duration
                else "LONGER"
            )

            if status == "LONGER":
                all_valid = False

            print(
                f"{scene_id} | {language.upper()} | "
                f"{duration:.2f}s | planned "
                f"{planned_duration}s | {status}"
            )
            print(
                f"      Sample rate: {sample_rate} Hz | "
                f"Channels: {channels} | "
                f"Sample width: {sample_width * 8} bit"
            )

        except (wave.Error, EOFError, ValueError, OSError) as error:
            print(f"[INVALID] {filename}: {error}")
            all_valid = False

    print("=" * 65)
    print(
        f"Valid audio files inspected: "
        f"{checked_files}/{len(data['scenes'])}"
    )
    print(
        f"Total generated narration: "
        f"{total_audio_duration:.2f} seconds"
    )
    print(
        f"Planned film duration: "
        f"{data['total_duration_seconds']} seconds"
    )

    if all_valid and checked_files == len(data["scenes"]):
        print("\n[SUCCESS] All narration files passed inspection.")
        return 0

    print("\n[FAILURE] Some audio files need attention.")
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:
        print(f"\n[ERROR] {error}")
        sys.exit(1)

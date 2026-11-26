
#!/usr/bin/env python3
"""Validate narration data and prepare English subtitles."""

import json
import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent

VALIDATOR = PROJECT_DIR / "scripts" / "01_validate_storyboard.py"
SCRIPT_FILE = PROJECT_DIR / "assets" / "audio" / "narration_script.json"
SUBTITLE_FILE = PROJECT_DIR / "assets" / "subtitles" / "en.srt"


def validate_storyboard():
    """Stop if the main storyboard fails validation."""
    print("\nValidating storyboard...")

    result = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=PROJECT_DIR,
        check=False
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Storyboard validation failed. Narration preparation stopped."
        )

    print("[PASS] Storyboard validation completed.")


def format_srt_time(seconds):
    milliseconds = round(seconds * 1000)
    hours = milliseconds // 3_600_000
    milliseconds %= 3_600_000
    minutes = milliseconds // 60_000
    milliseconds %= 60_000
    secs = milliseconds // 1000
    milliseconds %= 1000

    return (
        f"{hours:02}:{minutes:02}:"
        f"{secs:02},{milliseconds:03}"
    )


def main():
    validate_storyboard()

    if not SCRIPT_FILE.is_file():
        raise FileNotFoundError(
            f"Narration file not found: {SCRIPT_FILE}"
        )

    with SCRIPT_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    scenes = data.get("scenes", [])

    if len(scenes) != 8:
        raise ValueError(
            f"Expected 8 scenes, found {len(scenes)}"
        )

    previous_end = 0
    subtitle_entries = []

    for index, scene in enumerate(scenes, start=1):
        scene_id = scene.get("scene_id", f"Scene {index}")

        start = scene["start"]
        end = scene["end"]

        if start != previous_end:
            raise ValueError(
                f"Timeline gap or overlap before {scene_id}"
            )

        if end <= start:
            raise ValueError(
                f"Invalid timing in {scene_id}"
            )

        if not scene.get("narration"):
            raise ValueError(
                f"Missing narration in {scene_id}"
            )

        if not scene.get("english_subtitle"):
            raise ValueError(
                f"Missing English subtitle in {scene_id}"
            )

        subtitle_entries.append(
            f"{index}\n"
            f"{format_srt_time(start)} --> "
            f"{format_srt_time(end)}\n"
            f"{scene['english_subtitle']}\n"
        )

        previous_end = end

    expected_duration = data["total_duration_seconds"]

    if previous_end != expected_duration:
        raise ValueError(
            f"Expected {expected_duration} seconds, "
            f"but timeline ends at {previous_end}"
        )

    SUBTITLE_FILE.parent.mkdir(parents=True, exist_ok=True)

    subtitle_content = "\n".join(subtitle_entries)
    SUBTITLE_FILE.write_text(
        subtitle_content,
        encoding="utf-8"
    )

    if not SUBTITLE_FILE.is_file():
        raise RuntimeError("Subtitle file was not created.")

    if SUBTITLE_FILE.stat().st_size == 0:
        raise RuntimeError("Subtitle file is empty.")

    print("\n[PASS] Narration JSON loaded.")
    print("[PASS] All 8 scenes checked.")
    print("[PASS] Timeline is continuous.")
    print("[PASS] Narration and subtitles are present.")
    print(f"[PASS] Total duration: {previous_end} seconds.")
    print(f"[PASS] Subtitle file verified: {SUBTITLE_FILE}")


if __name__ == "__main__":
    main()

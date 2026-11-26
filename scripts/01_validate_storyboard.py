#!/usr/bin/env python3
"""
Validate the Lalibela Heritage Short storyboard.

Usage:
    python scripts/01_validate_storyboard.py
    python scripts/01_validate_storyboard.py --storyboard storyboard.json
    python scripts/01_validate_storyboard.py --storyboard storyboard.json --schema storyboard.schema.json

The script performs:
1. JSON parsing.
2. JSON Schema validation (when jsonschema is installed).
3. Project-specific semantic checks:
   - unique shot IDs
   - valid character references
   - positive shot durations
   - start/end/duration consistency
   - continuous, non-overlapping timeline
   - total duration consistency
   - required prompts and narration
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        raise ValueError(f"File not found: {path}")
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON in {path}: line {exc.lineno}, "
            f"column {exc.colno}: {exc.msg}"
        )


def validate_schema(data: dict, schema: dict, schema_path: Path) -> list[str]:
    errors: list[str] = []
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        return [
            "JSON Schema validation was skipped because the 'jsonschema' "
            "package is not installed. Run: pip install -r requirements.txt"
        ]

    try:
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        for error in sorted(validator.iter_errors(data), key=lambda e: list(map(str, e.path))):
            location = ".".join(str(part) for part in error.absolute_path) or "<root>"
            errors.append(f"Schema error at {location}: {error.message}")
    except Exception as exc:
        errors.append(f"Could not validate against schema {schema_path}: {exc}")
    return errors


def validate_semantics(data: dict) -> list[str]:
    errors: list[str] = []

    if not isinstance(data, dict):
        return ["Storyboard root must be a JSON object."]

    project = data.get("project")
    shots = data.get("shots")
    characters = data.get("characters")

    if not isinstance(project, dict):
        errors.append("Missing or invalid 'project' object.")
        project = {}
    if not isinstance(shots, list) or not shots:
        errors.append("'shots' must be a non-empty array.")
        shots = []
    if not isinstance(characters, list):
        errors.append("'characters' must be an array.")
        characters = []

    known_character_ids = {
        item.get("character_id")
        for item in characters
        if isinstance(item, dict) and isinstance(item.get("character_id"), str)
    }

    shot_ids: set[str] = set()
    previous_end = None
    computed_total = 0

    for index, shot in enumerate(shots, start=1):
        label = f"shots[{index - 1}]"

        if not isinstance(shot, dict):
            errors.append(f"{label} must be an object.")
            continue

        shot_id = shot.get("shot_id")
        if not isinstance(shot_id, str) or not shot_id:
            errors.append(f"{label} has a missing or invalid shot_id.")
        elif shot_id in shot_ids:
            errors.append(f"Duplicate shot_id: {shot_id}")
        else:
            shot_ids.add(shot_id)

        start = shot.get("start_seconds")
        end = shot.get("end_seconds")
        duration = shot.get("duration_seconds")

        if not all(isinstance(x, int) and not isinstance(x, bool) for x in (start, end, duration)):
            errors.append(f"{label} start_seconds, end_seconds and duration_seconds must be integers.")
        else:
            if start < 0:
                errors.append(f"{label} start_seconds cannot be negative.")
            if duration <= 0:
                errors.append(f"{label} duration_seconds must be positive.")
            if end <= start:
                errors.append(f"{label} end_seconds must be greater than start_seconds.")
            if end - start != duration:
                errors.append(
                    f"{label} timing mismatch: end - start is {end - start}, "
                    f"but duration_seconds is {duration}."
                )
            if previous_end is not None and start != previous_end:
                relation = "gap" if start > previous_end else "overlap"
                errors.append(
                    f"{label} timeline {relation}: starts at {start}s, "
                    f"previous shot ended at {previous_end}s."
                )
            previous_end = end
            computed_total += duration

        refs = shot.get("characters", [])
        if not isinstance(refs, list):
            errors.append(f"{label}.characters must be an array.")
        else:
            for character_id in refs:
                if character_id not in known_character_ids:
                    errors.append(
                        f"{label} references unknown character_id: {character_id}"
                    )

        for field in ("title", "image_prompt", "motion_prompt", "action", "camera"):
            if not isinstance(shot.get(field), str) or not shot[field].strip():
                errors.append(f"{label}.{field} is required and must be non-empty.")

        narration = shot.get("narration")
        if not isinstance(narration, dict) or narration.get("language") not in ("am", "en") \
                or not isinstance(narration.get("text"), str) or not narration["text"].strip():
            errors.append(f"{label}.narration must contain a supported language and non-empty text.")

        subtitle = shot.get("subtitle")
        if not isinstance(subtitle, dict) or subtitle.get("language") not in ("am", "en") \
                or not isinstance(subtitle.get("text"), str) or not subtitle["text"].strip():
            errors.append(f"{label}.subtitle must contain a supported language and non-empty text.")

    expected_total = project.get("target_duration_seconds")
    if isinstance(expected_total, int) and computed_total != expected_total:
        errors.append(
            f"Project duration mismatch: shots total {computed_total}s, "
            f"project target is {expected_total}s."
        )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the heritage short storyboard.")
    parser.add_argument("--storyboard", default="storyboard.json", help="Path to storyboard JSON.")
    parser.add_argument("--schema", default="storyboard.schema.json", help="Path to JSON Schema.")
    args = parser.parse_args()

    storyboard_path = Path(args.storyboard)
    schema_path = Path(args.schema)

    try:
        storyboard = load_json(storyboard_path)
        schema = load_json(schema_path)
    except ValueError as exc:
        print(f"[FAIL] {exc}")
        return 1

    errors = []
    errors.extend(validate_schema(storyboard, schema, schema_path))
    errors.extend(validate_semantics(storyboard))

    print("=" * 64)
    print("LALIBELA HERITAGE SHORT — STORYBOARD VALIDATION")
    print("=" * 64)

    if errors:
        print(f"[FAIL] Found {len(errors)} issue(s):")
        for number, error in enumerate(errors, start=1):
            print(f"  {number}. {error}")
        print("\nFix the issues before starting media generation.")
        return 1

    shot_count = len(storyboard["shots"])
    total_duration = sum(shot["duration_seconds"] for shot in storyboard["shots"])
    print("[PASS] JSON files loaded.")
    print("[PASS] JSON Schema validation completed.")
    print("[PASS] Shot IDs and character references checked.")
    print("[PASS] Shot timing and timeline continuity checked.")
    print("[PASS] Prompts, narration and subtitles checked.")
    print(f"[PASS] {shot_count} shots; total duration: {total_duration} seconds.")
    print("\nStoryboard is ready for the next production step.")
    return 0


if __name__ == "__main__":
    sys.exit(main())


import os
import sys
import json
import base64
import time
import subprocess
from pathlib import Path
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv


# --------------------------------------------------
# PROJECT CONFIGURATION
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

STORYBOARD = PROJECT_DIR / "storyboard.json"
IMAGE_DIR = PROJECT_DIR / "assets" / "images"
LOG_FILE = PROJECT_DIR / "logs" / "runs.jsonl"

IMAGE_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

MAX_RETRIES = 3

# Regenerate only S01 for the selective-regeneration demonstration.
REGENERATE_ONLY = {"S01"}


# --------------------------------------------------
# STORYBOARD VALIDATION
# --------------------------------------------------

def validate_storyboard():
    """Stop keyframe generation if storyboard validation fails."""

    validator = PROJECT_DIR / "scripts" / "01_validate_storyboard.py"

    result = subprocess.run(
        [sys.executable, str(validator)],
        cwd=PROJECT_DIR,
        check=False
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Storyboard validation failed. Image generation stopped."
        )

    print("[PASS] Storyboard validation completed.")


# --------------------------------------------------
# LOAD ENVIRONMENT AND API CONFIGURATION
# --------------------------------------------------

load_dotenv(PROJECT_DIR / ".env")

ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")

if not ACCOUNT_ID or not API_TOKEN:
    raise RuntimeError("Cloudflare credentials missing from .env")

MODEL = "@cf/black-forest-labs/flux-2-klein-4b"

BASE_URL = (
    f"https://api.cloudflare.com/client/v4/accounts/"
    f"{ACCOUNT_ID}/ai/run/{MODEL}"
)


# --------------------------------------------------
# LOAD STORYBOARD
# --------------------------------------------------

storyboard = json.loads(
    STORYBOARD.read_text(encoding="utf-8")
)


# --------------------------------------------------
# CACHE CHECK
# --------------------------------------------------

def matching_cached_image(shot_id, prompt, output):
    """Reuse a successful image when model, prompt and output match."""

    if not LOG_FILE.exists():
        return False

    try:
        records = [
            json.loads(line)
            for line in LOG_FILE.read_text(
                encoding="utf-8"
            ).splitlines()
            if line.strip()
        ]
    except (OSError, json.JSONDecodeError):
        return False

    relative_output = str(output.relative_to(PROJECT_DIR))

    for record in reversed(records):
        if (
            record.get("stage") == "keyframe"
            and record.get("scene_id") == shot_id
            and record.get("model") == MODEL
            and record.get("prompt") == prompt
            and record.get("status") == "success"
            and record.get("output") == relative_output
            and output.exists()
        ):
            print(f"[CACHE] Reusing existing image: {shot_id}")
            return True

    return False


# --------------------------------------------------
# IMAGE GENERATION
# --------------------------------------------------

def generate_image(shot_id, prompt, output):
    """Generate an image with retries and execution logging."""

    seed = int(time.time() * 1000) % 2147483647

    parameters = {
        "width": 1920,
        "height": 1080,
        "seed": seed
    }

    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }

    payload = {
        "prompt": prompt,
        "width": str(parameters["width"]),
        "height": str(parameters["height"]),
        "seed": str(seed)
    }

    for attempt in range(1, MAX_RETRIES + 1):
        start_time = time.time()

        try:
            response = requests.post(
                BASE_URL,
                headers=headers,
                files={
                    key: (None, value)
                    for key, value in payload.items()
                },
                timeout=180
            )

            if not response.ok:
                raise RuntimeError(
                    f"Cloudflare HTTP {response.status_code}: "
                    f"{response.text}"
                )

            result = response.json()

            if not result.get("success", True):
                raise RuntimeError(
                    f"Cloudflare API error: {result}"
                )

            image_data = result.get("result", {}).get("image")

            if not image_data:
                raise RuntimeError(
                    f"No image returned by API: {result}"
                )

            image_bytes = base64.b64decode(image_data)

            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(image_bytes)

            latency = round(time.time() - start_time, 2)

            log_record = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "stage": "keyframe",
                "scene_id": shot_id,
                "model": MODEL,
                "prompt": prompt,
                "parameters": parameters,
                "seed": seed,
                "latency_seconds": latency,
                "cost_usd": None,
                "attempt": attempt,
                "status": "success",
                "output": str(output.relative_to(PROJECT_DIR))
            }

            with LOG_FILE.open("a", encoding="utf-8") as log_file:
                log_file.write(json.dumps(log_record) + "\n")

            print(
                f"[PASS] Generated {shot_id} "
                f"in {latency} seconds."
            )

            return True

        except Exception as error:
            latency = round(time.time() - start_time, 2)

            log_record = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "stage": "keyframe",
                "scene_id": shot_id,
                "model": MODEL,
                "prompt": prompt,
                "parameters": parameters,
                "seed": seed,
                "latency_seconds": latency,
                "cost_usd": None,
                "attempt": attempt,
                "status": "failed",
                "error": str(error)
            }

            with LOG_FILE.open("a", encoding="utf-8") as log_file:
                log_file.write(json.dumps(log_record) + "\n")

            print(
                f"[WARNING] Attempt {attempt}/{MAX_RETRIES} "
                f"failed for {shot_id}: {error}"
            )

            if attempt < MAX_RETRIES:
                time.sleep(2 ** attempt)

    print(f"[ERROR] Could not generate image for {shot_id}.")
    return False


# --------------------------------------------------
# MAIN PIPELINE
# --------------------------------------------------

def main():
    print("=" * 64)
    print("LALIBELA HERITAGE SHORT — KEYFRAME GENERATION")
    print("=" * 64)

    validate_storyboard()

    successful = 0
    failed = 0

    for shot in storyboard["shots"]:
        shot_id = shot["shot_id"]

        if shot_id not in REGENERATE_ONLY:
            continue

        prompt = shot.get("image_prompt", "").strip()

        if not prompt:
            print(f"[ERROR] Missing image_prompt for {shot_id}.")
            failed += 1
            continue

        output = IMAGE_DIR / f"{shot_id}.jpg"

        if matching_cached_image(shot_id, prompt, output):
            successful += 1
            continue

        print(f"\n[GENERATING] {shot_id}")

        if generate_image(shot_id, prompt, output):
            successful += 1
        else:
            failed += 1

    print("\n========================================")
    print("KEYFRAME GENERATION SUMMARY")
    print("========================================")
    print(f"Successful or cached: {successful}")
    print(f"Failed: {failed}")

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()

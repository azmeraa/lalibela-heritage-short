
#!/usr/bin/env python3
"""Generate a test keyframe using Cloudflare FLUX.2 Klein."""

import os
import sys
import json
import time
import base64
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from io import BytesIO

import requests
from dotenv import load_dotenv
from PIL import Image

PROJECT_DIR = Path(__file__).resolve().parent.parent
VALIDATOR = PROJECT_DIR / "scripts" / "01_validate_storyboard.py"
STORYBOARD_FILE = PROJECT_DIR / "storyboard.json"
IMAGE_DIR = PROJECT_DIR / "assets" / "images"
OUTPUT_FILE = IMAGE_DIR / "test_S01.png"
LOG_FILE = PROJECT_DIR / "logs" / "test_runs.jsonl"
ENV_FILE = PROJECT_DIR / ".env"

MODEL = "@cf/black-forest-labs/flux-2-klein-4b"
SEED = 4242
PARAMETERS = {
    "width": "1024",
    "height": "576",
    "seed": str(SEED),
}

MAX_ATTEMPTS = 3


def validate_storyboard():
    print("\nValidating storyboard...")

    result = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=PROJECT_DIR,
        check=False
    )

    if result.returncode != 0:
        raise RuntimeError("Storyboard validation failed.")

    print("[PASS] Storyboard validation completed.")


def write_log(record):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")


def main():
    validate_storyboard()

    if not STORYBOARD_FILE.is_file():
        raise FileNotFoundError(STORYBOARD_FILE)

    load_dotenv(ENV_FILE)

    account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
    api_token = os.getenv("CLOUDFLARE_API_TOKEN")

    if not account_id or not api_token:
        raise RuntimeError("Cloudflare credentials are missing from .env")

    storyboard = json.loads(
        STORYBOARD_FILE.read_text(encoding="utf-8")
    )

    shot = next(
        (item for item in storyboard["shots"]
         if item["shot_id"] == "S01"),
        None
    )

    if shot is None:
        raise RuntimeError("Shot S01 was not found in the storyboard.")

    prompt = shot["image_prompt"] + (
        " Wide landscape composition, 16:9 framing. "
        "Photographic realism, natural geography, "
        "documentary cinematography, historically grounded."
    )

    url = (
        f"https://api.cloudflare.com/client/v4/accounts/"
        f"{account_id}/ai/run/{MODEL}"
    )

    headers = {"Authorization": f"Bearer {api_token}"}

    if OUTPUT_FILE.exists():
        raise FileExistsError(
            f"Test output already exists: {OUTPUT_FILE}. "
            "Rename or move it before running this test."
        )

    print("\nGenerating a test image for S01...")

    for attempt in range(1, MAX_ATTEMPTS + 1):
        start_time = time.perf_counter()
        status = "failed"
        latency = None
        error_message = None

        try:
            response = requests.post(
                url,
                headers=headers,
                files={
                    key: (None, value)
                    for key, value in {
                        "prompt": prompt,
                        **PARAMETERS,
                    }.items()
                },
                timeout=240,
            )

            response.raise_for_status()
            content_type = response.headers.get("content-type", "")

            if "image/" in content_type:
                image_bytes = response.content
            else:
                result = response.json()

                if not result.get("success", True):
                    raise RuntimeError(
                        json.dumps(result)[:1500]
                    )

                image_data = result.get("result", {}).get("image")

                if not image_data:
                    raise RuntimeError("No image found in API response.")

                image_bytes = base64.b64decode(image_data)

            with Image.open(BytesIO(image_bytes)) as image:
                image.load()
                image.convert("RGB").save(OUTPUT_FILE, format="PNG")

            if not OUTPUT_FILE.is_file() or OUTPUT_FILE.stat().st_size == 0:
                raise RuntimeError("Image output verification failed.")

            status = "success"
            latency = round(time.perf_counter() - start_time, 2)

            print("[SUCCESS] Test image created.")
            print("Output:", OUTPUT_FILE)
            print("Size:", OUTPUT_FILE.stat().st_size, "bytes")

            return 0

        except Exception as error:
            error_message = str(error)
            latency = round(time.perf_counter() - start_time, 2)

            print(
                f"[ATTEMPT {attempt}/{MAX_ATTEMPTS} FAILED] "
                f"{error_message}"
            )

        finally:
            write_log({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "model": MODEL,
                "shot_id": "S01",
                "parameters": PARAMETERS,
                "seed": SEED,
                "latency_seconds": latency,
                "cost_usd": None,
                "attempt": attempt,
                "status": status,
                "output": str(OUTPUT_FILE),
                "error": error_message,
            })

        if attempt < MAX_ATTEMPTS:
            time.sleep(2 ** attempt)

    raise RuntimeError("Test image generation failed after all retries.")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:
        print(f"\n[ERROR] {error}")
        sys.exit(1)

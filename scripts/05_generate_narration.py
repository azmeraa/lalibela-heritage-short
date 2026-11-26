
import base64
import json
import os
import subprocess
import sys
import time
import wave
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from google import genai


PROJECT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_DIR / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")

MODEL = "gemini-3.8-flash-tts"
VOICE = "Kore"
MAX_RETRIES = 3

SCRIPT_FILE = PROJECT_DIR / "assets" / "audio" / "narration_script.json"
AUDIO_DIR = PROJECT_DIR / "assets" / "audio"
LOG_FILE = PROJECT_DIR / "logs" / "runs.jsonl"

STYLE = (
    "Warm, clear, natural documentary narration. "
    "Calm and expressive, with measured pacing suitable "
    "for an international audience. "
    "Pronounce place names carefully."
)


def validate_storyboard():
    """Stop generation if storyboard validation fails."""
    validator = PROJECT_DIR / "scripts" / "01_validate_storyboard.py"

    result = subprocess.run(
        [sys.executable, str(validator)],
        cwd=PROJECT_DIR,
        check=False
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Storyboard validation failed. Narration generation stopped."
        )

    print("[PASS] Storyboard validation completed.")


def is_valid_wav(file_path):
    """Check that an existing audio file is a readable WAV."""
    if not file_path.exists() or file_path.stat().st_size == 0:
        return False

    try:
        with wave.open(str(file_path), "rb") as audio:
            return (
                audio.getnframes() > 0
                and audio.getframerate() > 0
                and audio.getnchannels() > 0
            )
    except (wave.Error, EOFError, OSError):
        return False


def write_log(scene, status, attempt, elapsed,
              output=None, error=None):

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "stage": "narration_generation",
        "model": MODEL,
        "parameters": {
            "voice": VOICE,
            "language": scene["language"],
            "style": STYLE,
            "response_format": "audio"
        },
        "seed": None,
        "cost_usd": None,
        "scene_id": scene["scene_id"],
        "language": scene["language"],
        "attempt": attempt,
        "latency_seconds": elapsed,
        "status": status
    }

    if output is not None:
        record["output"] = str(
            output.relative_to(PROJECT_DIR)
        )

    if error is not None:
        record["error"] = error

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")


def generate_scene_audio(client, scene):

    scene_id = scene["scene_id"]
    language = scene["language"]

    output_file = AUDIO_DIR / f"{scene_id}_{language}.wav"

    input_content = [{
        "type": "text",
        "text": scene["narration"],
        "annotations": [{
            "type": "speech_metadata",
            "style": STYLE
        }]
    }]

    for attempt in range(1, MAX_RETRIES + 1):

        start_time = time.monotonic()

        try:
            interaction = client.interactions.create(
                model=MODEL,
                input=[{
                    "type": "user_input",
                    "content": input_content
                }],
                response_format={"type": "audio"},
                generation_config={
                    "speech_config": [{
                        "voice": VOICE
                    }]
                }
            )

            audio_data = interaction.output_audio.data

            if not audio_data:
                raise ValueError("API returned no audio data.")

            if isinstance(audio_data, str):
                audio_bytes = base64.b64decode(audio_data)
            else:
                audio_bytes = audio_data

            if not audio_bytes:
                raise ValueError("Decoded audio data is empty.")

            # Validate the generated audio before replacing the output.
            temp_file = output_file.with_name(
                output_file.stem + ".tmp.wav"
            )
            temp_file.write_bytes(audio_bytes)

            if not is_valid_wav(temp_file):
                temp_file.unlink(missing_ok=True)
                raise ValueError(
                    "Generated audio is not a valid, readable WAV file."
                )

            temp_file.replace(output_file)

            elapsed = round(time.monotonic() - start_time, 2)

            write_log(
                scene,
                "success",
                attempt,
                elapsed,
                output=output_file
            )

            return output_file, elapsed

        except Exception as error:

            elapsed = round(time.monotonic() - start_time, 2)

            write_log(
                scene,
                "failed",
                attempt,
                elapsed,
                error=str(error)
            )

            if attempt == MAX_RETRIES:
                raise

            wait_seconds = 2 ** attempt

            print(
                f"[RETRY] {scene_id}: attempt "
                f"{attempt} failed. Waiting {wait_seconds}s."
            )

            time.sleep(wait_seconds)


def main():

    validate_storyboard()

    if not SCRIPT_FILE.exists():
        raise FileNotFoundError(
            "Narration script JSON was not found."
        )

    with SCRIPT_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    scenes = data.get("scenes")

    if not isinstance(scenes, list) or not scenes:
        raise ValueError(
            "Narration script contains no valid scenes."
        )

    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    # Identify valid cached files and files that need generation.
    pending_scenes = []

    for scene in scenes:
        scene_id = scene["scene_id"]
        language = scene["language"]
        output_file = AUDIO_DIR / f"{scene_id}_{language}.wav"

        if is_valid_wav(output_file):
            print(f"[CACHE] Reusing valid audio: {output_file.name}")
        else:
            if output_file.exists():
                print(f"[CACHE MISS] Invalid audio: {output_file.name}")
            else:
                print(f"[MISSING] Audio needs generation: {output_file.name}")

            pending_scenes.append(scene)

    if not pending_scenes:
        print("\nAll narration clips are valid and cached.")
        print("No Gemini API calls were necessary.")
        return

    if not API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY not found. Check your .env file."
        )

    client = genai.Client(
        api_key=API_KEY,
        http_options={"api_version": "v1beta"}
    )

    print("\nStarting scene-by-scene narration generation.")
    print(f"Model: {MODEL}")
    print(f"Voice: {VOICE}")
    print(f"Maximum attempts: {MAX_RETRIES}")
    print(f"Clips to generate: {len(pending_scenes)}")
    print("-" * 55)

    successful = 0
    failed = 0

    for scene in pending_scenes:

        scene_id = scene["scene_id"]
        language = scene["language"]

        print(f"\nGenerating {scene_id} ({language})...")

        try:
            output_file, elapsed = generate_scene_audio(
                client, scene
            )

            successful += 1

            print(f"[SUCCESS] Saved: {output_file.name}")
            print(f"Generation time: {elapsed} seconds")

        except Exception as error:

            failed += 1

            print(f"[FAILED] {scene_id}: {error}")

    print("\n" + "=" * 55)
    print("NARRATION GENERATION SUMMARY")
    print(f"Generated successfully: {successful}")
    print(f"Failed: {failed}")
    print(f"Reused from cache: {len(scenes) - len(pending_scenes)}")
    print(f"Total scenes: {len(scenes)}")
    print(f"Run log: {LOG_FILE}")

    if failed:
        print("\nSome scenes failed. Check the run log.")
    else:
        print("\nAll narration clips are ready.")


if __name__ == "__main__":
    main()

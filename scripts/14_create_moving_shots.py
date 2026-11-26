
import os
import shutil
import subprocess
import sys
from pathlib import Path


PROJECT = Path(__file__).resolve().parent.parent

IMAGE_DIR = PROJECT / "assets" / "images"
OUTPUT_DIR = PROJECT / "assets" / "video" / "moving_shots"

VALIDATOR = PROJECT / "scripts" / "01_validate_storyboard.py"

# Use an explicitly configured FFmpeg path if provided,
# otherwise find FFmpeg through the system PATH.
FFMPEG = os.getenv("FFMPEG_PATH") or shutil.which("ffmpeg")

FPS = 25

SHOTS = {
    "S01": 10,
    "S02": 10,
    "S03": 10,
    "S04": 10,
    "S05": 10,
    "S06": 10,
    "S07": 12,
    "S08": 13,
}


def validate_storyboard():
    """Validate the storyboard before generating moving shots."""

    print("\nVALIDATING STORYBOARD...")

    result = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=PROJECT,
        check=False
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Storyboard validation failed. Moving-shot generation stopped."
        )

    print("[PASS] Storyboard validation completed.")


def is_valid_video(file_path):
    """Check whether an existing MP4 can be decoded."""

    if not file_path.exists() or file_path.stat().st_size == 0:
        return False

    try:
        result = subprocess.run(
            [
                FFMPEG,
                "-v", "error",
                "-i", str(file_path),
                "-f", "null",
                "-"
            ],
            cwd=PROJECT,
            capture_output=True,
            text=True,
            check=False
        )

        return result.returncode == 0

    except OSError:
        return False


def main():

    validate_storyboard()

    if not FFMPEG:
        raise FileNotFoundError(
            "FFmpeg was not found. Install FFmpeg and add it to PATH, "
            "or set the FFMPEG_PATH environment variable."
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    successful = 0
    skipped = 0
    failed = 0

    for shot_id, duration in SHOTS.items():

        image = IMAGE_DIR / f"{shot_id}.jpg"
        output = OUTPUT_DIR / f"{shot_id}.mp4"
        temporary_output = OUTPUT_DIR / f"{shot_id}.tmp.mp4"

        if is_valid_video(output):
            print(f"\n[CACHE] Reusing valid clip: {shot_id}")
            skipped += 1
            continue

        if output.exists():
            print(f"\n[CACHE MISS] Invalid clip: {shot_id}")
            output.unlink()

        if not image.exists():
            print(f"\n[ERROR] Missing image: {image}")
            failed += 1
            continue

        frames = duration * FPS

        print(f"\n[GENERATING] {shot_id}")
        print(f"Duration: {duration} seconds")
        print(f"Frames: {frames}")

        filter_video = (
            "scale=1920:1080:force_original_aspect_ratio=increase,"
            "crop=1920:1080,"
            "zoompan="
            "z='min(1+on*0.00032,1.08)':"
            "x='iw/2-(iw/zoom/2)':"
            "y='ih/2-(ih/zoom/2)':"
            f"d={frames}:s=1920x1080:fps={FPS},"
            "format=yuv420p"
        )

        command = [
            FFMPEG,
            "-y",
            "-i", str(image),
            "-vf", filter_video,
            "-frames:v", str(frames),
            "-an",
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "20",
            "-pix_fmt", "yuv420p",
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
                    f"Generated video failed validation: {shot_id}"
                )

            temporary_output.replace(output)

            print(f"[PASS] Created: {output}")
            successful += 1

        except (subprocess.CalledProcessError, RuntimeError, OSError) as error:
            temporary_output.unlink(missing_ok=True)
            print(f"[FAILED] {shot_id}: {error}")
            failed += 1

    print("\n========================================")
    print("MOVING SHOT GENERATION SUMMARY")
    print("========================================")
    print(f"Successfully generated: {successful}")
    print(f"Reused from cache:      {skipped}")
    print(f"Failed:                 {failed}")

    if failed:
        sys.exit(1)

    print("\n[PASS] MOVING SHOT GENERATION FINISHED.")


if __name__ == "__main__":
    main()

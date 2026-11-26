
import os
import shutil
import subprocess
import sys
from pathlib import Path


PROJECT = Path(__file__).resolve().parent.parent

FFMPEG = os.getenv("FFMPEG_PATH") or shutil.which("ffmpeg")

VALIDATOR = PROJECT / "scripts" / "01_validate_storyboard.py"

VIDEO_DIR = PROJECT / "assets" / "video"
SHOTS_DIR = VIDEO_DIR / "moving_shots"

END_CARD = PROJECT / "assets" / "images" / "end_card.jpg"
END_CARD_VIDEO = VIDEO_DIR / "end_card.mp4"
AUDIO = PROJECT / "assets" / "audio" / "final_mix.wav"
SUBTITLES = PROJECT / "assets" / "subtitles" / "en.srt"
CONCAT_LIST = VIDEO_DIR / "horizontal_concat.txt"
OUTPUT = PROJECT / "outputs" / "lalibela_horizontal.mp4"

DURATION_END_CARD = 4
FPS = 25

SHOTS = [f"S{i:02d}" for i in range(1, 9)]


def validate_storyboard():
    print("\nVALIDATING STORYBOARD...")

    result = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=PROJECT,
        check=False
    )

    if result.returncode != 0:
        raise RuntimeError("Storyboard validation failed.")

    print("[PASS] Storyboard validation completed.")


def is_valid_video(path):
    if not path.is_file() or path.stat().st_size == 0:
        return False

    result = subprocess.run(
        [FFMPEG, "-v", "error", "-i", str(path), "-f", "null", "-"],
        cwd=PROJECT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False
    )

    return result.returncode == 0


def check_required_files():
    if not FFMPEG:
        raise FileNotFoundError(
            "FFmpeg not found. Install FFmpeg and add it to PATH, "
            "or set the FFMPEG_PATH environment variable."
        )

    required_files = [END_CARD, AUDIO, SUBTITLES]

    for path in required_files:
        if not path.is_file():
            raise FileNotFoundError(f"Missing required file: {path}")

    for shot in SHOTS:
        path = SHOTS_DIR / f"{shot}.mp4"
        if not is_valid_video(path):
            raise FileNotFoundError(
                f"Missing or invalid moving shot: {path}"
            )

    print("[PASS] All required source files are available.")


def run_ffmpeg(command, step_name):
    try:
        subprocess.run(command, check=True, cwd=PROJECT)
    except subprocess.CalledProcessError as error:
        raise RuntimeError(
            f"{step_name} failed. FFmpeg exit code: {error.returncode}"
        ) from error


def create_end_card_video():
    if is_valid_video(END_CARD_VIDEO):
        print("[CACHE] Reusing valid end-card video.")
        return

    print("\nSTEP 1: Creating the end-card video...")

    temporary = END_CARD_VIDEO.with_name("end_card.tmp.mp4")
    temporary.unlink(missing_ok=True)

    command = [
        FFMPEG, "-y",
        "-loop", "1",
        "-framerate", str(FPS),
        "-i", str(END_CARD),
        "-t", str(DURATION_END_CARD),
        "-vf", "scale=1920:1080,format=yuv420p",
        "-r", str(FPS),
        "-an",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "20",
        str(temporary)
    ]

    run_ffmpeg(command, "End-card video creation")

    if not is_valid_video(temporary):
        temporary.unlink(missing_ok=True)
        raise RuntimeError("Generated end-card video failed validation.")

    temporary.replace(END_CARD_VIDEO)
    print("[PASS] End-card video created and validated.")


def prepare_concat_list():
    entries = [
        f"file 'moving_shots/{shot}.mp4'"
        for shot in SHOTS
    ]

    entries.append("file 'end_card.mp4'")

    CONCAT_LIST.write_text(
        "\n".join(entries) + "\n",
        encoding="utf-8"
    )

    print("[PASS] Video sequence prepared.")


def assemble_horizontal():
    if is_valid_video(OUTPUT):
        print("\n[CACHE] Reusing valid horizontal film.")
        print("Output:", OUTPUT)
        return

    print("\nSTEP 2: Preparing English subtitles...")

    subtitle_filter = (
        "subtitles=assets/subtitles/en.srt:"
        "force_style='FontName=Arial,"
        "FontSize=48,"
        "Bold=1,"
        "PrimaryColour=&H00FFFFFF,"
        "OutlineColour=&H00000000,"
        "Outline=3,"
        "Shadow=1,"
        "MarginV=55,"
        "Alignment=2'"
    )

    audio_filter = "afade=t=out:st=84:d=1,apad=pad_dur=4"

    temporary = OUTPUT.with_name("lalibela_horizontal.tmp.mp4")
    temporary.unlink(missing_ok=True)

    print("\nSTEP 3: Assembling the horizontal film...")
    print("Resolution: 1920x1080")
    print("Aspect ratio: 16:9")
    print("Frame rate: 25 fps")
    print("Expected duration: approximately 89 seconds")

    command = [
        FFMPEG, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(CONCAT_LIST),
        "-i", str(AUDIO),
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-vf", subtitle_filter,
        "-af", audio_filter,
        "-t", "89",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-movflags", "+faststart",
        str(temporary)
    ]

    run_ffmpeg(command, "Horizontal film assembly")

    if not is_valid_video(temporary):
        temporary.unlink(missing_ok=True)
        raise RuntimeError("Horizontal film failed video validation.")

    temporary.replace(OUTPUT)

    print("\n========================================")
    print("HORIZONTAL FILM ASSEMBLY SUMMARY")
    print("========================================")
    print("[PASS] Horizontal film created successfully.")
    print("Output:", OUTPUT)
    print("Resolution: 1920x1080")
    print("Aspect ratio: 16:9")
    print("Expected duration: approximately 89 seconds")


def main():
    validate_storyboard()
    check_required_files()

    VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    create_end_card_video()
    prepare_concat_list()
    assemble_horizontal()


if __name__ == "__main__":
    main()

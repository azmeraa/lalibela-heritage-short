
import subprocess
import sys
from pathlib import Path


PROJECT = Path(__file__).resolve().parent.parent

FFMPEG = r"C:\ffmpeg\ffmpeg-9.1-essentials_build\bin\ffmpeg.exe"

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
    """Validate the storyboard before assembling the film."""

    print("\nVALIDATING STORYBOARD...")

    result = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=PROJECT,
        check=False
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Storyboard validation failed. Film assembly stopped."
        )

    print("[PASS] Storyboard validation completed.")


def check_required_files():
    """Check that all source files needed for assembly exist."""

    required_files = [
        Path(FFMPEG),
        END_CARD,
        AUDIO,
        SUBTITLES,
    ]

    for path in required_files:
        if not path.exists():
            raise FileNotFoundError(
                f"Missing required file: {path}"
            )

    for shot in SHOTS:
        path = SHOTS_DIR / f"{shot}.mp4"

        if not path.exists():
            raise FileNotFoundError(
                f"Missing moving shot: {path}"
            )

    print("[PASS] All required source files are available.")


def run_ffmpeg(command, step_name):
    """Run FFmpeg and report errors clearly."""

    try:
        subprocess.run(
            command,
            check=True,
            cwd=PROJECT
        )
    except subprocess.CalledProcessError as error:
        raise RuntimeError(
            f"{step_name} failed. FFmpeg exit code: "
            f"{error.returncode}"
        ) from error


def main():

    # Step 0: Validate storyboard before assembly.
    validate_storyboard()

    # Check required source files.
    check_required_files()

    VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    # Step 1: Create the 4-second end-card video.
    print("\nSTEP 1: Creating the end-card video...")

    end_card_command = [
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
        str(END_CARD_VIDEO)
    ]

    run_ffmpeg(end_card_command, "End-card video creation")

    print("[PASS] End-card video created.")

    # Step 2: Prepare the ordered video list.
    print("\nSTEP 2: Preparing the video sequence...")

    entries = []

    for shot in SHOTS:
        relative_path = f"moving_shots/{shot}.mp4"
        entries.append(f"file '{relative_path}'")

    entries.append("file 'end_card.mp4'")

    CONCAT_LIST.write_text(
        "\n".join(entries) + "\n",
        encoding="utf-8"
    )

    print("[PASS] Video sequence prepared.")

    # Step 3: Prepare English subtitles.
    print("\nSTEP 3: Preparing English subtitles...")

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

    # Step 4: Prepare audio fade-out and silence for end card.
    audio_filter = "afade=t=out:st=84:d=1,apad=pad_dur=4"

    # Step 5: Assemble the horizontal film.
    print("\nSTEP 4: Assembling the horizontal film...")
    print("Resolution: 1920x1080")
    print("Aspect ratio: 16:9")
    print("Frame rate: 25 fps")
    print("Subtitle style: Arial Bold, 48 px")
    print("Expected duration: approximately 89 seconds")

    assembly_command = [
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
        str(OUTPUT)
    ]

    run_ffmpeg(assembly_command, "Horizontal film assembly")

    if not OUTPUT.exists() or OUTPUT.stat().st_size == 0:
        raise RuntimeError(
            "Assembly finished without producing a valid output file."
        )

    print("\n========================================")
    print("HORIZONTAL FILM ASSEMBLY SUMMARY")
    print("========================================")
    print("[PASS] Horizontal film created successfully.")
    print("Output:", OUTPUT)
    print("Resolution: 1920x1080")
    print("Aspect ratio: 16:9")
    print("Expected duration: approximately 89 seconds")


if __name__ == "__main__":
    main()

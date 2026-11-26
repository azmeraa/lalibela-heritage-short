
#!/usr/bin/env python3
"""Validate and assemble the narration audio track."""

import json
import subprocess
import sys
import wave
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent

VALIDATOR = PROJECT_DIR / "scripts" / "01_validate_storyboard.py"
AUDIO_DIR = PROJECT_DIR / "assets" / "audio"
SCRIPT_FILE = AUDIO_DIR / "narration_script.json"
OUTPUT_FILE = AUDIO_DIR / "narration_track.wav"


def validate_storyboard():
    """Stop assembly if storyboard validation fails."""
    print("\nValidating storyboard...")

    result = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=PROJECT_DIR,
        check=False
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Storyboard validation failed. Audio assembly stopped."
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

    scenes = data["scenes"]
    total_duration = data["total_duration_seconds"]

    if not scenes:
        raise ValueError("No narration scenes found.")

    clips = []
    audio_format = None

    # Check all required clips before assembling.
    for scene in scenes:
        filename = (
            f"{scene['scene_id']}_{scene['language']}.wav"
        )
        audio_file = AUDIO_DIR / filename

        if not audio_file.is_file():
            raise FileNotFoundError(
                f"Missing audio clip: {audio_file}"
            )

        try:
            with wave.open(str(audio_file), "rb") as wav:
                params = wav.getparams()
                frames = wav.readframes(wav.getnframes())
        except (wave.Error, EOFError) as error:
            raise ValueError(
                f"Invalid WAV audio file: {filename}"
            ) from error

        current_format = (
            params.nchannels,
            params.sampwidth,
            params.framerate,
            params.comptype
        )

        if audio_format is None:
            audio_format = current_format
        elif current_format != audio_format:
            raise ValueError(
                f"Audio format mismatch in {filename}"
            )

        if params.nframes == 0:
            raise ValueError(
                f"Audio clip is empty: {filename}"
            )

        frame_size = params.nchannels * params.sampwidth
        clip_frames = len(frames) // frame_size

        start_frame = round(
            scene["start"] * params.framerate
        )
        end_frame = start_frame + clip_frames
        scene_end_frame = round(
            scene["end"] * params.framerate
        )

        if end_frame > scene_end_frame:
            raise ValueError(
                f"{filename} exceeds its scene duration."
            )

        clips.append((start_frame, frames, filename))

    channels, sample_width, sample_rate, _ = audio_format
    frame_size = channels * sample_width
    total_frames = round(total_duration * sample_rate)

    track = bytearray(total_frames * frame_size)

    for start_frame, frames, filename in clips:
        start_byte = start_frame * frame_size
        end_byte = start_byte + len(frames)

        if end_byte > len(track):
            raise ValueError(
                f"{filename} exceeds the total track duration."
            )

        track[start_byte:end_byte] = frames

        print(
            f"[PLACED] {filename} at "
            f"{start_frame / sample_rate:.2f}s"
        )

    # Write the assembled track.
    with wave.open(str(OUTPUT_FILE), "wb") as output:
        output.setnchannels(channels)
        output.setsampwidth(sample_width)
        output.setframerate(sample_rate)
        output.writeframes(track)

    # Verify the completed WAV file.
    with wave.open(str(OUTPUT_FILE), "rb") as output:
        actual_duration = (
            output.getnframes() / output.getframerate()
        )

        if output.getnframes() != total_frames:
            raise RuntimeError(
                "Output audio duration does not match the expected duration."
            )

    print("\n" + "=" * 55)
    print("[SUCCESS] Narration track assembled and verified.")
    print(f"Output: {OUTPUT_FILE}")
    print(f"Duration: {actual_duration:.2f} seconds")
    print(f"Audio clips: {len(clips)}")
    print(
        f"Format: {sample_rate} Hz, "
        f"{channels} channel(s), {sample_width * 8}-bit PCM"
    )


if __name__ == "__main__":
    main()

import os
import base64
import wave
from pathlib import Path
from dotenv import load_dotenv
from google import genai

PROJECT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_DIR / ".env")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is missing from .env")

MODEL = "gemini-3.8-flash-tts"
VOICE = "Charon"

SCRIPT = PROJECT_DIR / "walkthrough" / "scripts" / "walkthrough_narration.txt"
OUTPUT = PROJECT_DIR / "walkthrough" / "generated" / "audio" / "walkthrough_voice.wav"

text = SCRIPT.read_text(encoding="utf-8").strip()
if not text:
    raise RuntimeError("Walkthrough narration is empty.")

client = genai.Client(
    api_key=api_key,
    http_options={"api_version": "v1beta"}
)

print("Generating walkthrough narration...")
print("Model:", MODEL)
print("Voice:", VOICE)
print("Words:", len(text.split()))

interaction = client.interactions.create(
    model=MODEL,
    input=[{
        "type": "user_input",
        "content": [{
            "type": "text",
            "text": text,
            "annotations": [{
                "type": "speech_metadata",
                "style": (
                    "Professional male documentary presenter. "
                    "Warm, confident, clear, natural pacing. "
                    "Speak conversationally with clear pronunciation "
                    "and short pauses between sections."
                )
            }]
        }]
    }],
    response_format={"type": "audio"},
    generation_config={
        "speech_config": [{"voice": VOICE}]
    }
)

audio_data = interaction.output_audio.data
audio_bytes = (
    base64.b64decode(audio_data)
    if isinstance(audio_data, str)
    else audio_data
)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_bytes(audio_bytes)

with wave.open(str(OUTPUT), "rb") as audio:
    duration = audio.getnframes() / audio.getframerate()
    print("Duration:", round(duration, 2), "seconds")
    print("Channels:", audio.getnchannels())
    print("Sample rate:", audio.getframerate())

print("[SUCCESS] Walkthrough voice saved:", OUTPUT)


import os
import base64
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Load API key securely
load_dotenv()

if not os.getenv("GEMINI_API_KEY"):
    raise RuntimeError("GEMINI_API_KEY not found in .env")

# Use the required Gemini TTS model and API version
client = genai.Client(
    http_options={"api_version": "v1beta"}
)

text = (
    "Welcome to Lalibela, Ethiopia, "
    "where extraordinary churches were carved from solid rock."
)

interaction = client.interactions.create(
    model="gemini-3.8-flash-tts",
    input=[{
        "type": "user_input",
        "content": [{
            "type": "text",
            "text": text,
            "annotations": [{
                "type": "speech_metadata",
                "style": (
                    "Warm, clear, natural documentary narration. "
                    "Calm and expressive, with measured pacing "
                    "suitable for an international audience."
                )
            }]
        }]
    }],
    response_format={"type": "audio"},
    generation_config={
        "speech_config": [
            {"voice": "Kore"}
        ]
    }
)

audio_data = interaction.output_audio.data

output_dir = Path("assets/audio")
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "english_tts_test.wav"

output_file.write_bytes(base64.b64decode(audio_data))

print("SUCCESS: English TTS audio generated.")
print(f"Audio saved to: {output_file}")

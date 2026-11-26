
import os
import base64
from pathlib import Path
from dotenv import load_dotenv
from google import genai

load_dotenv()

if not os.getenv("GEMINI_API_KEY"):
    raise RuntimeError("GEMINI_API_KEY not found in .env")

client = genai.Client(
    http_options={"api_version": "v1beta"}
)

text = (
    "ከዓለም የተለያዩ አቅጣጫዎች፣ "
    "ሰዎች የኢትዮጵያን ታሪክ ለማወቅ ይጓዛሉ።"
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
                    "Natural, warm and respectful Amharic documentary "
                    "narration. Speak clearly with accurate Amharic "
                    "pronunciation, measured pacing and a calm tone."
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

output_file = output_dir / "amharic_tts_test.wav"
output_file.write_bytes(base64.b64decode(audio_data))

print("SUCCESS: Amharic TTS audio generated.")
print(f"Audio saved to: {output_file}")

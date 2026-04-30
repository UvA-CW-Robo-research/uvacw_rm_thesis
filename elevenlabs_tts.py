"""
ElevenLabs v3 TTS — NAO Robot Voice File Generator
Generates MP3 voice files suitable for playback on a NAO robot.
"""

!pip install elevenlabs

import os
import requests

# ── Configuration ──────────────────────────────────────────────────────────────
API_KEY   = "YOUR_API_KEY_HERE"          # Replace with your (new) API key
VOICE_ID  = "21m00Tcm4TlvDq8ikWAM"      # Default: "Rachel" — change as needed
MODEL_ID  = "eleven_v3"
OUTPUT_DIR = "nao_voice_files"

# NAO-friendly audio format: MP3 22050 Hz works well on NAO's audio system
OUTPUT_FORMAT = "mp3_22050_32"           # 22050 Hz, 32 kbps

# ── Phrases to generate ────────────────────────────────────────────────────────
phrases = {
    "greeting":      "Hello! I am NAO. How can I help you today?",
    "farewell":      "Goodbye! It was nice talking to you.",
    "confirmation":  "Sure, I will do that right away.",
    "error":         "I'm sorry, I did not understand that. Could you repeat?",
    "idle":          "I am ready and waiting for your instructions.",
}

# ── API call ───────────────────────────────────────────────────────────────────
def generate_voice(text: str, filename: str) -> None:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json",
    }

    payload = {
        "text": text,
        "model_id": MODEL_ID,
        "output_format": OUTPUT_FORMAT,
        "voice_settings": {
            "stability": 0.55,         # Higher = more consistent, less expressive
            "similarity_boost": 0.75,  # Higher = closer to original voice
            "style": 0.2,              # Slight style exaggeration for clarity
            "use_speaker_boost": True,
        },
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(response.content)
        print(f"[OK]  Saved: {filepath}")
    else:
        print(f"[ERR] {filename} — {response.status_code}: {response.text}")


# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for name, text in phrases.items():
        generate_voice(text, f"{name}.mp3")

    print(f"\nDone. Files saved to: ./{OUTPUT_DIR}/")

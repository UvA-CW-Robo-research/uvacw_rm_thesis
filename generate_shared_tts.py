"""
Generates, plays, and saves shared condition audio files.
Reads content from texts/shared.json.

Run with Python 3 (outside nao_env):
    python3 generate_shared_tts.py

Requires:
    pip install python-dotenv requests
"""

import json
import os
import subprocess
import tempfile
import requests
from dotenv import load_dotenv

load_dotenv()

# ── Configuration ──────────────────────────────────────────────────────────────
VOICE_ID      = "JGzTGubAVbbgG0SsLIlg"   # Riley
MODEL_ID      = "eleven_v3"
OUTPUT_FORMAT = "mp3_22050_32"
OUTPUT_DIR    = "nao_voice_files"
TEXTS_FILE    = "texts/shared.json"
API_KEY       = os.getenv("ELEVENLABS_API_KEY")

HEADERS = {
    "xi-api-key": API_KEY,
    "Content-Type": "application/json",
}

VOICE_SETTINGS_DEFAULT = {
    "stability": 0.40,
    "similarity_boost": 0.75,
    "style": 0.45,
    "use_speaker_boost": True,
}

# ── Helpers ────────────────────────────────────────────────────────────────────
def generate_tts(text: str) -> bytes:
    response = requests.post(
        "https://api.elevenlabs.io/v1/text-to-speech/{}".format(VOICE_ID),
        params={"output_format": OUTPUT_FORMAT},
        headers=HEADERS,
        json={
            "text": text,
            "model_id": MODEL_ID,
            "voice_settings": VOICE_SETTINGS_DEFAULT,
        },
    )
    response.raise_for_status()
    return response.content


def play_audio(audio_bytes: bytes) -> None:
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name
    subprocess.call(["afplay", tmp_path])
    os.remove(tmp_path)


def save_audio(audio_bytes: bytes, filename: str) -> str:
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "wb") as f:
        f.write(audio_bytes)
    return path


# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(TEXTS_FILE, "r") as f:
        lines = json.load(f)

    for key, item in lines.items():
        print("\n[{}]".format(key))

        for clip in item["clips"]:
            clip_id = clip["id"]
            text    = clip["text"]

            print("  Generating TTS: \"{}\"".format(text))
            tts_bytes = generate_tts(text)
            tts_path  = save_audio(tts_bytes, "{}.mp3".format(clip_id))
            print("  Saved → {}".format(tts_path))
            print("  Playing TTS...")
            play_audio(tts_bytes)

        input("  Press Enter for next line...")

    print("\nAll files saved to ./{}/".format(OUTPUT_DIR))

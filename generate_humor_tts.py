"""
Generates, plays, and saves humor condition audio files.
Reads content and delivery metadata from texts/humor.json.

Run with Python 3 (outside nao_env):
    python3 generate_humor.py

Requires:
    pip install python-dotenv requests
"""

import json
import os
import subprocess
import tempfile
import requests
from dotenv import load_dotenv

# ── Load .env from project root ────────────────────────────────────────────────
PROJECT_ROOT = "/Users/ada/Documents/GitHub/uvacw_rm_thesis"
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

# ── Configuration ──────────────────────────────────────────────────────────────
VOICE_ID      = "JGzTGubAVbbgG0SsLIlg"   # Riley
MODEL_ID      = "eleven_v3"
OUTPUT_FORMAT = "mp3_22050_32"
OUTPUT_DIR    = os.path.join(PROJECT_ROOT, "nao_voice_files")
TEXTS_FILE    = os.path.join(PROJECT_ROOT, "texts", "humor.json")
API_KEY       = os.getenv("ELEVENLABS_API_KEY")

HEADERS = {
    "xi-api-key": API_KEY,
    "Content-Type": "application/json",
}

# Default voice — statements, punchlines
VOICE_SETTINGS_DEFAULT = {
    "stability": 0.40,
    "similarity_boost": 0.75,
    "style": 0.45,
    "use_speaker_boost": True,
}

# Question voice — low stability, high style = pitch rise + curiosity
VOICE_SETTINGS_QUESTION = {
    "stability": 0.10,
    "similarity_boost": 0.75,
    "style": 0.80,
    "use_speaker_boost": True,
}

# ── Helpers ────────────────────────────────────────────────────────────────────
def generate_tts(text: str, voice_type: str = "default") -> bytes:
    settings = VOICE_SETTINGS_QUESTION if voice_type == "question" else VOICE_SETTINGS_DEFAULT
    response = requests.post(
        "https://api.elevenlabs.io/v1/text-to-speech/{}".format(VOICE_ID),
        params={"output_format": OUTPUT_FORMAT},
        headers=HEADERS,
        json={
            "text": text,
            "model_id": MODEL_ID,
            "voice_settings": settings,
        },
    )
    response.raise_for_status()
    return response.content


def generate_sfx(prompt: str, duration_seconds: float = None) -> bytes:
    payload = {
        "text": prompt,
        "prompt_influence": 0.7,
    }
    if duration_seconds:
        payload["duration_seconds"] = duration_seconds

    response = requests.post(
        "https://api.elevenlabs.io/v1/sound-generation",
        headers=HEADERS,
        json=payload,
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
        humor_lines = json.load(f)

    for key, item in humor_lines.items():
        print("\n[{}]".format(key))

        for clip in item["clips"]:
            clip_id      = clip["id"]
            text         = clip["text"]
            voice_type   = clip.get("voice", "default")
            sfx_prompt   = clip.get("sfx")
            sfx_duration = clip.get("sfx_duration")

            print("  Generating TTS [{}]: \"{}\"".format(voice_type, text))
            tts_bytes = generate_tts(text, voice_type)
            tts_path  = save_audio(tts_bytes, "{}.mp3".format(clip_id))
            print("  Saved → {}".format(tts_path))
            print("  Playing TTS...")
            play_audio(tts_bytes)

            if sfx_prompt:
                print("  Generating SFX: '{}'".format(sfx_prompt))
                sfx_bytes = generate_sfx(sfx_prompt, sfx_duration)
                sfx_path  = save_audio(sfx_bytes, "{}_sfx.mp3".format(clip_id))
                print("  Saved SFX → {}".format(sfx_path))
                print("  Playing SFX...")
                play_audio(sfx_bytes)

        input("  Press Enter for next line...")

    print("\nAll files saved to ./{}/".format(OUTPUT_DIR))

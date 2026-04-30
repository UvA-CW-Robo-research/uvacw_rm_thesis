"""
ElevenLabs v3 TTS — NAO Robot Voice File Generator
Reads phrase JSONs from /texts, outputs WAVs to /nao_voice_files.
Skips files that already exist to save API credits.

Folder structure:
    texts/
        shared.json
        humor.json
        no_humor.json
        failure.json
        no_failure.json
    nao_voice_files/     ← generated WAV files land here
    generate_tts.py
"""

import os
import json
import requests

# ── Configuration ──────────────────────────────────────────────────────────────
API_KEY       = "YOUR_API_KEY_HERE"       # Replace with the ElevenLabs API key
VOICE_ID      = "JGzTGubAVbbgG0SsLIlg"   # Voice name: Riley
MODEL_ID      = "eleven_v3"
OUTPUT_FORMAT = "wav_22050"               # NAO is compatible with 22050 Hz WAV
OUTPUT_DIR    = "nao_voice_files"
TEXTS_DIR     = "texts"

# Voice settings per file type
VOICE_SETTINGS_DEFAULT = {
    "stability": 0.55,
    "similarity_boost": 0.75,
    "style": 0.2,
    "use_speaker_boost": True,
}

# Lower stability for the glitch file to add slight irregularity
VOICE_SETTINGS_GLITCH = {
    "stability": 0.25,
    "similarity_boost": 0.75,
    "style": 0.3,
    "use_speaker_boost": True,
}

# JSON files to process
TEXT_FILES = [
    "shared.json",
    "humor.json",
    "no_humor.json",
    "failure.json",
    "no_failure.json",
]

# Keys that should use the glitch voice settings
GLITCH_KEYS = {"seq_8_2_failure"}

# ── API call ───────────────────────────────────────────────────────────────────
def generate_voice(key: str, text: str) -> None:
    output_path = os.path.join(OUTPUT_DIR, f"{key}.wav")

    # Skip if already generated
    if os.path.exists(output_path):
        print(f"[SKIP] {key}.wav already exists.")
        return

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json",
    }

    voice_settings = VOICE_SETTINGS_GLITCH if key in GLITCH_KEYS else VOICE_SETTINGS_DEFAULT

    payload = {
        "text": text,
        "model_id": MODEL_ID,
        "output_format": OUTPUT_FORMAT,
        "voice_settings": voice_settings,
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"[OK]   {key}.wav")
    else:
        print(f"[ERR]  {key}.wav — {response.status_code}: {response.text}")


# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    total = 0
    skipped = 0
    success = 0
    failed = 0

    for filename in TEXT_FILES:
        filepath = os.path.join(TEXTS_DIR, filename)

        if not os.path.exists(filepath):
            print(f"[WARN] {filename} not found, skipping.")
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            phrases = json.load(f)

        print(f"\n── {filename} ({len(phrases)} phrases) ──")

        for key, text in phrases.items():
            total += 1
            output_path = os.path.join(OUTPUT_DIR, f"{key}.wav")

            if os.path.exists(output_path):
                skipped += 1
                print(f"[SKIP] {key}.wav already exists.")
            else:
                generate_voice(key, text)
                if os.path.exists(output_path):
                    success += 1
                else:
                    failed += 1

    print(f"""
── Summary ──────────────────────────────
  Total phrases : {total}
  Generated     : {success}
  Skipped       : {skipped}
  Failed        : {failed}
  Output folder : ./{OUTPUT_DIR}/
─────────────────────────────────────────
""")

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
    .env                 ← contains ELEVENLABS_API_KEY
    generate_tts.py

Run with Python 3 (outside nao_env):
    pip install elevenlabs python-dotenv
    python3 generate_tts.py
"""

import os
import json
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()

# ── Configuration ──────────────────────────────────────────────────────────────
VOICE_ID      = "21m00Tcm4TlvDq8ikWAM"   # Default: Rachel — change as needed
MODEL_ID      = "eleven_v3"
OUTPUT_FORMAT = "wav_22050"               # 22050 Hz WAV — NAO compatible
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

# ── Init ElevenLabs client ─────────────────────────────────────────────────────
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

# ── Generate one voice file ────────────────────────────────────────────────────
def generate_voice(key, text):
    output_path = os.path.join(OUTPUT_DIR, "{}.wav".format(key))

    if os.path.exists(output_path):
        print("[SKIP] {}.wav already exists.".format(key))
        return

    voice_settings = VOICE_SETTINGS_GLITCH if key in GLITCH_KEYS else VOICE_SETTINGS_DEFAULT

    try:
        audio = client.text_to_speech.convert(
            text=text,
            voice_id=VOICE_ID,
            model_id=MODEL_ID,
            output_format=OUTPUT_FORMAT,
            voice_settings=voice_settings,
        )

        with open(output_path, "wb") as f:
            for chunk in audio:
                f.write(chunk)

        print("[OK]   {}.wav".format(key))

    except Exception as e:
        print("[ERR]  {}.wav — {}".format(key, e))


# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    total   = 0
    skipped = 0
    success = 0
    failed  = 0

    for filename in TEXT_FILES:
        filepath = os.path.join(TEXTS_DIR, filename)

        if not os.path.exists(filepath):
            print("[WARN] {} not found, skipping.".format(filename))
            continue

        with open(filepath, "r") as f:
            phrases = json.load(f)

        print("\n── {} ({} phrases) ──".format(filename, len(phrases)))

        for key, text in phrases.items():
            total += 1
            output_path = os.path.join(OUTPUT_DIR, "{}.wav".format(key))

            if os.path.exists(output_path):
                skipped += 1
                print("[SKIP] {}.wav already exists.".format(key))
            else:
                generate_voice(key, text)
                if os.path.exists(output_path):
                    success += 1
                else:
                    failed += 1

    print("""
── Summary ──────────────────────────────
  Total phrases : {}
  Generated     : {}
  Skipped       : {}
  Failed        : {}
  Output folder : ./{}/
─────────────────────────────────────────
""".format(total, success, skipped, failed, OUTPUT_DIR))

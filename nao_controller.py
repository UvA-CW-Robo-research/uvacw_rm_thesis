"""
NAO Teleoperation Controller
Runs on experimenter's laptop (Python 2.7), sends commands to NAO over WiFi.

Requirements:
    - NAOqi Python 2.7 SDK on laptop
    - WAVs uploaded to NAO at /home/nao/nao_voice_files/
    - pip install pygame (for spacebar capture)

Run:
    python nao_controller.py
"""

import sys
import time
import pygame
import naoqi
from naoqi import ALProxy

# ── Configuration ──────────────────────────────────────────────────────────────
ROBOT_IP   = "192.168.0.102"
PORT       = 9559
AUDIO_DIR  = "/home/nao/nao_voice_files/"

# ── NAOqi proxies ──────────────────────────────────────────────────────────────
def connect():
    print("Connecting to NAO at {}:{}...".format(ROBOT_IP, PORT))
    try:
        audio   = ALProxy("ALAudioPlayer",  ROBOT_IP, PORT)
        leds    = ALProxy("ALLeds",         ROBOT_IP, PORT)
        tracker = ALProxy("ALFaceTracker",  ROBOT_IP, PORT)
        motion  = ALProxy("ALMotion",       ROBOT_IP, PORT)
        print("Connected.\n")
        return audio, leds, tracker, motion
    except Exception as e:
        print("Connection failed: {}".format(e))
        sys.exit(1)

# ── NAO behaviours ─────────────────────────────────────────────────────────────
def start_face_tracking(tracker, motion):
    motion.setStiffnesses("Head", 1.0)
    tracker.setWholeBodyOn(False)
    tracker.startTracking()
    print("  [NAO] Face tracking started.")

def stop_face_tracking(tracker, motion):
    tracker.stopTracking()
    motion.setStiffnesses("Head", 0.0)
    print("  [NAO] Face tracking stopped.")

def blink_eyes(leds):
    """Single natural blink on both eyes."""
    leds.fadeRGB("FaceLeds", 0x00000000, 0.1)   # off
    time.sleep(0.15)
    leds.fadeRGB("FaceLeds", 0x0000FFFF, 0.1)   # back on (white-blue NAO default)
    print("  [NAO] Eye blink done.")

def play_clip(audio, filename):
    """Play a WAV file from NAO's local filesystem and block until done."""
    path = AUDIO_DIR + filename
    print("     Playing: {}".format(path))
    task_id = audio.post.playFile(path)
    audio.wait(task_id, 0)

# ── Keyboard helper ────────────────────────────────────────────────────────────
def wait_for_space(label):
    print("\n  [{}/{}] {}".format(label[0], label[1], label[2]))
    print("     Press SPACE to play...")
    pygame.event.clear()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        pygame.time.wait(30)

# ── Sequence builder ───────────────────────────────────────────────────────────
def build_sequence(condition):
    """
    condition:
        1 = C1 Error   + Humor
        2 = C2 Error   + No Humor
        3 = C3 No Error + Humor
        4 = C4 No Error + No Humor
    """
    humor   = condition in (1, 3)
    error   = condition in (1, 2)
    seq_9_2 = "task_error_seq_9_2.wav" if error else "task_no_error_seq_9_2.wav"
    seq_9_2_label = "9-digit seq 2: 7 2 9 GREEN 1 6 3 8 4  [ERROR]" if error \
                    else "9-digit seq 2: 7 2 9 5 1 6 3 8 4"

    steps = []

    # ── INTRODUCTION ──────────────────────────────────────────────────────────
    if humor:
        steps += [
            {"label": "NAO intro — Hello / my name is NAO",            "clips": ["intro_humor_1a.wav"]},
            {"label": "NAO intro — I prepared a joke",                  "clips": ["intro_humor_1b.wav"]},
            {"label": "NAO intro — Which days are the strongest?",      "clips": ["intro_humor_1c.wav"]},
            {"label": "NAO joke  — Saturday and Sunday",                "clips": ["intro_humor_2.wav"]},
            {"label": "NAO joke  — SFX: trombone (wah wah wah)",        "clips": ["intro_humor_3a_sfx.wav"]},
            {"label": "NAO joke  — Because the rest are…",              "clips": ["intro_humor_3a.wav"]},
            {"label": "NAO joke  — weak-days",                          "clips": ["intro_humor_3b.wav"]},
        ]

    steps += [
        {"label": "NAO intro — self intro + task description",          "clips": ["intro_shared_1.wav"]},
        {"label": "NAO intro — What's your name?",                      "clips": ["intro_shared_2.wav"]},
        {"label": "NAO intro — Nice to meet you!",                      "clips": ["intro_shared_3.wav"]},
    ]

    # ── TASK START ────────────────────────────────────────────────────────────
    if humor:
        steps += [
            {"label": "NAO task  — Alright, one more joke",             "clips": ["task_start_humor_1a.wav"]},
            {"label": "NAO task  — Where do cows go Saturday nights?",  "clips": ["task_start_humor_1b.wav"]},
            {"label": "NAO task  — The moooovies",                      "clips": ["task_start_humor_2.wav"]},
            {"label": "NAO task  — SFX: cow moo",                       "clips": ["task_start_humor_2_sfx.wav"]},
            {"label": "NAO task  — Okay I'm ready, go ahead",           "clips": ["task_start_humor_3.wav"]},
        ]
    else:
        steps += [
            {"label": "NAO task  — Alright I am ready to begin",        "clips": ["task_no_humor_ready.wav"]},
        ]

    # ── DIGIT SEQUENCES ───────────────────────────────────────────────────────
    sequences = [
        ("7-digit seq 1:  2 5 9 3 7 1 6",       "task_shared_seq_7_1.wav"),
        ("7-digit seq 2:  8 1 4 7 2 9 5",       "task_shared_seq_7_2.wav"),
        ("7-digit seq 3:  6 3 7 1 8 4 2",       "task_shared_seq_7_3.wav"),
        ("8-digit seq 1:  4 7 2 9 5 1 8 3",     "task_shared_seq_8_1.wav"),
        ("8-digit seq 2:  1 6 3 8 4 7 2 9",     "task_shared_seq_8_2.wav"),
        ("8-digit seq 3:  9 2 6 4 1 8 3 7",     "task_shared_seq_8_3.wav"),
        ("9-digit seq 1:  3 8 1 6 4 9 2 7 5",   "task_shared_seq_9_1.wav"),
        (seq_9_2_label,                          seq_9_2),
        ("9-digit seq 3:  5 4 7 2 8 1 6 3 9",   "task_shared_seq_9_3.wav"),
        ("10-digit seq 1: 2 6 9 3 7 4 1 8 5 2", "task_shared_seq_10_1.wav"),
        ("10-digit seq 2: 8 1 5 3 9 6 2 7 4 1", "task_shared_seq_10_2.wav"),
        ("10-digit seq 3: 4 9 2 7 5 3 8 1 6 4", "task_shared_seq_10_3.wav"),
    ]

    for lbl, fname in sequences:
        steps.append({"label": "NAO repeats — {}".format(lbl), "clips": [fname]})

    # ── TASK END ──────────────────────────────────────────────────────────────
    if humor:
        steps += [
            {"label": "NAO end   — End of task / one last joke",        "clips": ["end_humor_1a.wav"]},
            {"label": "NAO end   — Why do seagulls fly over the sea?",  "clips": ["end_humor_1b.wav"]},
            {"label": "NAO end   — SFX: rimshot (ba dum tss)",          "clips": ["end_humor_2a_sfx.wav"]},
            {"label": "NAO end   — Because if they flew over the bay…", "clips": ["end_humor_2a.wav"]},
            {"label": "NAO end   — they would be bay-gulls!",           "clips": ["end_humor_2b.wav"]},
            {"label": "NAO end   — Wonderful time, thank you!",         "clips": ["end_humor_3.wav"]},
        ]
    else:
        steps += [
            {"label": "NAO end   — End of task + thank you",            "clips": ["end_no_humor_1.wav"]},
        ]

    return steps

# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()

    # ── Condition selection ────────────────────────────────────────────────────
    print("\n╔══════════════════════════════════════╗")
    print("║     NAO TELEOPERATION CONTROLLER     ║")
    print("╠══════════════════════════════════════╣")
    print("║  Select condition:                   ║")
    print("║    1 — C1: Error    + Humor          ║")
    print("║    2 — C2: Error    + No Humor       ║")
    print("║    3 — C3: No Error + Humor          ║")
    print("║    4 — C4: No Error + No Humor       ║")
    print("╚══════════════════════════════════════╝")

    while True:
        choice = raw_input("\nEnter condition (1/2/3/4): ").strip()
        if choice in ("1", "2", "3", "4"):
            condition = int(choice)
            break
        print("  Invalid. Please enter 1, 2, 3, or 4.")

    condition_labels = {
        1: "C1 — Error + Humor",
        2: "C2 — Error + No Humor",
        3: "C3 — No Error + Humor",
        4: "C4 — No Error + No Humor",
    }
    print("\n  Condition: {}\n".format(condition_labels[condition]))

    # ── Connect to NAO ─────────────────────────────────────────────────────────
    audio, leds, tracker, motion = connect()

    # ── Setup: face tracking + eye blink ──────────────────────────────────────
    start_face_tracking(tracker, motion)
    blink_eyes(leds)

    # ── Build sequence ─────────────────────────────────────────────────────────
    sequence = build_sequence(condition)
    total    = len(sequence)
    print("\n  {} steps loaded. Press SPACE to trigger each clip.".format(total))

    raw_input("\n  Press ENTER when ready to begin...\n")

    # Minimal pygame window for key capture
    screen = pygame.display.set_mode((420, 80))
    pygame.display.set_caption("NAO Controller — {}".format(condition_labels[condition]))

    # ── Run session ────────────────────────────────────────────────────────────
    for i, step in enumerate(sequence):
        wait_for_space((i + 1, total, step["label"]))
        for clip in step["clips"]:
            play_clip(audio, clip)

    # ── Wrap up ────────────────────────────────────────────────────────────────
    stop_face_tracking(tracker, motion)
    print("\n  Session complete. Condition: {}".format(condition_labels[condition]))
    pygame.quit()
    sys.exit(0)

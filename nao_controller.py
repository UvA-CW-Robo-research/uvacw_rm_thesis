# -*- coding: utf-8 -*-
"""
NAO Teleoperation Controller
Runs on experimenter's laptop (Python 2.7), sends commands to NAO over WiFi.

Requirements:
    - NAOqi Python 2.7 SDK on laptop
    - WAVs uploaded to NAO at /home/nao/nao_voice_files/

Run:
    python nao_controller.py
"""

import sys
import time
import random
import threading
import naoqi
from naoqi import ALProxy

# ── Configuration ──────────────────────────────────────────────────────────────
ROBOT_IP   = "192.168.0.102"
PORT       = 9559
AUDIO_DIR  = "/home/nao/nao_voice_files/"

# ── Global blink control ───────────────────────────────────────────────────────
_blink_active = False
_blink_thread = None

# ── NAOqi proxies ──────────────────────────────────────────────────────────────
def connect():
    print("Connecting to NAO at {}:{}...".format(ROBOT_IP, PORT))
    try:
        audio   = ALProxy("ALAudioPlayer",  ROBOT_IP, PORT)
        leds    = ALProxy("ALLeds",         ROBOT_IP, PORT)
        tracker = ALProxy("ALTracker",      ROBOT_IP, PORT)
        motion  = ALProxy("ALMotion",       ROBOT_IP, PORT)
        posture = ALProxy("ALRobotPosture", ROBOT_IP, PORT)
        print("Connected.\n")
        return audio, leds, tracker, motion, posture
    except Exception as e:
        print("Connection failed: {}".format(e))
        sys.exit(1)

# ── NAO behaviours ─────────────────────────────────────────────────────────────
def set_posture(posture):
    """Put NAO in a stable sitting posture before anything else."""
    print("  [NAO] Going to Sit posture...")
    posture.goToPosture("Sit", 1.0)
    print("  [NAO] Sitting. Ready.")

def start_face_tracking(tracker, motion):
    motion.setStiffnesses("Head", 1.0)
    tracker.registerTarget("Face", 0.1)
    tracker.setMode("Head")
    tracker.track("Face")
    print("  [NAO] Face tracking started.")

def stop_face_tracking(tracker, motion):
    tracker.stopTracker()
    tracker.unregisterAllTargets()
    motion.setStiffnesses("Head", 0.0)
    print("  [NAO] Face tracking stopped.")

def _blink_loop(leds):
    """Background thread: blinks at random intervals (2–6 s) until stopped."""
    global _blink_active
    while _blink_active:
        time.sleep(random.uniform(2.0, 6.0))
        if not _blink_active:
            break
        leds.fadeRGB("FaceLeds", 0x00000000, 0.08)
        time.sleep(random.uniform(0.10, 0.20))
        leds.fadeRGB("FaceLeds", 0x00FFFFFF, 0.08)

def start_blinking(leds):
    """Start continuous random blinking in a background thread."""
    global _blink_active, _blink_thread
    _blink_active = True
    _blink_thread = threading.Thread(target=_blink_loop, args=(leds,))
    _blink_thread.daemon = True
    _blink_thread.start()
    print("  [NAO] Natural blinking started.")

def stop_blinking():
    """Stop the background blink thread."""
    global _blink_active
    _blink_active = False
    print("  [NAO] Natural blinking stopped.")

def play_clip(audio, filename):
    """Play a WAV file from NAO's local filesystem and block until done."""
    path = AUDIO_DIR + filename
    print("     Playing: {}".format(path))
    task_id = audio.post.playFile(path)
    audio.wait(task_id, 0)

# ── Keyboard helper ────────────────────────────────────────────────────────────
def wait_for_enter(label):
    print("\n  [{}/{}] {}".format(label[0], label[1], label[2]))
    raw_input("     Press ENTER to play...")

# ── Sequence builder ───────────────────────────────────────────────────────────
def build_sequence(condition):
    humor = condition in (1, 3)
    error = condition in (1, 2)

    seq_9_2       = "task_error_seq_9_2.wav"    if error else "task_no_error_seq_9_2.wav"
    seq_9_2_label = "9-digit seq 2: 7 2 9 GREEN 1 6 3 8 4  [ERROR]" if error \
                    else "9-digit seq 2: 7 2 9 5 1 6 3 8 4"

    steps = []

    # ── INTRODUCTION ──────────────────────────────────────────────────────────
    if humor:
        steps += [
            {"label": 'NAO intro — "Hello! My name is NAO."',
             "clips": ["intro_humor_1a.wav"]},
            {"label": 'NAO intro — "I prepared a joke for you."',
             "clips": ["intro_humor_1b.wav"]},
            {"label": 'NAO intro — "Which days are the strongest?!" [wait for reaction]',
             "clips": ["intro_humor_1c.wav"]},
            {"label": 'NAO joke  — "Saturday and Sunday." [wait for reaction]',
             "clips": ["intro_humor_2.wav"]},
            {"label": 'NAO joke  — "Because the rest are,"  →  SFX: trombone  →  "weak-days."',
             "clips": ["intro_humor_3a.wav", "intro_humor_3a_sfx.wav", "intro_humor_3b.wav"]},
        ]
    else:
        steps += [
            {"label": 'NAO intro — "Hello! My name is NAO. I\'m here for the short task…"',
             "clips": ["intro_shared_1.wav"]},
        ]

    steps += [
        {"label": 'NAO intro — "What\'s your name?" [wait for participant response]',
         "clips": ["intro_shared_2.wav"]},
        {"label": 'NAO intro — "Nice to meet you! I\'m looking forward to working with you."',
         "clips": ["intro_shared_3.wav"]},
    ]

    # ── TASK START ────────────────────────────────────────────────────────────
    if humor:
        steps += [
            {"label": 'NAO task  — "Alright, before we start, here\'s one more joke."',
             "clips": ["task_start_humor_1a.wav"]},
            {"label": 'NAO task  — "Where do cows go on Saturday nights?!" [wait]',
             "clips": ["task_start_humor_1b.wav"]},
            {"label": 'NAO task  — "The mooooovies."  →  SFX: cow moo [wait]',
             "clips": ["task_start_humor_2.wav", "task_start_humor_2_sfx.wav"]},
            {"label": 'NAO task  — "Okay, I\'m ready. Please go ahead with the first sequence."',
             "clips": ["task_start_humor_3.wav"]},
        ]
    else:
        steps += [
            {"label": 'NAO task  — "Alright, I am ready to begin. Please go ahead with the first sequence."',
             "clips": ["task_no_humor_ready.wav"]},
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
            {"label": 'NAO end   — "That is the end of the task. One last joke…"',
             "clips": ["end_humor_1a.wav"]},
            {"label": 'NAO end   — "Why do seagulls fly over the sea?!" [wait]',
             "clips": ["end_humor_1b.wav"]},
            {"label": 'NAO end   — "Because if they flew over the bay,"  →  SFX: rimshot  →  "they would be bay-gulls!"',
             "clips": ["end_humor_2a.wav", "end_humor_2a_sfx.wav", "end_humor_2b.wav"]},
            {"label": 'NAO end   — "I had a wonderful time working with you today. Thank you!"',
             "clips": ["end_humor_3.wav"]},
        ]
    else:
        steps += [
            {"label": 'NAO end   — "That is the end of the task… Thank you!"',
             "clips": ["end_no_humor_1.wav"]},
        ]

    return steps

# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":

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
    audio, leds, tracker, motion, posture = connect()

    # ── Sit posture ────────────────────────────────────────────────────────────
    set_posture(posture)

    # ── Setup: face tracking + white eyes + natural blinking ──────────────────
    start_face_tracking(tracker, motion)
    leds.fadeRGB("FaceLeds", 0x00FFFFFF, 0.5)
    start_blinking(leds)

    print("\n  [LIVE] NAO is blinking and tracking. Press ENTER when ready to begin...\n")
    raw_input("")

    # ── Build + run sequence ───────────────────────────────────────────────────
    sequence = build_sequence(condition)
    total    = len(sequence)
    print("\n  {} steps loaded.\n".format(total))

    for i, step in enumerate(sequence):
        wait_for_enter((i + 1, total, step["label"]))
        for clip in step["clips"]:
            play_clip(audio, clip)

    # ── Session complete — keep blinking + tracking until experimenter exits ───
    print("\n  Session complete. Condition: {}".format(condition_labels[condition]))
    print("  NAO is still blinking and tracking. Press ENTER to shut down...\n")
    raw_input("")

    stop_blinking()
    stop_face_tracking(tracker, motion)
    print("  NAO shut down. Goodbye.")
    sys.exit(0)


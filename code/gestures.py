# gestures.py
# Handles all NAO physical gestures: nod, wave, failure sequence, blinking

import time
import threading
from naoqi import ALProxy

def connect(ip, port):
    motion    = ALProxy("ALMotion",         str(ip), int(port))
    leds      = ALProxy("ALLeds",           str(ip), int(port))
    tts       = ALProxy("ALTextToSpeech",   str(ip), int(port))
    awareness = ALProxy("ALBasicAwareness", str(ip), int(port))
    posture   = ALProxy("ALRobotPosture",   str(ip), int(port))
    return motion, leds, tts, awareness, posture


def blink(leds):
    """Single natural blink."""
    leds.fadeRGB("FaceLeds", 0x000000, 0.05)
    time.sleep(0.15)
    leds.fadeRGB("FaceLeds", 0xFFFFFF, 0.05)


def speak_with_blink(tts, leds, text):
    """NAO speaks while blinking naturally."""
    stop_blinking = threading.Event()

    def blink_loop():
        while not stop_blinking.is_set():
            time.sleep(3.0)
            if not stop_blinking.is_set():
                blink(leds)

    blink_thread = threading.Thread(target=blink_loop)
    blink_thread.daemon = True
    blink_thread.start()

    tts.say(text)

    stop_blinking.set()


def nod(motion):
    """NAO nods head to show it is listening."""
    motion.setAngles("HeadPitch", 0.3, 0.15)
    time.sleep(0.4)
    motion.setAngles("HeadPitch", 0.0, 0.15)
    time.sleep(0.4)
    motion.setAngles("HeadPitch", 0.3, 0.15)
    time.sleep(0.4)
    motion.setAngles("HeadPitch", 0.0, 0.15)


def wave(motion):
    """NAO raises and waves right arm as goodbye gesture."""
    motion.setAngles("RShoulderPitch", -1.0, 0.2)
    motion.setAngles("RShoulderRoll",  -0.5, 0.2)
    time.sleep(1.0)
    for _ in range(3):
        motion.setAngles("RElbowRoll", 1.0, 0.5)
        time.sleep(0.4)
        motion.setAngles("RElbowRoll", 0.3, 0.5)
        time.sleep(0.4)
    motion.setAngles("RShoulderPitch", 1.4, 0.2)
    motion.setAngles("RShoulderRoll",  0.0, 0.2)


def failure_sequence(motion, leds, awareness):
    """
    Simulates robot failure:
    1. Stop awareness and freeze for 5 seconds with red LEDs
    2. Recover and restore awareness
    """
    print("[FAILURE SEQUENCE TRIGGERED]")

    # Stop face tracking during failure
    awareness.stopAwareness()

    # Stop movement and show red LEDs
    motion.stopMove()
    leds.fadeRGB("FaceLeds", 0xFF0000, 0.5)

    # Freeze for 5 seconds
    time.sleep(5)

    # Recover - restore white LEDs and face tracking
    leds.fadeRGB("FaceLeds", 0xFFFFFF, 0.5)
    awareness.startAwareness()

    print("[FAILURE SEQUENCE COMPLETE - press Enter to continue]")

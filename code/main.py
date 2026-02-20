# main.py
# Entry point for the NAO teleoperation experiment
# Usage: python code/main.py

import toml
from naoqi import ALProxy
from code.script import get_script
from code.gestures import connect
from code.controller import ExperimentController

def load_config():
    with open("config.toml", "r") as f:
        return toml.load(f)

def select_condition():
    print("\n=== NAO TELEOPERATION - SURVIVAL ON THE MOON ===")
    print("Conditions:")
    print("  1: Team Identity + Humor")
    print("  2: Team Identity + No Humor")
    print("  3: No Team Identity + Humor")
    print("  4: No Team Identity + No Humor")
    while True:
        try:
            condition = int(raw_input("\nEnter condition (1-4): "))
            if condition in [1, 2, 3, 4]:
                return condition
            else:
                print("Please enter a number between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    config    = load_config()
    ip        = config["robot"]["ip"]
    port      = config["robot"]["port"]
    condition = select_condition()

    print("\nConnecting to NAO at {}:{}...".format(ip, port))
    motion, leds, tts, awareness, posture = connect(ip, port)

    print("Connected! Waking up robot...")
    motion.wakeUp()

    print("Standing up...")
    posture.goToPosture("Stand", 0.5)

    print("Enabling face tracking...")
    awareness.setEngagementMode("FullyEngaged")
    awareness.setTrackingMode("Head")
    awareness.startAwareness()

    print("Enabling breathing animation...")
    motion.setBreathEnabled("Body", True)

    print("Condition {} selected. Loading script...".format(condition))
    script = get_script(condition)

    controller = ExperimentController(script, motion, leds, tts, awareness, condition)
    controller.run()

    print("Session complete. Shutting down...")
    motion.setBreathEnabled("Body", False)
    awareness.stopAwareness()
    motion.rest()

if __name__ == "__main__":
    main()
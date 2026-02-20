# controller.py
# Handles keyboard input and controls the flow of the experiment script

from pynput import keyboard
from code.gestures import nod, wave, failure_sequence, speak_with_blink

class ExperimentController:

    def __init__(self, script, motion, leds, tts, awareness, condition):
        self.script    = script
        self.motion    = motion
        self.leds      = leds
        self.tts       = tts
        self.awareness = awareness
        self.condition = condition
        self.index     = 0
        self.running   = True

        print("\n=== EXPERIMENT READY ===")
        print("Enter: next step | N: nod | F: failure sequence | W: wave | Esc: quit")
        print("========================\n")
        self.print_current_step()

    def print_current_step(self):
        if self.index < len(self.script):
            step_type, content = self.script[self.index]
            print("[Step {}/{}] [{}] {}".format(
                self.index + 1, len(self.script), step_type.upper(), content))
        else:
            print("[END OF SCRIPT]")

    def next_step(self):
        if self.index >= len(self.script):
            print("[END OF SCRIPT]")
            return

        step_type, content = self.script[self.index]

        if step_type == "speech":
            speak_with_blink(self.tts, self.leds, content)
        elif step_type == "wait":
            print("[WAIT] {}".format(content))
        elif step_type == "failure":
            print("[READY FOR FAILURE - Press F to trigger]")
            return
        elif step_type == "gesture":
            print("[READY FOR GESTURE - Press W to trigger]")
            return

        self.index += 1
        self.print_current_step()

    def on_press(self, key):
        try:
            if key == keyboard.Key.enter:
                self.next_step()
            elif key.char == 'n':
                nod(self.motion)
            elif key.char == 'f':
                failure_sequence(self.motion, self.leds, self.awareness)
                self.index += 1
                self.print_current_step()
            elif key.char == 'w':
                wave(self.motion)
                self.index += 1
                self.print_current_step()
        except AttributeError:
            if key == keyboard.Key.esc:
                print("\n[SHUTTING DOWN]")
                self.motion.setBreathEnabled("Body", False)
                self.awareness.stopAwareness()
                self.motion.rest()
                self.running = False
                return False

    def run(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()
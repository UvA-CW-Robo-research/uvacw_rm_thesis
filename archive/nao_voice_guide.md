# Changing NAO's Voice

## Check Available Voices

```bash
python -c "
from naoqi import ALProxy
tts = ALProxy('ALTextToSpeech', 'ENTER-NAO-IP-ADDRESS', ENTER-PORT-NUMBER)
print(tts.getAvailableVoices())
"
```

This robot has three voices: `maki_n16` (Japanese), `naoenu` (English default), `naomnc` (English alternative - but with a Chinese accent).

## Change Voice and Parameters

```bash
python -c "
from naoqi import ALProxy
tts = ALProxy('ALTextToSpeech', '192.168.0.102', 9559)
tts.setVoice('naoenu')
tts.setParameter('speed', 75)       # 50 (slow) to 200 (fast), default 100
tts.setParameter('pitchShift', 0.9) # below 1.0 = lower, above 1.0 = higher
tts.setParameter('volume', 100)     # 0 to 100
tts.say('Hello! My name is NAO. What is your name?')
"
```

## Current Settings

| Parameter | Value |
|-----------|-------|
| Voice | `naoenu` |
| Speed | `75` |
| Pitch | `0.9` |
| Volume | `100` |

## Notes

- Voice settings reset when the robot restarts. They are set permanently in `gestures.py` inside the `connect` function
- Additional voice packages are not freely available for NAO 2.8. Contact SoftBank support to order them

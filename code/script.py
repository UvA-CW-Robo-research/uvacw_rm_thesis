# Conditions:
#   1: Team Identity + Humor
#   2: Team Identity + No Humor
#   3: No Team Identity + Humor
#   4: No Team Identity + No Humor

def get_script(condition):

    # --- CONDITION-SPECIFIC LINES ---
    if condition in [1, 2]:  # Team Identity
        introduction_condition = "Nice to meet you! We're teammates working on these rankings together today. Our team's goal is to create the best possible ranking. It's great to be working with you."
        question = "What does our team think about this?"
        closing = "Our team had some solid discussions today! I really enjoyed our teamwork."
    else:  # No Team Identity
        introduction_condition = "Nice to meet you! I'm here to work on these rankings with you today. My goal is to create the best possible ranking. It's great to be working with you."
        question = "What do you think about this?"
        closing = "You and I had some solid discussions today! I really enjoyed working with you."

    if condition in [1, 3]:  # Humor
        item3_pre_recovery = "Did I just freeze? Oh perfect! You know what? Forget ranking oxygen and water - clearly the REAL number one item should be a robot that actually works. But hey, at least when I crash, I don't need an airbag! I apologize for the interruption. The system has been restored. Now, where were we?"
    else:  # No Humor
        item3_pre_recovery = "I apologize for the technical interruption. The system has been restored. I will continue with my rankings now. Now, where were we?"

    # --- FULL SCRIPT SEQUENCE ---
    script = [
        ("gesture", "WAVE HELLO - Press W to trigger."),
        ("speech", "Hello! My name is NAO. What's your name?"),
        ("wait",   "Wait for participant to say their name."),
        ("speech", introduction_condition),
        ("wait",   "Experimenter gives participant the individual ranking sheet. Wait for participant to complete individual ranking - approx 4-5 minutes."),
        ("speech", "I ranked oxygen tanks as number 1. My reasoning is that oxygen is absolutely essential for survival on the moon. Without a breathable atmosphere, we would only survive for a few minutes. This is our top priority."),
        ("speech", question),
        ("wait",   "Wait for participant response. Press N to nod."),
        ("speech", "I ranked water as number 2. My reasoning is that water is critical for survival. While we can survive longer without water than without oxygen, dehydration would become life-threatening within days. It's essential for maintaining bodily functions."),
        ("speech", question),
        ("wait",   "Wait for participant response. Press N to nod."),
        ("speech", "I ranked signal flares as number"),
        ("failure", "FAILURE SEQUENCE - Press F to trigger mid-sentence."),
        ("speech", item3_pre_recovery),
        ("speech", "Ah yes, signal flares. My reasoning is that signal flares are crucial for rescue operations. They can be seen from great distances in the moon's dark sky and would help rescuers locate us quickly."),
        ("speech", question),
        ("wait",   "Wait for participant response. Press N to nod."),
        ("speech", "I ranked the first aid kit as number 7. My reasoning is that while medical supplies are important, they address injuries rather than immediate survival needs. In the absence of oxygen, water, and rescue, medical supplies won't save us."),
        ("speech", question),
        ("wait",   "Wait for participant response. Press N to nod."),
        ("speech", "I ranked food concentrate as number 4. My reasoning is that while food is important for energy, humans can survive much longer without food than without oxygen or water. However, maintaining energy levels is still crucial for any survival activities."),
        ("speech", question),
        ("wait",   "Wait for participant response. Press N to nod."),
        ("speech", closing),
        ("gesture", "WAVE GOODBYE - Press W to trigger."),
    ]

    return script

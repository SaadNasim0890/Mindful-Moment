import json
import random

emotions = ["Stressed", "Tired", "Sad", "Confused", "Happy", "Anxious", "Angry", "Bored", "Overwhelmed"]

# Base templates for procedural generation to ensure variety and relevance
templates = {
    "Stressed": [
        ("Box Breathing", "Inhale 4s, hold 4s, exhale 4s, hold 4s. Repeat {n} times.", 2, ["breathing", "calm"]),
        ("Shoulder Roll", "Roll your shoulders backwards {n} times slowly.", 1, ["body", "relaxation"]),
        ("Desk Declutter", "Organize just {n} items on your desk to clear your mind.", 3, ["environment", "clarity"]),
        ("Quiet Sit", "Sit in silence for {n} minutes doing absolutely nothing.", 5, ["mindfulness", "rest"]),
    ],
    "Tired": [
        ("Water Break", "Drink {n} ml of cold water to rehydrate.", 1, ["health", "energy"]),
        ("Jumping Jacks", "Do {n} jumping jacks to get blood flowing.", 2, ["movement", "energy"]),
        ("Eye Rest", "Close your eyes and cover them with your palms for {n} seconds.", 1, ["health", "eyes"]),
        ("Fresh Air", "Step outside or open a window for {n} minutes.", 3, ["nature", "energy"]),
    ],
    "Sad": [
        ("Gratitude List", "List {n} small things you are grateful for right now.", 3, ["journaling", "positivity"]),
        ("Comfort Song", "Listen to your favorite song '{song}' (or similar).", 4, ["music", "mood"]),
        ("Kind Text", "Send a kind message to {person}.", 2, ["social", "connection"]),
        ("Texture Feel", "Touch a soft blanket or fabric for {n} minutes.", 2, ["sensory", "comfort"]),
    ],
    "Confused": [
        ("Brain Dump", "Write down {n} thoughts swirling in your head.", 5, ["writing", "clarity"]),
        ("Prioritize", "Pick the top {n} most important tasks and ignore the rest.", 3, ["planning", "focus"]),
        ("Walk & Think", "Take a {n} minute walk to clear your thoughts.", 10, ["movement", "clarity"]),
    ],
    "Happy": [
        ("Savoring", "Spend {n} minutes writing about why you feel good.", 3, ["journaling", "joy"]),
        ("Share Joy", "Tell {n} friends about your good news.", 2, ["social", "connection"]),
        ("Photo Memory", "Look at {n} photos that bring you joy.", 2, ["memory", "joy"]),
    ],
    "Anxious": [
        ("5-4-3-2-1", "Name {n} things you can see right now.", 2, ["grounding", "anxiety"]),
        ("Cold Water", "Run cold water over your wrists for {n} seconds.", 1, ["sensory", "calm"]),
        ("Deep Exhale", "Exhale for twice as long as you inhale for {n} cycles.", 3, ["breathing", "calm"]),
    ],
    "Angry": [
        ("Paper Tear", "Tear a piece of paper into {n} tiny pieces.", 2, ["release", "physical"]),
        ("Squeeze Ball", "Squeeze a stress ball or pillow {n} times.", 1, ["release", "physical"]),
        ("Count Down", "Count backwards from {n} to 0 slowly.", 1, ["mindfulness", "control"]),
    ],
    "Bored": [
        ("Doodle", "Draw {n} random shapes on a piece of paper.", 3, ["creativity", "fun"]),
        ("Learn New", "Read one article about a topic you know nothing about for {n} minutes.", 5, ["learning", "curiosity"]),
        ("Clean Up", "Clean {n} small area of your room.", 5, ["environment", "productivity"]),
    ],
    "Overwhelmed": [
        ("One Thing", "Focus on just ONE task for the next {n} minutes.", 5, ["focus", "productivity"]),
        ("No Screen", "Look away from all screens for {n} minutes.", 5, ["rest", "digital-detox"]),
        ("Floor Lie", "Lie flat on the floor for {n} minutes and feel the ground.", 3, ["grounding", "rest"]),
    ]
}

actions = []

# Generate variations
for emotion, emotion_templates in templates.items():
    for name, desc_template, base_duration, tags in emotion_templates:
        # Create variations for each template
        for i in range(1, 20): # Generate ~20 variations per template
            n_val = i * 2 + 1 # Variation in numbers
            
            # Variation in description
            desc = desc_template.replace("{n}", str(n_val))
            desc = desc.replace("{song}", random.choice(["Happy", "Roar", "Three Little Birds", "Don't Stop Believin'"]))
            desc = desc.replace("{person}", random.choice(["a friend", "a family member", "a colleague", "your partner"]))
            
            # Variation in title
            title_variations = [
                f"{name} {i}",
                f"{emotion} {name}",
                f"Quick {name}",
                f"Deep {name}",
                f"Mindful {name}"
            ]
            final_title = f"{name} (Level {i})"
            
            action = {
                "emotion": emotion,
                "action": final_title,
                "description": desc,
                "duration_minutes": base_duration + (i % 3), # Slight duration variation
                "tags": tags + [emotion.lower()]
            }
            actions.append(action)

# Add some specific curated ones to ensure high quality core set
curated = [
    {"emotion": "Stressed", "action": "4-7-8 Breathing", "description": "Inhale 4s, hold 7s, exhale 8s.", "duration_minutes": 3, "tags": ["breathing"]},
    {"emotion": "Happy", "action": "Victory Dance", "description": "Do a silly dance for 1 minute.", "duration_minutes": 1, "tags": ["movement"]},
    # ... (we could add more here)
]
actions.extend(curated)

print(f"Generated {len(actions)} actions.")

with open("data/micro_actions.json", "w") as f:
    json.dump(actions, f, indent=2)

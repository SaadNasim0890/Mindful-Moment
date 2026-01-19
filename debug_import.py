print("Importing schemas...")
try:
    from app.models.schemas import UserRequest
    print("Schemas imported.")
except Exception as e:
    print(f"Schemas failed: {e}")

print("Importing config...")
try:
    from app.core.config import get_settings
    print("Config imported.")
except Exception as e:
    print(f"Config failed: {e}")

print("Importing EmotionAgent...")
try:
    from app.agents.emotion_agent import EmotionAgent
    print("EmotionAgent imported.")
except Exception as e:
    print(f"EmotionAgent failed: {e}")

print("Importing PlannerAgent...")
try:
    from app.agents.planner_agent import PlannerAgent
    print("PlannerAgent imported.")
except Exception as e:
    print(f"PlannerAgent failed: {e}")

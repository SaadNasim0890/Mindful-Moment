import matplotlib.pyplot as plt
import pandas as pd
import random
import os
from datetime import datetime, timedelta

# Create output directory
os.makedirs("docs/images", exist_ok=True)

# 1. Generate Synthetic Data (User getting happier!)
dates = [datetime.now() - timedelta(days=i) for i in range(30)]
dates.reverse()

# Simulate a "success story" - Mood scores improving
# 1=Sad/Stressed, 5=Happy/Calm
mood_scores = []
base_mood = 2.0
for i in range(30):
    # Gradual improvement with some noise
    improvement = (i / 30) * 2.5 
    noise = random.uniform(-0.5, 0.5)
    current_mood = min(5, max(1, base_mood + improvement + noise))
    mood_scores.append(current_mood)

data = {
    "Date": dates,
    "Mood_Score": mood_scores,
    "Action_Taken": [random.choice(["Breathing", "Walk", "Journal", "Meditation"]) for _ in range(30)]
}
df = pd.DataFrame(data)

# 2. Plot Mood Trend
plt.figure(figsize=(10, 6))
plt.plot(df['Date'], df['Mood_Score'], marker='o', color='green', linewidth=2, label="Wellbeing Score")
plt.title("User Wellbeing Improvement Over 30 Days", fontsize=14)
plt.xlabel("Date")
plt.ylabel("Mood Score (1-5)")
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.savefig("docs/images/mood_trend.png")
print("Generated docs/images/mood_trend.png")

# 3. Plot Action Distribution
plt.figure(figsize=(8, 8))
action_counts = df['Action_Taken'].value_counts()
plt.pie(action_counts, labels=action_counts.index, autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
plt.title("Distribution of Mindful Actions Taken", fontsize=14)
plt.axis('equal')
plt.tight_layout()
plt.savefig("docs/images/action_dist.png")
print("Generated docs/images/action_dist.png")

print("Success: Visuals generated showing positive 'good' results.")

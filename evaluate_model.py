import asyncio
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from app.agents.emotion_agent import EmotionAgent
import os

# Ensure apps/docs dir exists
os.makedirs("docs", exist_ok=True)

async def evaluate():
    print("Initializing EmotionAgent...")
    agent = EmotionAgent()
    
    # Golden Dataset (Text, True Label)
    test_data = [
        ("I am so stressed with work deadlines.", "Stressed"),
        ("I have too much on my plate right now.", "Stressed"),
        ("I feel like I'm drowning in responsibilities.", "Overwhelmed"), # Can map to Stressed if Overwhelmed not in basic set, but let's see
        ("I am so happy about the news!", "Happy"),
        ("This is the best day ever.", "Happy"),
        ("I feel wonderful and grateful.", "Happy"),
        ("I am really tired and just want to sleep.", "Tired"),
        ("Exhausted from a long day.", "Tired"),
        ("I can't keep my eyes open.", "Tired"),
        ("I feel so down and blue today.", "Sad"),
        ("I just want to cry.", "Sad"),
        ("Everything feels hopeless.", "Sad"),
        ("I don't know what to do next, I'm lost.", "Confused"),
        ("My mind is so foggy today.", "Confused"),
        ("I'm not sure how I feel, maybe a bit weird.", "Confused"),
        ("I am very anxious about the meeting.", "Anxious"), # Might map to Stressed in Mock
        ("My heart is racing and I'm nervous.", "Anxious"), # Might map to Stressed in Mock
        ("I am so angry at him!", "Angry"), # Might map to Stressed in Mock
        ("This is so frustrating.", "Angry"), # Might map to Stressed in Mock
        ("I am bored out of my mind.", "Bored"), # Might map to Stressed in Mock
    ]
    
    print(f"Running inference on {len(test_data)} samples...")
    
    y_true = []
    y_pred = []
    
    for text, label in test_data:
        response = await agent.analyze(text)
        # Check if the predicted emotion is strictly one of the labels, 
        # or if we need to map complex emotions to the basic Mock set if running in mock mode.
        # But for "good results", let's assume valid output.
        pred = response.emotion
        
        y_true.append(label)
        y_pred.append(pred)
        # print(f"Text: {text} -> Pred: {pred} (True: {label})")

    # Metrics
    acc = accuracy_score(y_true, y_pred)
    report = classification_report(y_true, y_pred, zero_division=0)
    
    print(f"Accuracy: {acc:.2f}")
    print("Classification Report:\n", report)
    
    # Save Report
    with open("docs/evaluation_report.md", "w") as f:
        f.write("# Model Evaluation Report\n\n")
        f.write(f"**Overall Accuracy**: {acc:.2%}\n\n")
        f.write("## Classification Details\n")
        f.write("```text\n")
        f.write(report)
        f.write("\n```\n")
        f.write("\n## Confusion Matrix\n")
        f.write("![Confusion Matrix](confusion_matrix.png)\n")

    # Confusion Matrix
    unique_labels = sorted(list(set(y_true) | set(y_pred)))
    cm = confusion_matrix(y_true, y_pred, labels=unique_labels)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=unique_labels, yticklabels=unique_labels)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Emotion Classification Confusion Matrix')
    plt.tight_layout()
    plt.savefig("docs/confusion_matrix.png")
    print("Saved docs/confusion_matrix.png")
    print("Saved docs/evaluation_report.md")

if __name__ == "__main__":
    asyncio.run(evaluate())

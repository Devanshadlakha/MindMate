# utils/emotion_scoring.py

from transformers import pipeline
from datetime import datetime

sentiment_pipeline = pipeline("sentiment-analysis")
emotion_pipeline = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=None)

def compute_stress_score(text):
    score = 50

    sentiment = sentiment_pipeline(text)[0]
    if sentiment['label'] == 'POSITIVE':
        score += 20
    else:
        score -= 30 * sentiment['score']

    emotion_weights = {
        "anger": -15,
        "sadness": -20,
        "fear": -25,
        "joy": +10,
        "love": +5
    }
    emotions = emotion_pipeline(text)[0]
    top_emotion = emotions[0]['label']
    for emo in emotions:
        label = emo['label'].lower()
        if label in emotion_weights:
            score += emotion_weights[label] * emo['score']

    hour = datetime.now().hour
    if hour >= 22 or hour <= 5:
        score -= 5

    return max(1, min(100, int(score))), top_emotion.capitalize()

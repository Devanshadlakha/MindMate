# utils/chat_engine.py

import os
import requests
from dotenv import load_dotenv

from utils.translator import detect_lang, translate_to_english, translate_from_english
from utils.emotion_scoring import compute_stress_score

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {MISTRAL_API_KEY}",
    "Content-Type": "application/json"
}

# Static system prompt for the bot
system_prompt = (
    "You are MindMate, a compassionate mental health assistant designed to listen empathetically "
    "and provide support, resources, and suggestions to users experiencing emotional distress. "
    "Always respond in a kind and supportive tone."
)

# Context-based examples
def determine_context(user_input):
    if any(word in user_input.lower() for word in ["hi", "hello", "hey"]):
        return "greeting"
    elif any(word in user_input.lower() for word in ["kill", "hate", "die", "worthless", "suicide"]):
        return "offensive"
    else:
        return "general"

def call_mistral(user_message, context_msgs=None, context_type="general"):
    if context_msgs is None:
        context_msgs = []

    temperature = 0.5 if context_type == "greeting" else (0.3 if context_type == "offensive" else 0.8)

    messages = [{"role": "system", "content": system_prompt}] + context_msgs
    messages.append({"role": "user", "content": user_message})

    payload = {
        "model": "mistral-tiny",
        "temperature": temperature,
        "max_tokens": 400,
        "top_p": 0.9,
        "messages": messages
    }

    response = requests.post(MISTRAL_URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    reply = response.json()["choices"][0]["message"]["content"].strip()
    return reply

def get_response(user_input, emergency_contact=None):
    lang = detect_lang(user_input)
    input_en = translate_to_english(user_input) if lang != 'en' else user_input

    stress_score, emotion = compute_stress_score(input_en)
    context_type = determine_context(input_en)

    reply_en = call_mistral(input_en, context_msgs=[], context_type=context_type)
    translated_reply = translate_from_english(reply_en, lang) if lang != 'en' else reply_en

    suggestion = ""
    if stress_score < 10:
        suggestion = f"🚨 Please seek immediate help or contact your emergency contact ({emergency_contact})."
    elif stress_score < 30:
        suggestion = "💡 Consider talking to a friend or doing a relaxing activity."

    return translated_reply, stress_score, emotion, suggestion

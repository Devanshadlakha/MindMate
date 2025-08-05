# utils/translator.py

from googletrans import Translator

translator = Translator()

def detect_lang(text):
    try:
        return translator.detect(text).lang
    except:
        return 'en'

def translate_to_english(text):
    return translator.translate(text, src='auto', dest='en').text

def translate_from_english(text, target_lang):
    return translator.translate(text, src='en', dest=target_lang).text

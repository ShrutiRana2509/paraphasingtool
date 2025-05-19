from flask import Flask, render_template, request
import requests
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

DetectorFactory.seed = 0  

LANGUAGE_MAP = {
    "en": "English",
    "hi": "Hindi",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "mr": "Marathi",
    "ta": "Tamil",
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "ar": "Arabic",
    "ru": "Russian",
    "pt": "Portuguese",
    "it": "Italian",
    "bn": "Bengali",
    "ur": "Urdu",
    "gu": "Gujarati",
    "kn": "Kannada",
    "ml": "Malayalam",
    "te": "Telugu",
    "pa": "Punjabi",
    "pl": "Polish",
    "nl": "Dutch",
    "sv": "Swedish",
    "no": "Norwegian",
    "fi": "Finnish",
    "tr": "Turkish",
    "he": "Hebrew",
    "vi": "Vietnamese",
    "th": "Thai",
    "id": "Indonesian",
    "ro": "Romanian",
    "cs": "Czech",
    "el": "Greek",
    "hu": "Hungarian",
    "da": "Danish",
    "fa": "Persian",
    "sr": "Serbian",
    "uk": "Ukrainian",
    "bg": "Bulgarian",
    "sl": "Slovenian",
    "lt": "Lithuanian",
    "lv": "Latvian",
    "et": "Estonian",
    "is": "Icelandic",
    "ms": "Malay",
    "sw": "Swahili",
    "af": "Afrikaans",
    "ta": "Tamil",
}

app = Flask(__name__)
GROQ_API_KEY = "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"

def detect_language(text):
    try:
        lang_code = detect(text)
        return LANGUAGE_MAP.get(lang_code, "English")  
    except LangDetectException:
        return "English"

def paraphrase_with_groq(text):
    language = detect_language(text)

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"Paraphrase the following sentence in {language} without changing its meaning:\n\"{text}\""

    payload = {
        "model": "Gemma2-9b-It",
        "messages": [
            {"role": "system", "content": "You are a multilingual paraphrasing assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 200
    }

    response = requests.post(url, headers=headers, json=payload)
    try:
        result = response.json()
        if "choices" in result:
            return result['choices'][0]['message']['content'].strip()
        elif "error" in result:
            return f"API Error: {result['error']['message']}"
        else:
            return "Error: Unexpected response format."
    except Exception as e:
        print("Exception:", e)
        print("Response Text:", response.text)
        return "Error: Unable to paraphrase text."

@app.route("/", methods=["GET", "POST"])
def index():
    paraphrased_text = ""
    original_text = ""
    if request.method == "POST":
        original_text = request.form["original_text"]
        paraphrased_text = paraphrase_with_groq(original_text)

    return render_template("index.html", original_text=original_text, paraphrased_text=paraphrased_text)

if __name__ == '__main__':
    app.run(debug=True)
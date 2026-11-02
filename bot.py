import os
import requests
import time

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/"

def ask_ai(q):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        data = {"contents": [{"parts": [{"text": q}]}]}
        r = requests.post(url, json=data, timeout=30).json()
        return r['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"Error: {e}"

def send_message(chat_id, text):
    url = BASE_URL + "sendMessage"
    for i in range(0, len(text), 4000):
        requests.post(url, data={"chat_id": chat_id, "text": text[i:i+4000]})

offset = 0
print("Night King AI Ready!")
while True:
    try:
        resp = requests.get(BASE_URL + "getUpdates", params={"offset": offset, "timeout": 20}).json()
        for u in resp.get("result", []):
            offset = u["update_id"] + 1
            

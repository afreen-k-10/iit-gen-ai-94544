import time
import requests
import json
from dotenv import load_dotenv
import os
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

PROMPT = "Explain artificial intelligence in simple terms."

def call_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 150
    }

    start = time.time()
    response = requests.post(url, headers=headers, json=payload)
    elapsed = time.time() - start

    data = response.json()
    text = data["choices"][0]["message"]["content"]

    return text, elapsed

def call_gemini(prompt):
    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        "models/gemini-2.5-flash:generateContent"
    )

    headers = {
        "x-goog-api-key": GEMINI_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    start = time.time()
    response = requests.post(url, headers=headers, json=payload)
    elapsed = time.time() - start

    data = response.json()
    text = data["candidates"][0]["content"]["parts"][0]["text"]

    return text, elapsed

if __name__ == "__main__":
    print("\nPrompt:")
    print(PROMPT)

    print("\n--- Calling Groq ---")
    groq_text, groq_time = call_groq(PROMPT)
    print(f"Groq Time: {groq_time:.2f} seconds")
    print("Groq Output:")
    print(groq_text)

    print("\n--- Calling Gemini ---")
    gemini_text, gemini_time = call_gemini(PROMPT)
    print(f"Gemini Time: {gemini_time:.2f} seconds")
    print("Gemini Output:")
    print(gemini_text)

    print("\n--- Speed Comparison ---")
    if groq_time < gemini_time:
        print(f"Groq is faster by {gemini_time - groq_time:.2f} seconds")
    else:
        print(f"Gemini is faster by {groq_time - gemini_time:.2f} seconds")
import json
import os
from google import genai

try:
    with open('../aria_settings.json', 'r') as f:
        settings = json.load(f)
    api_key = settings.get('GEMINI_API_KEY')
    
    client = genai.Client(api_key=api_key)
    print("Available Models for generateContent:")
    for model in client.models.list():
        if "generateContent" in model.supported_actions:
            print("-", model.name)
except Exception as e:
    print("Error:", e)

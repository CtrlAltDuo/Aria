from google import genai
from google.genai import types
from .prompts import SYSTEM_PROMPT
import json
import base64

class GeminiClient:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def ask(self, screenshot_base64: str, instruction: str, history: list) -> dict:
        prompt = f"Instruction: {instruction}\n"
        if history:
            prompt += "Recent Actions:\n"
            for act in history:
                prompt += f"- {json.dumps(act)}\n"
        prompt += "\nWhat is the next action?"

        part = types.Part.from_bytes(
            data=base64.b64decode(screenshot_base64),
            mime_type='image/png',
        )

        response = self.client.models.generate_content(
            model='gemini-1.5-flash',
            contents=[part, prompt],
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
            )
        )
        
        text = response.text
        # Strip potential markdown formatting
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
            
        return json.loads(text.strip())

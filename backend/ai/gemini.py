import google.generativeai as genai
from .prompts import SYSTEM_PROMPT
import json
import base64
from io import BytesIO
from PIL import Image

class GeminiClient:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            system_instruction=SYSTEM_PROMPT
        )

    def ask(self, screenshot_base64: str, instruction: str, history: list) -> dict:
        image_data = base64.b64decode(screenshot_base64)
        image = Image.open(BytesIO(image_data))
        
        prompt = f"Instruction: {instruction}\n"
        if history:
            prompt += "Recent Actions:\n"
            for act in history:
                prompt += f"- {json.dumps(act)}\n"
        prompt += "\nWhat is the next action?"

        response = self.model.generate_content([image, prompt])
        
        text = response.text
        # Strip potential markdown formatting if model didn't listen perfectly
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
            
        return json.loads(text.strip())

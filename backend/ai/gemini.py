from google import genai
from google.genai import types
from .prompts import SYSTEM_PROMPT
import json
import base64

class GeminiClient:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def ask(self, screenshot_base64: str, instruction: str, history: list, active_window: str = None, ui_tree: list = None) -> dict:
        prompt = f"Instruction: {instruction}\n"
        if active_window:
            prompt += f"Active Window: {active_window}\n"
        if ui_tree:
            prompt += f"UI Elements Available (Extracted Accessibility Tree):\n{json.dumps(ui_tree)}\n"
        if history:
            prompt += "Recent Actions:\n"
            for act in history:
                prompt += f"- {json.dumps(act)}\n"
        prompt += "\nWhat is the next action?"

        part = types.Part.from_bytes(
            data=base64.b64decode(screenshot_base64),
            mime_type='image/png',
        )

        import time
        import re
        retries = 3
        response = None
        
        models = [
            'gemini-2.5-flash',
            'gemini-flash-latest',
            'gemini-3.5-flash',
            'gemini-2.0-flash',
            'gemini-2.5-pro'
        ]
        
        last_error = ""
        for model in models:
            success = False
            for attempt in range(retries):
                try:
                    response = self.client.models.generate_content(
                        model=model,
                        contents=[part, prompt],
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_PROMPT,
                        )
                    )
                    success = True
                    break
                except Exception as e:
                    error_msg = str(e)
                    last_error = error_msg
                    
                    if "404" in error_msg:
                        # Model not found, break to try next model immediately
                        break
                    
                    if "429" in error_msg:
                        # We hit a rate limit (either per-minute or per-day). 
                        # Since it could be the daily 20-request limit, we just switch to the next model to keep the app fast.
                        break
                        
                    if attempt < retries - 1 and "503" in error_msg:
                        time.sleep((2 ** attempt))
                        continue
                        
            if success:
                break
                
        if not response:
            raise Exception(f"Failed to get a response. All fallback models exhausted. Last error: {last_error}")
        
        text = response.text
        # Strip potential markdown formatting
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
            
        return json.loads(text.strip())

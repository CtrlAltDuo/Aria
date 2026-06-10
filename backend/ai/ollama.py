import json
from ollama import Client
from .prompts import SYSTEM_PROMPT

class OllamaClient:
    def __init__(self, url: str = "http://localhost:11434"):
        self.client = Client(host=url)
        # Using minicpm-v as an example local vision model, though qwen2-vl or llava are also options.
        self.model = "qwen2-vl" 

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
        prompt += "\nWhat is the next action? Respond ONLY with a JSON object as requested by system instructions."

        response = self.client.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": prompt,
                    "images": [screenshot_base64]
                }
            ]
        )
        
        text = response['message']['content']
        # Strip potential markdown formatting
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
            
        return json.loads(text.strip())

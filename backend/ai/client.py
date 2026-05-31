import os
import json
from .gemini import GeminiClient
from .ollama import OllamaClient

def get_settings():
    settings_path = "aria_settings.json"
    if os.path.exists(settings_path):
        try:
            with open(settings_path, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

class AIClient:
    def __init__(self):
        self.gemini = None
        self.ollama = None
        
    def _initialize_clients(self):
        # Re-initialize on each call to grab latest settings
        settings = get_settings()
        gemini_key = settings.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
        ollama_url = settings.get("OLLAMA_URL") or os.getenv("OLLAMA_URL", "http://localhost:11434")
        
        if gemini_key:
            self.gemini = GeminiClient(api_key=gemini_key)
        else:
            self.gemini = None
            
        self.ollama = OllamaClient(url=ollama_url)

    def ask(self, screenshot_base64: str, instruction: str, history: list, active_window: str = None) -> dict:
        self._initialize_clients()
        
        settings = get_settings()
        provider = settings.get("AI_PROVIDER") or os.getenv("AI_PROVIDER", "auto")
        
        if provider == "gemini" and self.gemini:
            return self.gemini.ask(screenshot_base64, instruction, history, active_window)
        elif provider == "ollama":
            return self.ollama.ask(screenshot_base64, instruction, history, active_window)
        else: # auto
            if self.gemini:
                return self.gemini.ask(screenshot_base64, instruction, history, active_window)
            else:
                return self.ollama.ask(screenshot_base64, instruction, history, active_window)

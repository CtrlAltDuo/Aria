import pyautogui
import time
import pyperclip
import subprocess

# Add a tiny fail-safe delay for PyAutoGUI
pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True

def execute(action_json: dict) -> bool:
    try:
        action = action_json.get("action")
        
        if action == "click":
            x = action_json.get("x")
            y = action_json.get("y")
            if x is not None and y is not None:
                pyautogui.click(x=x, y=y)
            else:
                pyautogui.click()
                
        elif action == "type":
            text = action_json.get("text")
            if text:
                pyautogui.write(text, interval=0.05)
                
        elif action == "scroll":
            direction = action_json.get("direction", "down")
            amount = -500 if direction == "down" else 500
            pyautogui.scroll(amount)
            
        elif action == "hotkey":
            keys = action_json.get("keys", [])
            if keys:
                pyautogui.hotkey(*keys)
                
        elif action == "wait":
            time.sleep(2)
            
        elif action == "copy":
            text = action_json.get("text")
            if text:
                pyperclip.copy(text)

        elif action == "paste":
            text = action_json.get("text")
            if text:
                pyperclip.copy(text)
                time.sleep(0.1)
                import platform
                if platform.system() == "Darwin":
                    pyautogui.hotkey('command', 'v')
                else:
                    pyautogui.hotkey('ctrl', 'v')

        elif action == "run_command":
            cmd = action_json.get("command")
            if cmd:
                # Run the command in the background, we don't wait for output here
                # to prevent blocking the agent loop if it's a long running app (like 'gedit' or 'notepad')
                subprocess.Popen(cmd, shell=True)
                
        elif action in ["done", "fail"]:
            pass # Handled by the loop
            
        else:
            print(f"Unknown action: {action}")
            return False

        time.sleep(1) # Small delay after each action
        return True
    except Exception as e:
        print(f"Error executing action: {e}")
        return False

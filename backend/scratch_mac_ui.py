import subprocess
import json

def get_mac_ui():
    script = """
    tell application "System Events"
        set frontApp to first application process whose frontmost is true
        set uiElements to {}
        try
            set frontWindow to front window of frontApp
            repeat with uiElem in (every UI element of frontWindow)
                set end of uiElements to {name:(name of uiElem as string), role:(role of uiElem as string)}
            end repeat
        end try
        return uiElements
    end tell
    """
    try:
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        print("Stdout:", result.stdout)
        print("Stderr:", result.stderr)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    get_mac_ui()

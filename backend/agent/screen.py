import mss
import mss.tools
from PIL import Image
import base64
from io import BytesIO

def take_screenshot() -> str:
    with mss.mss() as sct:
        # Get the first monitor
        monitor = sct.monitors[1]
        
        # Grab the screenshot
        sct_img = sct.grab(monitor)
        
        # Convert to PIL Image
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        
        # Save to BytesIO buffer as PNG
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        
        # Encode to base64 string
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        return img_str

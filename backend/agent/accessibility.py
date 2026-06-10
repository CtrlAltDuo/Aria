import platform
import re

# Simple regex for finding sensitive info (like SSN, credit cards, or basic email)
SENSITIVE_REGEX = re.compile(
    r'(\b\d{3}-\d{2}-\d{4}\b)|' # SSN
    r'(\b(?:\d[ -]*?){13,16}\b)|' # Credit Card
    r'(\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b)', # Email
    re.IGNORECASE
)

def filter_sensitive_data(node_name: str, is_password: bool = False) -> str:
    """Redacts sensitive information to preserve privacy."""
    if is_password:
        return "[REDACTED PASSWORD]"
    
    if not node_name:
        return ""
        
    if SENSITIVE_REGEX.search(node_name):
        return "[REDACTED SENSITIVE DATA]"
        
    return node_name

def get_accessibility_tree() -> list:
    """
    Extracts a lightweight, privacy-scrubbed JSON tree of actionable 
    UI elements from the OS. Falls back to empty list on unsupported platforms.
    """
    sys_plat = platform.system()
    ui_elements = []

    if sys_plat == "Windows":
        try:
            import uiautomation as auto
            root = auto.GetRootControl()
            # Walk the tree (we limit depth to avoid freezing)
            for control, depth in auto.WalkTree(root, getChildren=lambda c: c.GetChildren(), maxDepth=4):
                try:
                    c_type = control.ControlTypeName
                    if c_type in ["ButtonControl", "EditControl", "HyperlinkControl", "MenuItemControl"]:
                        rect = control.BoundingRectangle
                        # Privacy Filter
                        is_pwd = getattr(control, "IsPassword", False)
                        safe_name = filter_sensitive_data(control.Name, is_pwd)
                        
                        if safe_name:
                            ui_elements.append({
                                "type": c_type.replace("Control", ""),
                                "name": safe_name,
                                "center_x": (rect.left + rect.right) // 2,
                                "center_y": (rect.top + rect.bottom) // 2
                            })
                except Exception:
                    continue
        except ImportError:
            print("uiautomation not installed.")
            
    elif sys_plat == "Linux":
        try:
            import pyatspi
            desktop = pyatspi.Registry.getDesktop(0)
            
            # Simple recursive walk (limited depth to prevent lag)
            def walk_atspi(node, depth=0):
                if depth > 4 or not node: return
                try:
                    role = node.getRoleName()
                    if role in ["button", "text", "link", "menu item"]:
                        # Extract coordinates (screen coordinates)
                        try:
                            extents = node.queryComponent().getExtents(pyatspi.DESKTOP_COORDS)
                            center_x = extents.x + (extents.width // 2)
                            center_y = extents.y + (extents.height // 2)
                            
                            # Privacy filter
                            name = node.name or ""
                            is_pwd = "password" in role or "password" in name.lower()
                            safe_name = filter_sensitive_data(name, is_pwd)
                            
                            if safe_name:
                                ui_elements.append({
                                    "type": role.capitalize(),
                                    "name": safe_name,
                                    "center_x": center_x,
                                    "center_y": center_y
                                })
                        except Exception:
                            pass
                    for child in node:
                        walk_atspi(child, depth + 1)
                except Exception:
                    pass
            
            walk_atspi(desktop)
        except ImportError:
            print("pyatspi not installed. (Usually installable via 'sudo apt-get install python3-pyatspi')")

    return ui_elements

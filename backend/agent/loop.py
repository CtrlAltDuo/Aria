import os
from .screen import take_screenshot
from .actions import execute
from .accessibility import get_accessibility_tree
from ..ai.client import AIClient
from ..db.database import SessionLocal
from ..db.models import Task, ActionLog
import asyncio
import datetime
import pygetwindow as gw
from pynput import keyboard

def get_active_window_title():
    try:
        window = gw.getActiveWindow()
        if window:
            return window.title
    except Exception:
        pass
    return None

async def run_task(task_id: str, instruction: str, broadcast_fn):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        db.close()
        return

    task.status = "running"
    db.commit()

    # Setup Safety Kill Switch
    def on_activate():
        nonlocal task
        task.status = "cancelled"
        try:
            db.commit()
            print("KILL SWITCH ACTIVATED. Task cancelled.")
        except Exception:
            pass

    listener = None
    try:
        hotkey = keyboard.GlobalHotKeys({'<ctrl>+<shift>+x': on_activate})
        hotkey.start()
        listener = hotkey
    except Exception as e:
        print(f"Warning: Could not start kill-switch listener (needs accessibility permissions): {e}")

    ai = AIClient()
    history = []
    
    max_steps = int(os.getenv("MAX_STEPS", "40"))
    steps = 0
    
    try:
        while steps < max_steps:
            # 1. Check if task was cancelled externally
            db.refresh(task)
            if task.status != "running":
                break

            # 2. Get active window context
            active_window = await asyncio.to_thread(get_active_window_title)
            
            # Extract Accessibility Tree
            ui_tree = await asyncio.to_thread(get_accessibility_tree)

            # 3. Take screenshot
            screenshot = await asyncio.to_thread(take_screenshot)

            # 4. Send to AI
            try:
                action_json = await asyncio.to_thread(ai.ask, screenshot, instruction, history[-10:], active_window, ui_tree)
            except Exception as e:
                action_json = {
                    "action": "fail",
                    "reasoning": f"AI error: {str(e)}",
                    "confidence": 0.0
                }

            # 4. Log action to DB
            log = ActionLog(
                task_id=task_id,
                action_type=action_json.get("action", "unknown"),
                x=action_json.get("x"),
                y=action_json.get("y"),
                text=action_json.get("text"),
                reasoning=action_json.get("reasoning"),
                confidence=action_json.get("confidence")
            )
            db.add(log)
            db.commit()
            db.refresh(log)

            # 5. Call broadcast_fn
            log_dict = {
                "id": log.id,
                "action_type": log.action_type,
                "reasoning": log.reasoning,
                "confidence": log.confidence,
                "timestamp": log.timestamp.isoformat()
            }
            await broadcast_fn(log_dict)

            # 6. Execute action
            success = await asyncio.to_thread(execute, action_json)
            if not success and action_json.get("action") not in ["done", "fail"]:
                # Force fail on execute error
                action_json["action"] = "fail"
                action_json["reasoning"] = "Failed to execute OS action."

            # 7. Add to history
            history.append(action_json)

            # 8. Check done/fail
            action = action_json.get("action")
            if action == "done":
                task.status = "complete"
                task.completed_at = datetime.datetime.utcnow()
                task.result_summary = action_json.get("reasoning", "Completed successfully.")
                db.commit()
                break
            elif action == "fail":
                task.status = "failed"
                task.completed_at = datetime.datetime.utcnow()
                task.result_summary = action_json.get("reasoning", "Failed to complete task.")
                db.commit()
                break

            steps += 1

        if steps >= max_steps and task.status == "running":
            task.status = "failed"
            task.completed_at = datetime.datetime.utcnow()
            task.result_summary = "Exceeded maximum steps."
            db.commit()

    except Exception as e:
        task.status = "failed"
        task.result_summary = f"System error: {str(e)}"
        task.completed_at = datetime.datetime.utcnow()
        db.commit()
    finally:
        if listener:
            listener.stop()
        db.close()

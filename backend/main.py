from fastapi import FastAPI, Depends, BackgroundTasks, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import json
import os
import asyncio

from db.database import engine, Base, get_db
from tasks import manager
from agent.loop import run_task
from utils.logger import logger
from utils.config import load_config

# Load config and create tables
load_config()
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Aria Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TaskRequest(BaseModel):
    instruction: str

class SettingsRequest(BaseModel):
    key: str
    value: str

# In-memory store for active websocket connections per task
active_websockets = {}

@app.on_event("startup")
async def startup_event():
    logger.info("Aria backend ready")

@app.post("/tasks")
def create_task(req: TaskRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    task = manager.create_task(db, req.instruction)
    
    async def broadcast_fn(data: dict):
        if task.id in active_websockets:
            disconnected = []
            for ws in active_websockets[task.id]:
                try:
                    await ws.send_json(data)
                except Exception:
                    disconnected.append(ws)
            for ws in disconnected:
                active_websockets[task.id].remove(ws)
                
    background_tasks.add_task(run_task, task.id, req.instruction, broadcast_fn)
    return {"id": task.id, "instruction": task.instruction, "status": task.status}

@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    tasks = manager.list_tasks(db)
    return [{"id": t.id, "instruction": t.instruction, "status": t.status, "created_at": t.created_at} for t in tasks]

@app.get("/tasks/{task_id}")
def get_task(task_id: str, db: Session = Depends(get_db)):
    task, logs = manager.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    return {
        "id": task.id,
        "instruction": task.instruction,
        "status": task.status,
        "created_at": task.created_at,
        "completed_at": task.completed_at,
        "result_summary": task.result_summary,
        "logs": [
            {
                "id": log.id,
                "action_type": log.action_type,
                "text": log.text,
                "reasoning": log.reasoning,
                "confidence": log.confidence,
                "timestamp": log.timestamp
            } for log in logs
        ]
    }

@app.delete("/tasks/{task_id}")
def cancel_task(task_id: str, db: Session = Depends(get_db)):
    success = manager.cancel_task(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "cancelled"}

@app.get("/settings")
def get_settings():
    settings_path = "aria_settings.json"
    if os.path.exists(settings_path):
        with open(settings_path, "r") as f:
            return json.load(f)
    return {}

@app.put("/settings")
def update_settings(req: SettingsRequest):
    settings_path = "aria_settings.json"
    settings = {}
    if os.path.exists(settings_path):
        with open(settings_path, "r") as f:
            settings = json.load(f)
    
    settings[req.key] = req.value
    with open(settings_path, "w") as f:
        json.dump(settings, f)
    
    return {"status": "success"}

@app.websocket("/ws/{task_id}")
async def websocket_endpoint(websocket: WebSocket, task_id: str):
    await websocket.accept()
    if task_id not in active_websockets:
        active_websockets[task_id] = []
    active_websockets[task_id].append(websocket)
    try:
        while True:
            # Keep connection open, client doesn't send messages
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_websockets[task_id].remove(websocket)

from sqlalchemy.orm import Session
from ..db.models import Task, ActionLog

def create_task(db: Session, instruction: str) -> Task:
    task = Task(instruction=instruction, status="pending")
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def list_tasks(db: Session):
    return db.query(Task).order_by(Task.created_at.desc()).all()

def get_task(db: Session, task_id: str):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        logs = db.query(ActionLog).filter(ActionLog.task_id == task_id).order_by(ActionLog.timestamp.asc()).all()
        return task, logs
    return None, None

def cancel_task(db: Session, task_id: str):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.status = "cancelled"
        db.commit()
        db.refresh(task)
        return True
    return False

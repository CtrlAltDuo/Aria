from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import uuid
import datetime
from .database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    instruction = Column(String, nullable=False)
    status = Column(String, default="pending") # pending, running, complete, failed, cancelled
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    result_summary = Column(String, nullable=True)

    action_logs = relationship("ActionLog", back_populates="task", cascade="all, delete-orphan")

class ActionLog(Base):
    __tablename__ = "action_logs"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    task_id = Column(String, ForeignKey("tasks.id"), nullable=False)
    action_type = Column(String, nullable=False)
    x = Column(Integer, nullable=True)
    y = Column(Integer, nullable=True)
    text = Column(String, nullable=True)
    reasoning = Column(String, nullable=True)
    confidence = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    task = relationship("Task", back_populates="action_logs")

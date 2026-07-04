from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from app.core.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    goal = Column(Text, nullable=False)
    status = Column(String(20), default="queued")
    created_at = Column(DateTime, default=datetime.utcnow)
    step_logs = Column(JSON, nullable=True)
    output = Column(JSON, nullable=True)

from sqlalchemy.orm import Session
from app.models.task import Task


def create_task(db: Session, goal: str) -> Task:
    task = Task(goal=goal, status="queued")
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_task(db: Session, task_id: int) -> Task | None:
    return db.query(Task).filter(Task.id == task_id).first()


def list_tasks(db: Session) -> list[Task]:
    return db.query(Task).order_by(Task.created_at.desc()).all()


def update_task(db: Session, task_id: int, **kwargs) -> Task | None:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return None
    for key, value in kwargs.items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

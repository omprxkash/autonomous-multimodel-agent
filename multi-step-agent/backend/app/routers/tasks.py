import asyncio
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db, SessionLocal
from app.services.task_service import create_task, get_task, list_tasks, update_task
from app.agent.graph import graph

router = APIRouter(prefix="/tasks", tags=["tasks"])


class TaskCreate(BaseModel):
    goal: str


async def _run_pipeline(task_id: int, goal: str):
    db = SessionLocal()
    try:
        initial_state = {
            "goal": goal,
            "search_queries": [],
            "search_results": [],
            "filtered_results": [],
            "summaries": [],
            "outline": "",
            "draft": "",
            "step_logs": [],
            "current_step": "planner",
            "status": "running",
            "error": None,
        }
        update_task(db, task_id, status="running")
        result = await graph.ainvoke(initial_state)
        update_task(
            db,
            task_id,
            status="complete",
            step_logs=result.get("step_logs", []),
            output={
                "draft": result.get("draft", ""),
                "outline": result.get("outline", ""),
                "summaries": result.get("summaries", []),
            },
        )
    except Exception as exc:
        update_task(db, task_id, status="failed", step_logs=[], output={"error": str(exc)})
    finally:
        db.close()


@router.post("")
async def create_new_task(body: TaskCreate, db: Session = Depends(get_db)):
    task = create_task(db, body.goal)
    asyncio.create_task(_run_pipeline(task.id, body.goal))
    return {"id": task.id, "status": task.status}


@router.get("")
def list_all_tasks(db: Session = Depends(get_db)):
    tasks = list_tasks(db)
    return [
        {
            "id": t.id,
            "goal": t.goal,
            "status": t.status,
            "created_at": t.created_at.isoformat() if t.created_at else None,
            "step_logs": t.step_logs,
            "output": t.output,
        }
        for t in tasks
    ]


@router.get("/{task_id}")
def get_one_task(task_id: int, db: Session = Depends(get_db)):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {
        "id": task.id,
        "goal": task.goal,
        "status": task.status,
        "created_at": task.created_at.isoformat() if task.created_at else None,
        "step_logs": task.step_logs,
        "output": task.output,
    }


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    from app.models.task import Task
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"detail": "deleted"}

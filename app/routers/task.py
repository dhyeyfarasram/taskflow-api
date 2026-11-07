from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.task import Task
from app.db.database import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

#create a new task
@router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task( **task.model_dump())

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

#get all tasks
@router.get("/", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks

#get a specific task by ID
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task

#update a specific task by ID
@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id ==task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    else:
        for key, value in task_update.model_dump(exclude_unset=True).items():
            setattr(task, key, value)
    
        db.commit()
        db.refresh(task)

    return task

@router.delete("/{task_id}", response_model=dict)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}
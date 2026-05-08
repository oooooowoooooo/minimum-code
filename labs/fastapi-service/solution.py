from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

app = FastAPI(title="Task Management API")

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"

class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    priority: str
    completed: bool
    created_at: str

tasks_db: dict = {}

def get_task_store():
    return tasks_db

@app.post("/tasks", status_code=201, response_model=TaskResponse)
def create_task(task: TaskCreate, store: dict = Depends(get_task_store)):
    task_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    task_data = {
        "id": task_id,
        "title": task.title,
        "description": task.description,
        "priority": task.priority,
        "completed": False,
        "created_at": now,
    }
    store[task_id] = task_data
    return task_data

@app.get("/tasks", response_model=List[TaskResponse])
def list_tasks(store: dict = Depends(get_task_store)):
    return list(store.values())

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: str, store: dict = Depends(get_task_store)):
    if task_id not in store:
        raise HTTPException(status_code=404, detail="Task not found")
    return store[task_id]

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: str, store: dict = Depends(get_task_store)):
    if task_id not in store:
        raise HTTPException(status_code=404, detail="Task not found")
    del store[task_id]

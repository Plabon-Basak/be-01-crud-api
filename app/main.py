
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app import service

app = FastAPI(title="Task API")


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = ""


class TaskUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = ""
    completed: bool = False


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    return service.create_task(task.title, task.description)


@app.get("/tasks")
def list_tasks():
    return service.list_tasks()


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = service.find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    updated = service.update_task(
        task_id,
        task.title,
        task.description,
        task.completed,
    )
    if updated is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    deleted = service.remove_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}
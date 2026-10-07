from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel


app = FastAPI(
    title="Task API",
    description="A simple in-memory CRUD API built with FastAPI.",
    version="1.0.0"
)


# -------------------------
# Error Handling
# -------------------------

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=400,
        content={"error": "Invalid request body"}
    )


# -------------------------
# Data Models
# -------------------------

class TaskCreate(BaseModel):
    title: str
    done: bool = False


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None


# -------------------------
# In-memory data
# -------------------------

tasks = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "done": False
    },
    {
        "id": 2,
        "title": "Build CRUD API",
        "done": False
    }
]


# -------------------------
# Root Route
# -------------------------

@app.get(
    "/",
    summary="API information",
    description="Returns basic information about the Task API."
)
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


# -------------------------
# Health Route
# -------------------------

@app.get(
    "/health",
    summary="Health check",
    description="Checks whether the API is running."
)
def health():
    return {"status": "ok"}


# -------------------------
# Get All Tasks
# -------------------------

@app.get(
    "/tasks",
    summary="List all tasks",
    description="Returns all tasks currently stored in memory."
)
def get_tasks():
    return tasks


# -------------------------
# Get One Task
# -------------------------

@app.get(
    "/tasks/{task_id}",
    summary="Get a task",
    description="Returns a single task by its ID."
)
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )


# -------------------------
# Create Task
# -------------------------

@app.post(
    "/tasks",
    status_code=201,
    summary="Create a task",
    description="Creates a new task. The title must not be empty."
)
def create_task(task: TaskCreate):

    if not task.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title cannot be empty"}
        )

    new_id = max([task["id"] for task in tasks], default=0) + 1

    new_task = {
        "id": new_id,
        "title": task.title,
        "done": task.done
    }

    tasks.append(new_task)

    return new_task


# -------------------------
# Update Task
# -------------------------

@app.put(
    "/tasks/{task_id}",
    summary="Update a task",
    description="Updates an existing task by its ID."
)
def update_task(task_id: int, task: TaskUpdate):

    existing_task = None

    for item in tasks:
        if item["id"] == task_id:
            existing_task = item
            break

    if existing_task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )

    if task.title is None and task.done is None:
        return JSONResponse(
            status_code=400,
            content={"error": "At least one field is required"}
        )

    if task.title is not None:

        if not task.title.strip():
            return JSONResponse(
                status_code=400,
                content={"error": "Title cannot be empty"}
            )

        existing_task["title"] = task.title

    if task.done is not None:
        existing_task["done"] = task.done

    return existing_task


# -------------------------
# Delete Task
# -------------------------

@app.delete(
    "/tasks/{task_id}",
    status_code=204,
    summary="Delete a task",
    description="Deletes an existing task by its ID."
)
def delete_task(task_id: int):

    for index, task in enumerate(tasks):

        if task["id"] == task_id:
            tasks.pop(index)

            return None

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )
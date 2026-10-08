from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field
from database import initialize_database

initialize_database()

app = FastAPI(
    title="Task API",
    description="A small in-memory CRUD API for managing tasks.",
    version="1.0.0",
)


# -------------------------
# Error handling
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
# Data models
# -------------------------

class TaskCreate(BaseModel):
    title: str = Field(..., description="Task title")
    done: bool = Field(False, description="Whether the task is completed")


class TaskUpdate(BaseModel):
    title: str | None = Field(None, description="Updated task title")
    done: bool | None = Field(None, description="Updated completion status")


# -------------------------
# In-memory task storage
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
# GET /
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
# GET /health
# -------------------------

@app.get(
    "/health",
    summary="Health check",
    description="Checks whether the API is running."
)
def health():
    return {
        "status": "ok"
    }


# -------------------------
# GET /tasks
# -------------------------

@app.get(
    "/tasks",
    summary="List all tasks",
    description="Returns all tasks currently stored in memory."
)
def get_tasks():
    return tasks


# -------------------------
# GET /tasks/{id}
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
        content={
            "error": f"Task {task_id} not found"
        }
    )


# -------------------------
# POST /tasks
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
            content={
                "error": "Title cannot be empty"
            }
        )

    new_id = max(
        [item["id"] for item in tasks],
        default=0
    ) + 1

    new_task = {
        "id": new_id,
        "title": task.title,
        "done": task.done
    }

    tasks.append(new_task)

    return new_task


# -------------------------
# PUT /tasks/{id}
# -------------------------

@app.put(
    "/tasks/{task_id}",
    summary="Update a task",
    description="Updates an existing task by its ID."
)
def update_task(
    task_id: int,
    task: TaskUpdate
):

    existing_task = None

    for item in tasks:
        if item["id"] == task_id:
            existing_task = item
            break

    if existing_task is None:
        return JSONResponse(
            status_code=404,
            content={
                "error": f"Task {task_id} not found"
            }
        )

    if task.title is None and task.done is None:
        return JSONResponse(
            status_code=400,
            content={
                "error": "At least one field is required"
            }
        )

    if task.title is not None:

        if not task.title.strip():
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Title cannot be empty"
                }
            )

        existing_task["title"] = task.title

    if task.done is not None:
        existing_task["done"] = task.done

    return existing_task


# -------------------------
# DELETE /tasks/{id}
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

            return Response(status_code=204)

    return JSONResponse(
        status_code=404,
        content={
            "error": f"Task {task_id} not found"
        }
    )
# Task API

A simple CRUD API built with Python and FastAPI for the FlyRank Backend AI Engineering BE-01 assignment.

## Features

* Create tasks
* Read all tasks
* Read a single task
* Update tasks
* Delete tasks
* Input validation
* Correct HTTP status codes
* Interactive Swagger UI
* In-memory task storage

## Tech Stack

* Python 3
* FastAPI
* Uvicorn
* Pydantic
* Swagger UI / OpenAPI
* Git and GitHub

## Installation

Clone the repository:

```bash
git clone https://github.com/Plabon-Basak/be-01-crud-api
cd BE-01-crud-api
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

Start the API:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Swagger UI:

```text
http://localhost:8000/docs
```

## Endpoints

| Method | Endpoint      | Description     | Success |
| ------ | ------------- | --------------- | ------- |
| GET    | `/`           | API information | 200     |
| GET    | `/health`     | Health check    | 200     |
| GET    | `/tasks`      | Get all tasks   | 200     |
| GET    | `/tasks/{id}` | Get one task    | 200     |
| POST   | `/tasks`      | Create a task   | 201     |
| PUT    | `/tasks/{id}` | Update a task   | 200     |
| DELETE | `/tasks/{id}` | Delete a task   | 204     |

## Error Handling

| Status | Meaning              |
| ------ | -------------------- |
| 400    | Invalid request data |
| 404    | Task not found       |

## Example Request

Create a task:

```bash
curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d "{\"title\":\"Buy milk\"}"
```

Example response:

```text
HTTP/1.1 201 Created
```

```json
{
  "id": 4,
  "title": "Buy milk",
  "done": false
}
```

## Swagger UI

The API documentation is available through FastAPI's built-in Swagger UI.

![Swagger UI](screenshots/swagger.png)

## Storage

This project intentionally uses an in-memory Python list instead of a database.

Therefore, tasks are lost when the server restarts. This is intentional because database persistence is covered in a later stage of the backend track.

## Assignment

FlyRank Backend AI Engineering — BE-01: Build your first CRUD API.

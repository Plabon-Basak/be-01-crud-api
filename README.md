## BE-04: Containerize Your Stack

### Overview

This project containerizes the FastAPI Task API and PostgreSQL database using Docker Compose.

### Tech Stack

* Python
* FastAPI
* PostgreSQL
* Psycopg
* Docker
* Docker Compose

### Architecture

The API uses a repository layer to access task data stored in PostgreSQL. The database connection is configured through environment variables in `.env`.

The PostgreSQL database runs in a Docker container and stores its data in a persistent named volume.

**Layering:** The existing A2 service and route layers were kept unchanged, and the storage implementation was replaced with a PostgreSQL repository.

*Keep the statement above only if your service and routes really remained unchanged.*

### Configuration

1. Copy `.env.example` to `.env`.
2. Set the local database credentials and connection string.
3. Do not commit `.env` to version control.

### Run the Application

Start the complete stack:

```bash
docker compose up --build
```

Open the interactive API documentation at `http://localhost:8000/docs`.

Stop the stack with:

```bash
docker compose down
```

### Persistence Verification

1. Created a task through the API.
2. Verified the record in PostgreSQL.
3. Stopped and removed the containers using `docker compose down`.
4. Rebuilt and restarted the stack using `docker compose up --build -d`.
5. Verified that the original record was still present through PostgreSQL and the API.

The database volume was retained throughout the test. The `docker compose down -v` command was not used.

*Update this section after completing the test and include screenshots as evidence.*

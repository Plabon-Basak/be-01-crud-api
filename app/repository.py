
import os

import psycopg
from psycopg.rows import dict_row


DATABASE_URL = os.environ["DATABASE_URL"]


def get_connection():
    return psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row,
    )


def get_all_tasks():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, title, description, completed
                FROM tasks
                ORDER BY id
                """
            )
            return cur.fetchall()


def get_task(task_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, title, description, completed
                FROM tasks
                WHERE id = %s
                """,
                (task_id,),
            )
            return cur.fetchone()


def create_task(title: str, description: str = ""):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO tasks (title, description)
                VALUES (%s, %s)
                RETURNING id, title, description, completed
                """,
                (title, description),
            )
            return cur.fetchone()


def update_task(
    task_id: int,
    title: str,
    description: str,
    completed: bool,
):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE tasks
                SET title = %s,
                    description = %s,
                    completed = %s
                WHERE id = %s
                RETURNING id, title, description, completed
                """,
                (title, description, completed, task_id),
            )
            return cur.fetchone()


def delete_task(task_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM tasks WHERE id = %s RETURNING id",
                (task_id,),
            )
            return cur.fetchone() is not None
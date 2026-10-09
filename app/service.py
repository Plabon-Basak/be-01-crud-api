
from app import repository


def list_tasks():
    return repository.get_all_tasks()


def find_task(task_id: int):
    return repository.get_task(task_id)


def create_task(title: str, description: str = ""):
    return repository.create_task(title, description)


def update_task(
    task_id: int,
    title: str,
    description: str,
    completed: bool,
):
    return repository.update_task(
        task_id, title, description, completed
    )


def remove_task(task_id: int):
    return repository.delete_task(task_id)
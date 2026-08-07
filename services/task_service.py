"""
Service layer responsible for task operations,
including ownership validation and admin permissions.
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

import models
from schemas import TaskCreate, TaskUpdate


def get_tasks_service(
    db: Session,
    user: models.User,
    page: int,
    limit: int,
    search: str | None,
    completed: bool | None,
    order: str,
) -> list[models.Task]:
    """
    Retrieves tasks available to the current user.

    Regular users can only access their own tasks.
    Administrators can access all tasks.
    """
    query = db.query(models.Task)

    # Regular users only see tasks they own.
    if user.role != "admin":
        query = query.filter(models.Task.owner_id == user.id)

    if search:
        query = query.filter(
            models.Task.title.ilike(f"%{search}%")
        )

    if completed is not None:
        query = query.filter(
            models.Task.completed == completed
        )

    if order == "desc":
        query = query.order_by(models.Task.id.desc())
    else:
        query = query.order_by(models.Task.id.asc())

    offset = (page - 1) * limit

    return query.offset(offset).limit(limit).all()


def create_task_service(
    db: Session,
    task_data: TaskCreate,
    user_id: int,
) -> models.Task:
    """
    Creates a new task and assigns it to its owner.
    """
    task = models.Task(
        **task_data.model_dump(),
        owner_id=user_id,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def delete_task_service(
    db: Session,
    task_id: int,
    user: models.User,
) -> models.Task:
    """
    Deletes a task after validating ownership permissions.
    """
    task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id)
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )

    if user.role != "admin" and task.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this task.",
        )

    db.delete(task)
    db.commit()

    return task


def update_task_service(
    db: Session,
    task_id: int,
    task_data: TaskUpdate,
    user: models.User,
) -> models.Task:
    """
    Updates a task after validating ownership permissions.
    """
    task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id)
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )

    if user.role != "admin" and task.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this task.",
        )

    for field, value in task_data.model_dump(
        exclude_unset=True
    ).items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task
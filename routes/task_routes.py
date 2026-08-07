from fastapi import APIRouter, Depends, Query, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

import models
from database import get_db
from dependencies.security import get_current_user
from schemas import TaskCreate, TaskResponseEnvelope, TaskUpdate
from services.task_service import (
    create_task_service,
    delete_task_service,
    get_tasks_service,
    update_task_service,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])




@router.get("/", response_model=TaskResponseEnvelope)
def get_tasks_route(
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    search: str = Query(None),
    completed: bool = Query(None),
    order: str = Query("desc", pattern="^(asc|desc)$"),
    # Depends(get_current_user) handles the authentication logic,
    # and Swagger recognizes that this route requires authorization.
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Retrieves tasks with pagination, search, and filtering support.
    """
    tasks = get_tasks_service(db, user, page, limit, search, completed, order)

    return {
        "success": True,
        "message": "Task list retrieved successfully",
        "data": tasks,
    }


@router.post(
    "/",
    response_model=TaskResponseEnvelope,
    status_code=status.HTTP_201_CREATED,
)
def create_task_route(
    task: TaskCreate,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Creates a new task linked to the authenticated user.
    """
    new_task = create_task_service(db, task, user.id)

    return {
        "success": True,
        "message": "Task created successfully",
        "data": new_task,
    }


@router.delete("/{task_id}", response_model=TaskResponseEnvelope)
def delete_task_route(
    task_id: int,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Removes an existing task.
    """
    delete_task_service(db, task_id, user)

    return {
        "success": True,
        "message": "Task deleted successfully",
        "data": None,
    }


@router.put("/{task_id}", response_model=TaskResponseEnvelope)
def update_task_route(
    task_id: int,
    task: TaskUpdate,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Updates a task partially or completely.
    """
    updated_task = update_task_service(db, task_id, task, user)

    return {
        "success": True,
        "message": "Task updated successfully",
        "data": updated_task,
    }
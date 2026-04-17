from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from database import get_db
from dependencies.security import get_current_user
from schemas import TaskCreate, TaskResponse, TaskResponseEnvelope
from services.task_service import (
    get_tasks_service,
    create_task_service,
    delete_task_service,
    update_task_service
)
from models import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/", response_model=TaskResponseEnvelope)
def get_tasks_route(
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    search: str = Query(None),
    done: bool = Query(None),
    order: str = Query("desc", pattern="^(asc|desc)$"),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Rota para listagem de tarefas com suporte a paginacao, busca e filtros.
    """
    tasks = get_tasks_service(db, user, page, limit, search, done, order)
    return {
        "success": True,
        "message": "Lista de tarefas recuperada com sucesso",
        "data": tasks
    }

@router.post("/", response_model=TaskResponseEnvelope, status_code=status.HTTP_201_CREATED)
def create_task_route(
    task: TaskCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Rota para criacao de uma nova tarefa vinculada ao usuario autenticado.
    """
    nova_task = create_task_service(db, task, user.id)
    return {
        "success": True,
        "message": "Tarefa criada com sucesso",
        "data": nova_task
    }

@router.delete("/{task_id}", response_model=TaskResponseEnvelope)
def delete_task_route(
    task_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Rota para remocao de uma tarefa existente.
    """
    resultado = delete_task_service(db, task_id, user)
    return {
        "success": True,
        "message": "Tarefa removida com sucesso",
        "data": None
    }

@router.put("/{task_id}", response_model=TaskResponseEnvelope)
def update_task_route(
    task_id: int,
    task: TaskCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Rota para atualizacao parcial ou total de uma tarefa.
    """
    task_atualizada = update_task_service(db, task_id, task, user)
    return {
        "success": True,
        "message": "Tarefa atualizada com sucesso",
        "data": task_atualizada
    }
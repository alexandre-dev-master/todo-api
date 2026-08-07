from fastapi import APIRouter, Depends, Query, status, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from dependencies.security import get_current_user
from schemas import TaskCreate, TaskResponseEnvelope, TaskUpdate
from services.task_service import (
    get_tasks_service,
    create_task_service,
    delete_task_service,
    update_task_service
)
import models

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# 1. Definimos o esquema de segurança explicitamente
# O FastAPI vai usar isso para criar o cadeado no Swagger automaticamente
security = HTTPBearer()

@router.get("/", response_model=TaskResponseEnvelope)
def get_tasks_route(
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    search: str = Query(None),
    completed: bool = Query(None),
    order: str = Query("desc", pattern="^(asc|desc)$"),
    # 2. O Depends(get_current_user) já cuida da lógica, 
    # mas o Swagger precisa saber que essa rota REQUER o security.
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Rota para listagem de tarefas com suporte a paginação, busca e filtros.
    """
    tasks = get_tasks_service(db, user, page, limit, search, completed, order)
    return {
        "success": True,
        "message": "Lista de tarefas recuperada com sucesso",
        "data": tasks
    }

@router.post("/", response_model=TaskResponseEnvelope, status_code=status.HTTP_201_CREATED)
def create_task_route(
    task: TaskCreate,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Rota para criação de uma nova tarefa vinculada ao usuário autenticado.
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
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Rota para remoção de uma tarefa existente.
    """
    delete_task_service(db, task_id, user)
    return {
        "success": True,
        "message": "Tarefa removida com sucesso",
        "data": None
    }

@router.put("/{task_id}", response_model=TaskResponseEnvelope)
def update_task_route(
    task_id: int,
    task: TaskUpdate,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Rota para atualização parcial ou total de uma tarefa.
    """
    task_atualizada = update_task_service(db, task_id, task, user)
    return {
        "success": True,
        "message": "Tarefa atualizada com sucesso",
        "data": task_atualizada
    }
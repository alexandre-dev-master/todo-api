from fastapi import APIRouter, Depends, Query
# router e dependências do FastAPI

from sqlalchemy.orm import Session
# sessão do banco

from database import get_db
# dependência do banco

from dependencies.security import get_current_user
# autenticação via JWT

from models import User
# model do usuário

from schemas import TaskCreate, TaskUpdate, TaskResponseEnvelope
# schemas usados nas rotas

from services.task_service import get_tasks_service, create_task_service, delete_task_service, update_task_service
# funções do service


router = APIRouter(prefix="/tasks")
# prefixo centraliza tudo em /tasks


# =========================
# GET - LISTAR TASKS
# =========================
@router.get("/", response_model=TaskResponseEnvelope)
def get_tasks_route(
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    search: str = Query(None),
    done: bool = Query(None),
    order: str = Query("desc", regex="^(asc|desc)$"),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    tasks = get_tasks_service(db, user, page, limit, search, done, order)
    return {
        "success": True,
        "message": "Lista de tarefas recuperada",
        "data": tasks
    }

# =========================
# POST - CRIAR TASK
# =========================
@router.post("/", response_model=TaskResponseEnvelope)
def create_task_route(task: TaskCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    nova_task = create_task_service(db, task, user.id)
    return {
        "success": True,
        "message": "Tarefa criada com sucesso",
        "data": nova_task
    }

# =========================
# DELETE - DELETAR TASK
# =========================
@router.delete("/{task_id}", response_model=TaskResponseEnvelope)
def delete_task_route(task_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    resultado = delete_task_service(db, task_id, user)
    return {
        "success": True,
        "message": resultado["message"],
        "data": None  # No delete, geralmente o data vai vazio ou nulo
    }

# =========================
# PUT - ATUALIZAR TASK
# =========================
@router.put("/{task_id}", response_model=TaskResponseEnvelope)
def update_task_route(task_id: int, task: TaskUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task_atualizada = update_task_service(db, task_id, task, user)
    return {
        "success": True,
        "message": "Tarefa atualizada com sucesso",
        "data": task_atualizada
    }
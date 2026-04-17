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

from services.task_service import get_tasks, create_task, delete_task, update_task
# funções do service


router = APIRouter(prefix="/tasks")
# prefixo centraliza tudo em /tasks


# =========================
# GET - LISTAR TASKS
# =========================
@router.get("/", response_model=TaskResponseEnvelope)
# GET /tasks

def get_tasks(user, db, page, limit, search, done, order):
    query = db.query(Task)
    # Inicia a preparação do comando SQL (SELECT * FROM tasks)

    if user.role != "admin":
        query = query.filter(Task.owner_id == user.id)
    # Se não for admin, adiciona um filtro para buscar apenas as tarefas do ID do usuário logado

    if search:
        query = query.filter(Task.title.contains(search))
    # Se houver busca, filtra títulos que contenham o texto enviado (operador LIKE)

    if done is not None:
        query = query.filter(Task.done == done)
    # Se o filtro 'done' foi enviado (True/False), filtra pelo status de conclusão

    if order == "asc":
        query = query.order_by(Task.id.asc())
    else:
        query = query.order_by(Task.id.desc())
    # Define a ordenação: 'asc' para as mais antigas primeiro, ou 'desc' para as novas

    offset = (page - 1) * limit
    # Calcula quantos registros pular com base na página atual (ex: página 2 pula a página 1)

    tasks = query.offset(offset).limit(limit).all()
    # Executa a query final no banco trazendo apenas a "fatia" de dados solicitada

    total = query.count()
    # Conta o total de registros que existem para esses filtros (sem considerar o limite da página)

    return {
        "success": True,
        "data": tasks,
        "metadata": {
            "total": total,
            "page": page,
            "limit": limit
        }
    }
    # Retorna o dicionário formatado que será convertido em JSON para o cliente


# =========================
# POST - CRIAR TASK
# =========================
@router.post("/", response_model=TaskResponseEnvelope)
# POST /tasks

def create_task_route(
    task: TaskCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_task(task, user, db)
    # cria task


# =========================
# DELETE - DELETAR TASK
# =========================
@router.delete("/{task_id}", response_model=TaskResponseEnvelope)
# DELETE /tasks/{id}

def delete_task_route(
    task_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return delete_task(task_id, user, db)
    # deleta task


# =========================
# PUT - ATUALIZAR TASK
# =========================
@router.put("/{task_id}", response_model=TaskResponseEnvelope)
# PUT /tasks/{id}

def update_task_route(
    task_id: int,
    task: TaskUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return update_task(task_id, task, user, db)
    # atualiza task
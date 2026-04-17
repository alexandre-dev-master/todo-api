from sqlalchemy.orm import Session
from models import Task, User
from schemas import TaskCreate, TaskUpdate
from fastapi import HTTPException, status

# =========================
# LISTAR TAREFAS (READ)
# =========================
def get_tasks_service(
    db: Session, 
    current_user: User, 
    page: int = 1, 
    limit: int = 10, 
    search: str = None, 
    done: bool = None, 
    order: str = "desc"
):
    query = db.query(Task)

    # 1. Filtro de Segurança
    if current_user.role != "admin":
        query = query.filter(Task.owner_id == current_user.id)
    
    # 2. Filtro de busca (Case-insensitive)
    if search:
        query = query.filter(Task.title.ilike(f"%{search}%"))
        
    # 3. Filtro de status
    if done is not None:
        query = query.filter(Task.done == done)

    # 4. Ordenação
    if order == "desc":
        query = query.order_by(Task.id.desc())
    else:
        query = query.order_by(Task.id.asc())

    # =========================
    # LÓGICA DE PAGINAÇÃO REAL
    # =========================
    offset = (page - 1) * limit
    return query.offset(offset).limit(limit).all()

# =========================
# CRIAR TAREFA (CREATE)
# =========================
def create_task_service(db: Session, task_data: TaskCreate, user_id: int):
    db_task = Task(
        title=task_data.title,
        # description removida para bater com seu models.py
        owner_id=user_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# =========================
# ATUALIZAR TAREFA (UPDATE)
# =========================
def update_task_service(db: Session, task_id: int, task_data: TaskUpdate, current_user):
    # 1. Busca a tarefa no banco
    db_query = db.query(Task).filter(Task.id == task_id)
    db_task = db_query.first()

    # 2. Se não existir, erro 404
    if not db_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")

    # 3. Segurança: Só o dono ou Admin pode editar
    if db_task.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado")

    # 4. Atualiza os campos (o .dict(exclude_unset=True) evita apagar o que não foi enviado)
    update_data = task_data.dict(exclude_unset=True)
    db_query.update(update_data)
    
    db.commit()
    db.refresh(db_task)
    return db_task

# =========================
# DELETAR TAREFA (DELETE)
# =========================
def delete_task_service(db: Session, task_id: int, current_user):
    db_task = db.query(Task).filter(Task.id == task_id).first()

    if not db_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")

    # Segurança: Só o dono ou Admin pode deletar
    if db_task.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado")

    db.delete(db_task)
    db.commit()
    return {"message": "Tarefa removida com sucesso"}
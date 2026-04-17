from sqlalchemy.orm import Session
from models import Task 
from schemas import TaskCreate, TaskUpdate
from fastapi import HTTPException, status

# =========================
# LISTAR TAREFAS (READ)
# =========================
def get_tasks(db: Session, current_user: dict):
    if current_user["role"] == "admin":
        return db.query(Task).all()
        # Admin visualiza todas as tarefas do sistema
    
    return db.query(Task).filter(Task.owner_id == current_user["id"]).all()
    # Usuário comum visualiza apenas as suas próprias tarefas

# =========================
# CRIAR TAREFA (CREATE)
# =========================
def create_task(db: Session, task_data: TaskCreate, user_id: int):
    db_task = Task(
        title=task_data.title,
        description=task_data.description,
        owner_id=user_id
    )
    # Instancia a tarefa vinculando o owner_id do usuário logado

    db.add(db_task)
    # Adiciona o novo objeto à sessão do banco de dados
    
    db.commit()
    # Confirma a transação e salva no disco
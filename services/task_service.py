from sqlalchemy.orm import Session
from models import Task, User
from schemas import TaskCreate
from fastapi import HTTPException, status

def get_tasks_service(db: Session, current_user: User, page: int, limit: int, search: str, done: bool, order: str):
    """
    Consulta o banco de dados para retornar tarefas com base nos filtros e permissões.
    """
    query = db.query(Task)
    
    # Filtro de propriedade (Admin ve tudo, usuario comum ve apenas o que e dele)
    if current_user.role != "admin":
        query = query.filter(Task.owner_id == current_user.id)

    if search:
        query = query.filter(Task.title.ilike(f"%{search}%"))
    
    if done is not None:
        query = query.filter(Task.done == done)

    if order == "desc":
        query = query.order_by(Task.id.desc())
    else:
        query = query.order_by(Task.id.asc())

    offset = (page - 1) * limit
    return query.offset(offset).limit(limit).all()

def create_task_service(db: Session, task_data: TaskCreate, user_id: int):
    """
    Instancia e persiste uma nova tarefa no banco de dados.
    """
    db_task = Task(title=task_data.title, owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task_service(db: Session, task_id: int, current_user: User):
    """
    Remove uma tarefa apos verificar a existencia e as permissoes de acesso.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    if current_user.role != "admin" and task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para excluir esta tarefa")
    
    db.delete(task)
    db.commit()
    return {"message": "Tarefa removida"}

def update_task_service(db: Session, task_id: int, task_data: TaskCreate, current_user: User):
    """
    Atualiza os dados de uma tarefa respeitando as regras de negocio e permissões.
    """
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    if current_user.role != "admin" and db_task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar esta tarefa")

    for key, value in task_data.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task
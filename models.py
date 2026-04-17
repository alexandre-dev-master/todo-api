from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    """
    Modelo representativo da tabela de usuarios do sistema.
    Armazena credenciais, perfil de acesso e relacoes com tarefas.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="user") # 'admin' ou 'user'

    # Relacao um-para-muitos com a tabela de tarefas
    tasks = relationship("Task", back_populates="owner")

class Task(Base):
    """
    Modelo representativo da tabela de tarefas (tasks).
    Cada tarefa e obrigatoriamente vinculada a um usuario (owner).
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    done = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Referencia ao objeto do usuario dono da tarefa
    owner = relationship("User", back_populates="tasks")
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


# =========================
# TASK
# =========================
class Task(Base):
    __tablename__ = "tasks"  # nome da tabela no banco

    id = Column(Integer, primary_key=True, index=True)
    # id único da task

    title = Column(String)
    # título da tarefa

    done = Column(Boolean, default=False)
    # se a tarefa foi concluída ou não

    owner_id = Column(Integer, ForeignKey("users.id"))
    # chave estrangeira → liga a task ao usuário
    # "users.id" = tabela users, coluna id

    owner = relationship("User", back_populates="tasks")
    # cria relação com User
    # permite acessar: task.owner


# =========================
# USER
# =========================
class User(Base):
    __tablename__ = "users"  # nome da tabela no banco

    id = Column(Integer, primary_key=True)
    # id único do usuário

    username = Column(String, unique=True, index=True)
    # nome do usuário (não pode repetir)

    password = Column(String)
    # senha criptografada

    role = Column(String, default="user")
    # 'user' ou 'admin'

    tasks = relationship("Task", back_populates="owner")
    # relação inversa
    # permite acessar: user.tasks (lista de tarefas do usuário)


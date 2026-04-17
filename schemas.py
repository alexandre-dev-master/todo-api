from pydantic import BaseModel, Field
from typing import Optional, List

# =========================
# SCHEMA: BASE DE TAREFAS
# =========================
class TaskBase(BaseModel):
    # Contém os campos comuns a todas as versões de uma tarefa
    title: str = Field(..., min_length=3, max_length=100, description="Título da tarefa")
    description: Optional[str] = Field(None, max_length=500, description="Detalhes extras")

# =========================
# SCHEMA: CRIAÇÃO (POST)
# =========================
class TaskCreate(TaskBase):
    pass
    # Usado na rota POST para receber dados do usuário

# =========================
# SCHEMA: ATUALIZAÇÃO (PUT)
# =========================
class TaskUpdate(BaseModel):
    # Todos os campos são opcionais para permitir atualizações parciais
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    done: Optional[bool] = None

# =========================
# SCHEMA: RESPOSTA (GET)
# =========================
class TaskResponse(TaskBase):
    # Campos que o banco gera e que a API deve devolver
    id: int
    done: bool
    owner_id: int

    class Config:
        from_attributes = True 
        # Permite converter objetos do SQLAlchemy para JSON automaticamente

# =========================
# SCHEMA: METADADOS
# =========================
class TaskMetadata(BaseModel):
    # Informações de paginação para o envelope
    total: int
    page: int
    limit: int

# =========================
# SCHEMA: ENVELOPE (SAÍDA PADRÃO)
# =========================
class TaskResponseEnvelope(BaseModel):
    # Padronização de todas as respostas da API
    success: bool
    message: Optional[str] = None
    data: Optional[List[TaskResponse]] = None # Para listas de tarefas
    metadata: Optional[TaskMetadata] = None # Apenas se houver paginação
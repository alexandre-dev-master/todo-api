from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any, Union

class TaskCreate(BaseModel):
    """
    Schema para validacao de dados na criacao ou atualizacao de uma tarefa.
    """
    title: str
    done: Optional[bool] = False

class TaskResponse(BaseModel):
    """
    Schema para representacao dos dados de uma tarefa no retorno da API.
    """
    id: int
    title: str
    done: bool
    owner_id: int

    class Config:
        from_attributes = True

class TaskResponseEnvelope(BaseModel):
    """
    Estrutura de envelope padronizada.
    Usa Union ou tipos específicos para que o Pydantic 
    saiba como validar o conteúdo de 'data'.
    """
    success: bool
    message: str

    data: Optional[Union[TaskResponse, List[TaskResponse], Any]] = None

    class Config:
        from_attributes = True 

class UserCreate(BaseModel):
    """
    Schema para validacao de dados no registro de novos usuarios.
    """
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """
    Schema para retorno de dados publicos do usuario.
    """
    id: int
    email: EmailStr
    role: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    """
    Schema para representacao do token de acesso JWT.
    """
    access_token: str
    token_type: str
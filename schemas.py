from pydantic import BaseModel


# =========================
# USER
# =========================
class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


# =========================
# TASK
# =========================
class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None


class DefaultResponse(BaseModel):
    message: str

class TaskResponse(BaseModel):
    id: int
    title: str
    done: bool
    
    class Config:
        from_attributes = True
        
class TaskListData(BaseModel):
    items: list[TaskResponse]
    total: int
    page: int
    pages: int

class TaskResponseEnvelope(BaseModel):
    success: bool
    message: str
    data: dict | None = None
    meta: dict | None = None
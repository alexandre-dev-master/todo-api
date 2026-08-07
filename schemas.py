"""
Pydantic schemas used for request validation and API responses.
"""
from pydantic import BaseModel, ConfigDict, EmailStr


class TaskCreate(BaseModel):
    """Schema for task creation."""

    title: str
    description: str | None = None
    completed: bool = False


class TaskUpdate(BaseModel):
    """Schema for task updates."""

    title: str | None = None
    description: str | None = None
    completed: bool | None = None


class TaskResponse(BaseModel):
    """Schema returned for task resources."""

    id: int
    title: str
    description: str | None = None
    completed: bool
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class TaskResponseEnvelope(BaseModel):
    """Standard API response for task endpoints."""

    success: bool
    message: str
    data: TaskResponse | list[TaskResponse] | None = None

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    """Schema for user registration."""

    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Schema returned for user resources."""

    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """Authentication token."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """JWT payload data."""

    email: str | None = None
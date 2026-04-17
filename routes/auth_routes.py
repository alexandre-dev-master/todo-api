from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from dependencies.security import role_admin_required
from schemas import UserCreate
from services.auth_service import create_user_service, login_user_service
from models import User

router = APIRouter()


# =========================
# REGISTER
# =========================
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    create_user_service(user, db)

    return {"message": "user created"}


# =========================
# LOGIN
# =========================
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    token = login_user_service(
        form_data.username,
        form_data.password,
        db
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# =========================
# TESTE DE ADMIN
# =========================
@router.get("/admin-only")
def test_admin_route(admin: User = Depends(role_admin_required)):
    return {
        "success": True,
        "message": f"B  em-vindo, Admin {admin.username}!"
    }
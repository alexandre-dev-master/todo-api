from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import get_db
from dependencies.security import role_admin_required
from schemas import UserCreate
from services.auth_service import create_user_service, login_user_service
from models import User

router = APIRouter(tags=["Auth"]) # Adicionei a tag para organizar o Swagger

# =========================
# REGISTRO (Com correção de e-mail duplicado)
# =========================
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = create_user_service(user, db)
        return {"message": "USUÁRIO_CADASTRADO", "id": new_user.id}
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este e-mail já está registrado no sistema."
        )

# =========================
# LOGIN
# =========================
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    token = login_user_service(form_data.username, form_data.password, db)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas. Verifique usuário e senha.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# =========================
# TESTE DE ADMIN (A que estava faltando!)
# =========================
@router.get("/admin-only")
def test_admin_route(admin: User = Depends(role_admin_required)):
    """
    Rota de elite: Só quem tem role='admin' no banco de dados consegue entrar.
    """
    return {
        "success": True,
        "message": f"Acesso concedido. Bem-vindo ao painel de controle, {admin.email}!",
        "role": admin.role
    }
"""
Authentication routes.

Handles user registration, login,
and protected admin endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import get_db
from dependencies.security import role_admin_required
from models import User
from schemas import UserCreate
from services.auth_service import (
    create_user_service,
    login_user_service,
)

router = APIRouter(tags=["Auth"])


@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    try:
        new_user = create_user_service(user, db)

        return {
            "message": "User registered successfully.",
            "id": new_user.id,
        }

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered.",
        )


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    token = login_user_service(
        form_data.username,
        form_data.password,
        db,
    )

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router.get("/admin-only")
def test_admin_route(
    admin: User = Depends(role_admin_required),
):
    return {
        "success": True,
        "message": "Admin access granted.",
        "role": admin.role,
    }

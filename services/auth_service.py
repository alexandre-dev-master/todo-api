"""
Business logic for user authentication and account management.
"""

from sqlalchemy.orm import Session

from auth import create_access_token, hash_password, verify_password
from models import User
from schemas import UserCreate


def create_user_service(user: UserCreate, db: Session) -> User:
    """
    Creates a new user with a hashed password.
    """
    hashed_password = hash_password(user.password)

    new_user = User(
        email=user.email,
        hashed_password=hashed_password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user_service(
    email: str,
    password: str,
    db: Session,
) -> str | None:
    """
    Authenticates a user and returns a JWT access token.
    """
    user = db.query(User).filter(User.email == email).first()

    if user is None:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    token_data = {
        "sub": user.email,
        "role": user.role,
    }

    return create_access_token(token_data)

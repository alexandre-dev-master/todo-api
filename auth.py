"""
Authentication utilities for password hashing and JWT handling.
"""

from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from core.config import settings


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str):
    """Hashes a plain text password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    """Checks whether a password matches its hash."""
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_access_token(data: dict):
    """Creates a JWT access token."""
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
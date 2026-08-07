"""
Database models for users and tasks.
"""

from typing import List, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    """Represents an application user."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        index=True
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255)
    )

    role: Mapped[str] = mapped_column(
        String(20),
        default="user"
    )

    tasks: Mapped[List["Task"]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan"
    )


class Task(Base):
    """Represents a user task."""

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(100)
    )

    description: Mapped[Optional[str]] = mapped_column(
        String(255)
    )

    completed: Mapped[bool] = mapped_column(
        default=False
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    owner: Mapped["User"] = relationship(
        back_populates="tasks"
    )
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from models import User


def test_register_user(client: TestClient, db_session: Session):
    response = client.post(
        "/register", json={"email": "test@example.com", "password": "123456"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "User registered successfully."

    user = db_session.query(User).filter(User.email == "test@example.com").first()

    assert user is not None
    assert user.email == "test@example.com"
    assert user.hashed_password != "123456"


def test_login_user(client: TestClient):
    register_response = client.post(
        "/register", json={"email": "login@example.com", "password": "123456"}
    )

    assert register_response.status_code == 200

    response = client.post(
        "/login", data={"username": "login@example.com", "password": "123456"}
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_admin_access(client: TestClient, db_session: Session):
    client.post("/register", json={"email": "admin@example.com", "password": "123456"})

    user = db_session.query(User).filter(User.email == "admin@example.com").first()

    user.role = "admin"
    db_session.commit()

    response = client.post(
        "/login", data={"username": "admin@example.com", "password": "123456"}
    )

    token = response.json()["access_token"]

    response = client.get("/admin-only", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["role"] == "admin"

import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def auth_token(client: TestClient):
    email = f"user_{uuid.uuid4()}@example.com"

    client.post("/register", json={"email": email, "password": "123456"})

    response = client.post("/login", data={"username": email, "password": "123456"})

    return response.json()["access_token"]


@pytest.fixture
def create_user_token(client: TestClient):

    def _create_user(email: str):
        client.post("/register", json={"email": email, "password": "123456"})

        response = client.post("/login", data={"username": email, "password": "123456"})

        return response.json()["access_token"]

    return _create_user

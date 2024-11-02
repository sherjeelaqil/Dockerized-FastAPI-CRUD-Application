import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from typing import Generator

from app.main import app
from app.common.database import Base, get_db
from app.crud import crud
from app.schemas.users_schemas import UserCreate, UserRole
from app.auth import create_access_token

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db() -> Generator:
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db) -> Generator:
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def admin_user(db) -> dict:
    user = UserCreate(
        username="admin",
        email="admin@example.com",
        password="admin123",
        role=UserRole.admin
    )
    db_user = crud.create_user(db, user)
    token = create_access_token({"sub": db_user.username})
    return {"user": db_user, "token": token}

@pytest.fixture(scope="function")
def normal_user(db) -> dict:
    user = UserCreate(
        username="testuser",
        email="test@example.com",
        password="test123",
        role=UserRole.user
    )
    db_user = crud.create_user(db, user)
    token = create_access_token({"sub": db_user.username})
    return {"user": db_user, "token": token}
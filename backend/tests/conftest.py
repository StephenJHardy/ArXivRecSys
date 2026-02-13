import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from typing import Generator, Dict

from app.database import Base, get_db
from app.main import app
from app import models
from app.controllers import user_controller

# Test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db() -> Generator:
    # Create the test database and tables
    Base.metadata.create_all(bind=engine)
    
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        # Clean up after the test
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db: TestingSessionLocal) -> Generator:
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
def test_user(db: TestingSessionLocal) -> Dict:
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    db_user = user_controller.create_user(db, models.UserCreate(**user_data))
    return {"user": db_user, "password": user_data["password"]}

@pytest.fixture(scope="function")
def test_user_token(client: TestClient, test_user: Dict) -> Dict:
    response = client.post(
        "/api/users/token",
        data={
            "username": test_user["user"].email,
            "password": test_user["password"]
        }
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"} 
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

def test_create_user(client: TestClient):
    response = client.post(
        "/api/users/register",
        json={"email": "newuser@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "id" in data
    assert "created_at" in data

def test_create_user_duplicate_email(client: TestClient, test_user):
    response = client.post(
        "/api/users/register",
        json={"email": test_user["user"].email, "password": "password123"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_login_user(client: TestClient, test_user):
    response = client.post(
        "/api/users/token",
        data={
            "username": test_user["user"].email,
            "password": test_user["password"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_user_wrong_password(client: TestClient, test_user):
    response = client.post(
        "/api/users/token",
        data={
            "username": test_user["user"].email,
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

def test_read_users_me(client: TestClient, test_user_token):
    response = client.get(
        "/api/users/me",
        headers=test_user_token
    )
    assert response.status_code == 200
    data = response.json()
    assert "email" in data
    assert "id" in data

def test_read_users_me_no_token(client: TestClient):
    response = client.get("/api/users/me")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_read_user_ratings(client: TestClient, test_user_token):
    response = client.get(
        "/api/users/me/ratings",
        headers=test_user_token
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list) 
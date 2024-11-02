import pytest
from fastapi import status
from app.schemas.users_schemas import UserCreate, UserRole

def test_register_user_success(client, admin_user):
    new_user = {
        "username": "newuser",
        "email": "new@example.com",
        "password": "newpass123",
        "role": UserRole.user
    }
    response = client.post(
        "/register",
        json=new_user,
        params={"token": admin_user["token"]}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == new_user["username"]
    assert data["email"] == new_user["email"]
    assert "password" not in data

def test_register_user_duplicate_username(client, admin_user, normal_user):
    new_user = {
        "username": normal_user["user"].username,
        "email": "different@example.com",
        "password": "newpass123",
        "role": UserRole.user
    }
    response = client.post(
        "/register",
        json=new_user,
        params={"token": admin_user["token"]}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_login_success(client, normal_user):
    response = client.post(
        "/login",
        json={
            "username": "testuser",
            "password": "test123"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client):
    response = client.post(
        "/login",
        json={
            "username": "testuser",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_users_admin(client, admin_user):
    response = client.get(
        "/users",
        params={"token": admin_user["token"]}
    )
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

def test_get_users_unauthorized(client, normal_user):
    response = client.get(
        "/users",
        params={"token": normal_user["token"]}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_get_user_own_profile(client, normal_user):
    response = client.get(
        f"/users/{normal_user['user'].id}",
        params={"token": normal_user["token"]}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == normal_user["user"].username

def test_get_user_unauthorized_access(client, normal_user, admin_user):
    response = client.get(
        f"/users/{admin_user['user'].id}",
        params={"token": normal_user["token"]}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
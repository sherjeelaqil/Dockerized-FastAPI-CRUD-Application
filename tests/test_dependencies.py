import pytest
from fastapi import HTTPException
from app.dependencies import get_current_user, get_current_admin_user
from app.schemas.users_schemas import UserRole

async def test_get_current_user_valid_token(db, normal_user):
    user = await get_current_user(normal_user["token"], db)
    assert user.username == normal_user["user"].username

async def test_get_current_user_invalid_token(db):
    with pytest.raises(HTTPException) as exc:
        await get_current_user("invalid_token", db)
    assert exc.value.status_code == 401

async def test_get_current_admin_user_success(db, admin_user):
    user = await get_current_admin_user(admin_user["user"])
    assert user.role == UserRole.admin

async def test_get_current_admin_user_unauthorized(db, normal_user):
    with pytest.raises(HTTPException) as exc:
        await get_current_admin_user(normal_user["user"])
    assert exc.value.status_code == 403
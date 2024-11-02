import pytest
from app.auth import verify_password, create_access_token, decode_access_token
from jose import jwt
from app.common.config import settings

def test_verify_password():
    password = "testpassword"
    hashed = "$2b$12$LQrP6WTCy3PBmgf3Yl4IeuqWY9W6A3VZ8F9FZ9Z9Z9Z9Z9Z9Z9"
    assert not verify_password(password, hashed)

def test_create_access_token():
    data = {"sub": "testuser"}
    token = create_access_token(data)
    assert token
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert decoded["sub"] == "testuser"
    assert "exp" in decoded

def test_decode_access_token():
    original_data = {"sub": "testuser"}
    token = create_access_token(original_data)
    token_data = decode_access_token(token)
    assert token_data.username == "testuser"

def test_decode_access_token_invalid():
    with pytest.raises(ValueError):
        decode_access_token("invalid_token")
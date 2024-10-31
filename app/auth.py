# app/auth.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

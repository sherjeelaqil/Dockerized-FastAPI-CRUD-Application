from fastapi import HTTPException, Request
from jose import jwt, JWTError
from app.common.config import settings
from app.models.users_models import UserRole

async def verify_admin(request: Request):
    token = request.query_params.get("token")
    if not token:
        raise HTTPException(status_code=403, detail="Token missing")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        if payload.get("role") != UserRole.admin:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid credentials")

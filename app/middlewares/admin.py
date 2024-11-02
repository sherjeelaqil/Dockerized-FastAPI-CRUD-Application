from fastapi import HTTPException, Request
from jose import jwt, JWTError
from app.common.config import settings
from app.models.users_models import UserRole

async def verify_admin(request: Request):
    """
    Verify if the request is done by an admin.

    This middleware will verify if the request query params contains a valid admin token.
    If the token is invalid or missing, it will raise a 403 error.

    :param request: The incoming request
    :type request: fastapi.Request
    :raises HTTPException: if the token is invalid or missing
    """
    token = request.query_params.get("token")
    if not token:
        raise HTTPException(status_code=403, detail="Token missing")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        if payload.get("role") != UserRole.admin:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid credentials")

from fastapi import Depends, HTTPException, status, Request
from app import auth
from app.common.database import get_db
from jose import JWTError
from sqlalchemy.orm import Session
from app.crud import crud
from app.models import users_models

async def get_token(request: Request) -> str:
    token = request.query_params.get('token')
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No token provided"
        )
    return token

async def get_current_user(
    token: str = Depends(get_token),
    db: Session = Depends(get_db)
):
    try:
        token_data = auth.decode_access_token(token)
        if token_data.username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return user

async def get_current_admin_user(current_user: users_models.User = Depends(get_current_user)):
    if current_user.role != users_models.UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

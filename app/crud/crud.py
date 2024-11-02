from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.schemas import users_schemas
from fastapi import HTTPException, status

from app.models import users_models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, user_id: int):
    return db.query(users_models.User).filter(users_models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(users_models.User).filter(users_models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(users_models.User).filter(users_models.User.email == email).first()

def get_all_users(db: Session):
    return db.query(users_models.User).all()

def create_user(db: Session, user: users_schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = users_models.User(username=user.username, email=user.email, password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: users_schemas.UserCreate, current_user_role: users_schemas.UserRole):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if current_user_role != users_schemas.UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    db_user.username = user.username or db_user.username
    db_user.email = user.email or db_user.email
    if user.password:
        db_user.password = pwd_context.hash(user.password)
    db_user.role = user.role or db_user.role

    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int, current_user_role: users_schemas.UserRole):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if current_user_role != users_schemas.UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted successfully"}

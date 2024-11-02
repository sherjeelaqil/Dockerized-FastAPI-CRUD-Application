from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.schemas import users_schemas
from fastapi import HTTPException, status

from app.models import users_models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, user_id: int):
    """
    Return a user by their ID.

    Args:
        db (Session): Database session.
        user_id (int): User ID.

    Returns:
        users_models.User: User model.
    """
    return db.query(users_models.User).filter(users_models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    """
    Retrieve a user by their username.

    Args:
        db (Session): Database session.
        username (str): Username of the user to retrieve.

    Returns:
        users_models.User or None: User model if found, otherwise None.
    """
    return db.query(users_models.User).filter(users_models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    """
    Retrieve a user by their email.

    Args:
        db (Session): Database session.
        email (str): Email of the user to retrieve.

    Returns:
        users_models.User or None: User model if found, otherwise None.
    """
    return db.query(users_models.User).filter(users_models.User.email == email).first()

def get_all_users(db: Session):
    """
    Retrieve all users from the database.

    Args:
        db (Session): Database session.

    Returns:
        List[users_models.User]: List of all users in the database.
    """
    return db.query(users_models.User).all()

def create_user(db: Session, user: users_schemas.UserCreate):
    """
    Create a new user in the database.

    Args:
        db (Session): Database session.
        user (users_schemas.UserCreate): User to be created.

    Returns:
        users_models.User: Created user model.
    """
    hashed_password = pwd_context.hash(user.password)
    db_user = users_models.User(username=user.username, email=user.email, password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: users_schemas.UserCreate, current_user_role: users_schemas.UserRole):
    """
    Update a user's information in the database.

    Args:
        db (Session): Database session.
        user_id (int): ID of the user to update.
        user (users_schemas.UserCreate): New user data.
        current_user_role (users_schemas.UserRole): Role of the current user performing the update.

    Returns:
        users_models.User: Updated user model.

    Raises:
        HTTPException: If the user is not found or if the current user lacks permissions.
    """
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
    """
    Delete a user from the database.

    Args:
        db (Session): Database session.
        user_id (int): ID of the user to delete.
        current_user_role (users_schemas.UserRole): Role of the current user performing the deletion.

    Returns:
        dict: A dictionary with a key "detail" containing the string "User deleted successfully".

    Raises:
        HTTPException: If the user is not found or if the current user lacks permissions.
    """
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if current_user_role != users_schemas.UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted successfully"}

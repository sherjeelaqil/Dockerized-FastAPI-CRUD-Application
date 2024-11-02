from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from typing import List
from app import auth
from app.common.database import get_db
from app.common.limiter import rate_limiter
from app.crud import crud
from app.dependencies import get_current_user, get_current_admin_user
from app.models import users_models
from app.schemas import users_schemas
from app.schemas.users_schemas import UserRole
from app.schemas.token import Token
from app.common.logging_config import logger

router = APIRouter()

@router.post("/register", response_model=users_schemas.UserResponse)
def register_user(
    user: users_schemas.UserCreate,
    db: Session = Depends(get_db),
    admin_user: users_models.User = Depends(get_current_admin_user),
    token: str = Query(..., description="JWT token for authorization")
):
    """
    Creates a new user in the database.

    Args:
        user (users_schemas.UserCreate): The new user to be created.
        db (Session): The database session.
        admin_user (users_models.User): The admin user performing the registration.
        token (str): The JWT token for authorization.

    Raises:
        HTTPException: If the username or email is already registered.
    """
    logger.info(f"Admin {admin_user.username} attempting to register a new user: {user.username}")
    db_user = crud.get_user_by_username(db, user.username)
    db_email = crud.get_user_by_email(db, user.email)

    if db_user:
        logger.warning(f"Registration failed: Username '{user.username}' is already registered")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    if db_email:
        logger.warning(f"Registration failed: Email '{user.email}' is already registered")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    logger.info(f"User {user.username} successfully registered by admin {admin_user.username}")
    return crud.create_user(db=db, user=user)

@router.post("/login", response_model=Token)
def login(
    user: users_schemas.UserLogin,
    db: Session = Depends(get_db),
    request: Request = None
):
    """
    Authenticates a user using a username and password.

    Args:
        user (users_schemas.UserLogin): The user credentials.
        db (Session): The database session.
        request (Request): The current request.

    Raises:
        HTTPException: If the credentials are invalid.

    Returns:
        Token: The access token for the user.
    """
    rate_limiter(request)
    logger.info(f"Login attempt for user: {user.username}")
    db_user = crud.get_user_by_username(db, user.username)
    if not db_user or not auth.verify_password(user.password, db_user.password):
        logger.warning(f"Login failed for user: {user.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = auth.create_access_token(data={"sub": db_user.username, "role": db_user.role})
    logger.info(f"User {user.username} logged in successfully")
    return {"access_token": token, "token_type": "bearer"}

@router.get("/users", response_model=List[users_schemas.UserResponse], dependencies=[Depends(get_current_admin_user)])
def read_users(
    db: Session = Depends(get_db),
    token: str = Query(..., description="JWT token for authorization")
):
    """
    Retrieves all users from the database.

    Args:
        db (Session): The database session.
        token (str): The JWT token for authorization.

    Returns:
        List[users_schemas.UserResponse]: A list of all users in the database.
    """
    return crud.get_all_users(db)

@router.get("/users/{user_id}", response_model=users_schemas.UserResponse)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: users_schemas.UserResponse = Depends(get_current_user),
    token: str = Query(..., description="JWT token for authorization")
):
    """
    Retrieves a user from the database by ID.

    Args:
        user_id (int): ID of the user to retrieve.
        db (Session): The database session.
        current_user (users_schemas.UserResponse): The user performing the request.
        token (str): The JWT token for authorization.

    Returns:
        users_schemas.UserResponse: The user model retrieved from the database.

    Raises:
        HTTPException: If the user is not found or if the current user lacks permissions.
    """
    
    logger.info(f"User {current_user.username} attempting to access user ID {user_id}")
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        logger.warning(f"User ID {user_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if db_user.id != current_user.id and current_user.role != UserRole.admin:
        logger.warning(f"Unauthorized access attempt by {current_user.username} to user ID {user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )
    logger.info(f"User ID {user_id} details accessed successfully by {current_user.username}")
    return db_user

@router.put("/users/{user_id}", response_model=users_schemas.UserResponse, dependencies=[Depends(get_current_admin_user)])
def update_user(
    user_id: int,
    user: users_schemas.UserUpdate,
    db: Session = Depends(get_db),
    token: str = Query(..., description="JWT token for authorization")
):
    """
    Updates a user in the database.

    Args:
        user_id (int): ID of the user to update.
        user (users_schemas.UserUpdate): The new user data.
        db (Session): The database session.
        token (str): The JWT token for authorization.

    Returns:
        users_schemas.UserResponse: The updated user model.

    Raises:
        HTTPException: If the user is not found or if the current user lacks permissions.
    """
    logger.info(f"Admin attempting to update user ID {user_id}")
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        logger.warning(f"User ID {user_id} not found for update")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    updated_user = crud.update_user(db, user_id=user_id, user=user, current_user_role=user.role)
    logger.info(f"User ID {user_id} updated successfully")
    return updated_user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_admin_user)])
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    token: str = Query(..., description="JWT token for authorization")
):
    """
    Deletes a user from the database.

    Args:
        user_id (int): ID of the user to delete.
        db (Session): The database session.
        token (str): The JWT token for authorization.

    Raises:
        HTTPException: If the user is not found or if the current user lacks permissions.

    Returns:
        dict: A dictionary with a key "status" containing the string "success".
    """

    logger.info(f"Admin attempting to delete user ID {user_id}")
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        logger.warning(f"User ID {user_id} not found for deletion")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    crud.delete_user(db, user_id=user_id, current_user_role=db_user.role)
    logger.info(f"User ID {user_id} deleted successfully")
    return {"status": "success"}
from sqlalchemy.orm import Session
from app.models.users_models import User, UserRole
from app.common.database import SessionLocal
from passlib.hash import bcrypt

def create_admin_user(db: Session):
    """
    Creates an admin user if one does not exist.

    Args:
        db (Session): The SQLAlchemy session to use.

    Returns:
        None
    """
    admin_email = "admin@example.com"
    admin_username = "admin"
    admin_password = "strongpass123"
    admin_role = UserRole.admin

    # Check if an admin user already exists
    admin_user = db.query(User).filter(User.email == admin_email).first()
    if not admin_user:
        # Create admin user if not found
        new_admin = User(
            email=admin_email,
            username=admin_username,
            password=bcrypt.hash(admin_password),  # Securely hash the password
            role=admin_role
        )
        db.add(new_admin)
        db.commit()
        print("Admin user created.")
    else:
        print("Admin user already exists.")

def initialize_database():
    """
    Initializes the database by creating an admin user if one does not exist.

    This function creates a local database session and calls create_admin_user to
    create an admin user if one does not exist. Finally, it closes the database
    session.

    Args:
        None

    Returns:
        None
    """
    db = SessionLocal()
    try:
        create_admin_user(db)
    finally:
        db.close()

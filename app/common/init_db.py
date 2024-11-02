from sqlalchemy.orm import Session
from app.models.users_models import User, UserRole
from app.common.database import SessionLocal
from passlib.hash import bcrypt

def create_admin_user(db: Session):
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
    db = SessionLocal()
    try:
        create_admin_user(db)
    finally:
        db.close()

from pydantic import BaseModel, EmailStr, Field, validator
from enum import Enum
from typing import Optional

class UserRole(str, Enum):
    admin = "admin"
    user = "user"

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: UserRole

    class Config:
        json_schema_extra = {
            "example": {
                "username": "test",
                "email": "test@example.com",
                "password": "strongpass123",
                "role": "user"
            }
        }

class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    role: Optional[UserRole]

class UserResponse(UserBase):
    id: int
    role: UserRole

class UserLogin(BaseModel):
    username: str
    password: str


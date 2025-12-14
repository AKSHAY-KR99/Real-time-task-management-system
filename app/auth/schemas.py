from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    role: str = "user"

    @field_validator("password")
    @classmethod
    def validate_password_length(cls, value: str):
        if len(value.encode("utf-8")) > 72:
            raise ValueError("Password must be at most 72 characters")
        if len(value) < 6:
            raise ValueError("Password must be at least 6 characters")
        return value


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: Optional[str] = None
    role: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
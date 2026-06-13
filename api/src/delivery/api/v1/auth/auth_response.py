from pydantic import BaseModel

from src.domain.user import UserRole


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class UserResponse(BaseModel):
    email: str
    name: str
    role: UserRole

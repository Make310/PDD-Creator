from dataclasses import dataclass
from enum import StrEnum


class UserRole(StrEnum):
    ADMIN = "admin"
    USER = "user"


@dataclass(frozen=True)
class User:
    email: str
    name: str
    role: UserRole
    is_active: bool
    password_hash: str

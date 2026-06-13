from datetime import UTC, datetime
from typing import Annotated, ClassVar

from beanie import Document, Indexed

from src.domain.user import User, UserRole


class UserDocument(Document):
    email: Annotated[str, Indexed(unique=True)]
    password_hash: str
    name: str
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Settings:
        name = "users"
        indexes: ClassVar[list[str]] = ["role"]

    @classmethod
    def from_domain(cls, user: User) -> "UserDocument":
        now = datetime.now(UTC)
        return cls(
            email=user.email,
            password_hash=user.password_hash,
            name=user.name,
            role=user.role,
            is_active=user.is_active,
            created_at=now,
            updated_at=now,
        )

    def to_domain(self) -> User:
        return User(
            email=self.email,
            name=self.name,
            role=self.role,
            is_active=self.is_active,
            password_hash=self.password_hash,
        )

from abc import ABC, abstractmethod

from src.domain.user import User


class UserRepositoryException(Exception):
    pass


class UserRepository(ABC):
    @abstractmethod
    async def find_by_email(self, email: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def save(self, user: User) -> None:
        raise NotImplementedError

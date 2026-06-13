from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.domain.user import User


@dataclass(frozen=True)
class AuthToken:
    access_token: str
    expires_in_seconds: int


class TokenService(ABC):
    @abstractmethod
    def issue(self, user: User) -> AuthToken:
        raise NotImplementedError

    @abstractmethod
    def verify(self, token: str) -> str:
        """Returns the subject (user email) of a valid token. Raises InvalidTokenException otherwise."""
        raise NotImplementedError

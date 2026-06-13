from datetime import UTC, datetime, timedelta

import jwt

from src.domain.exceptions import InvalidTokenException
from src.domain.token_service import AuthToken, TokenService
from src.domain.user import User

SECONDS_PER_MINUTE = 60


class JwtTokenService(TokenService):
    ALGORITHM = "HS256"

    def __init__(self, secret_key: str, ttl_minutes: int) -> None:
        self._secret_key = secret_key
        self._ttl_minutes = ttl_minutes

    def issue(self, user: User) -> AuthToken:
        issued_at = datetime.now(UTC)
        payload = {
            "sub": user.email,
            "role": user.role.value,
            "iat": issued_at,
            "exp": issued_at + timedelta(minutes=self._ttl_minutes),
        }
        access_token = jwt.encode(payload, self._secret_key, algorithm=self.ALGORITHM)
        return AuthToken(access_token=access_token, expires_in_seconds=self._ttl_minutes * SECONDS_PER_MINUTE)

    def verify(self, token: str) -> str:
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self.ALGORITHM])
        except jwt.InvalidTokenError as ex:
            raise InvalidTokenException("Invalid or expired token") from ex

        subject = payload.get("sub")
        if not isinstance(subject, str) or not subject:
            raise InvalidTokenException("Invalid or expired token")
        return subject

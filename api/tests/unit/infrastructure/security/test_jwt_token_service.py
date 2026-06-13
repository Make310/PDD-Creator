from datetime import UTC, datetime, timedelta

import jwt
from expects import equal, expect, raise_error

from src.domain.exceptions import InvalidTokenException
from src.domain.user import User, UserRole
from src.infrastructure.security.jwt_token_service import JwtTokenService

SECRET_KEY = "test-secret-0123456789-0123456789-0123456789"
TTL_MINUTES = 60
USER = User(email="user@example.com", name="Jane Doe", role=UserRole.USER, is_active=True, password_hash="$2b$12$h")


class TestJwtTokenService:
    def _service(self, ttl_minutes: int = TTL_MINUTES) -> JwtTokenService:
        return JwtTokenService(secret_key=SECRET_KEY, ttl_minutes=ttl_minutes)

    def test_issue_returns_token_with_ttl_in_seconds(self) -> None:
        auth_token = self._service().issue(USER)

        expect(auth_token.expires_in_seconds).to(equal(TTL_MINUTES * 60))

    def test_verify_returns_the_subject_of_an_issued_token(self) -> None:
        service = self._service()
        auth_token = service.issue(USER)

        expect(service.verify(auth_token.access_token)).to(equal(USER.email))

    def test_verify_rejects_an_expired_token(self) -> None:
        service = self._service()
        expired_token = self._service(ttl_minutes=-1).issue(USER)

        expect(lambda: service.verify(expired_token.access_token)).to(raise_error(InvalidTokenException))

    def test_verify_rejects_a_tampered_token(self) -> None:
        service = self._service()
        auth_token = service.issue(USER)
        tampered = auth_token.access_token[:-2] + ("aa" if not auth_token.access_token.endswith("aa") else "bb")

        expect(lambda: service.verify(tampered)).to(raise_error(InvalidTokenException))

    def test_verify_rejects_a_token_signed_with_another_secret(self) -> None:
        service = self._service()
        foreign_secret = "another-secret-0123456789-0123456789-0123456789"
        foreign_token = JwtTokenService(secret_key=foreign_secret, ttl_minutes=TTL_MINUTES).issue(USER)

        expect(lambda: service.verify(foreign_token.access_token)).to(raise_error(InvalidTokenException))

    def test_verify_rejects_a_token_without_subject(self) -> None:
        service = self._service()
        expires_at = datetime.now(UTC) + timedelta(minutes=TTL_MINUTES)
        token_without_subject = jwt.encode({"exp": expires_at}, SECRET_KEY, algorithm=JwtTokenService.ALGORITHM)

        expect(lambda: service.verify(token_without_subject)).to(raise_error(InvalidTokenException))

    def test_verify_rejects_garbage(self) -> None:
        expect(lambda: self._service().verify("not-a-jwt")).to(raise_error(InvalidTokenException))

from collections.abc import Generator
from http.client import OK, UNAUTHORIZED, UNPROCESSABLE_ENTITY

import pytest
from doublex import ANY_ARG, Mimic, Stub
from expects import equal, expect
from fastapi.testclient import TestClient

from main import app, settings
from src.delivery.api.v1.auth.auth_dependencies import (
    UNAUTHORIZED_DETAIL,
    authenticate_user_command_handler,
    login_command_handler,
)
from src.delivery.api.v1.auth.auth_router import LOGIN_FAILED_DETAIL
from src.domain.exceptions import InvalidCredentialsException, InvalidTokenException
from src.domain.token_service import AuthToken
from src.domain.user import User, UserRole
from src.infrastructure.security.jwt_token_service import JwtTokenService
from src.use_cases.authenticate_user_command import AuthenticateUserCommandHandler, AuthenticateUserCommandResponse
from src.use_cases.login_command import LoginCommandHandler, LoginCommandResponse
from tests.support import resolved

LOGIN_URL = "/auth/login"
ME_URL = "/auth/me"
LOGIN_BODY = {"email": "user@example.com", "password": "secret-password"}
USER = User(email="user@example.com", name="Jane Doe", role=UserRole.USER, is_active=True, password_hash="$2b$12$hash")
AUTH_TOKEN = AuthToken(access_token="a.jwt.token", expires_in_seconds=3600)


class TestAuthController:
    @pytest.fixture
    def client(self) -> Generator[TestClient]:
        yield TestClient(app)
        app.dependency_overrides.clear()

    def _stub_login_handler(self, response: LoginCommandResponse) -> None:
        with Mimic(Stub, LoginCommandHandler) as handler:
            handler.execute(ANY_ARG).returns(resolved(response))
        app.dependency_overrides[login_command_handler] = lambda: handler

    def _stub_failing_login_handler(self) -> None:
        with Mimic(Stub, LoginCommandHandler) as handler:
            handler.execute(ANY_ARG).raises(InvalidCredentialsException("Invalid credentials"))
        app.dependency_overrides[login_command_handler] = lambda: handler

    def _stub_authenticate_handler(self, response: AuthenticateUserCommandResponse) -> None:
        with Mimic(Stub, AuthenticateUserCommandHandler) as handler:
            handler.execute(ANY_ARG).returns(resolved(response))
        app.dependency_overrides[authenticate_user_command_handler] = lambda: handler

    def _stub_failing_authenticate_handler(self) -> None:
        with Mimic(Stub, AuthenticateUserCommandHandler) as handler:
            handler.execute(ANY_ARG).raises(InvalidTokenException("Invalid or expired token"))
        app.dependency_overrides[authenticate_user_command_handler] = lambda: handler

    def test_login_returns_token_for_valid_credentials(self, client: TestClient) -> None:
        self._stub_login_handler(LoginCommandResponse(AUTH_TOKEN))

        response = client.post(f"{settings.api_v1_prefix}{LOGIN_URL}", json=LOGIN_BODY)

        expect(response.status_code).to(equal(OK))
        expect(response.json()).to(
            equal({"access_token": AUTH_TOKEN.access_token, "token_type": "bearer", "expires_in": 3600})
        )

    def test_login_returns_generic_unauthorized_for_invalid_credentials(self, client: TestClient) -> None:
        self._stub_failing_login_handler()

        response = client.post(f"{settings.api_v1_prefix}{LOGIN_URL}", json=LOGIN_BODY)

        expect(response.status_code).to(equal(UNAUTHORIZED))
        expect(response.json()).to(equal({"detail": LOGIN_FAILED_DETAIL}))

    def test_login_with_missing_fields_returns_validation_error(self, client: TestClient) -> None:
        response = client.post(f"{settings.api_v1_prefix}{LOGIN_URL}", json={})

        expect(response.status_code).to(equal(UNPROCESSABLE_ENTITY))

    def test_login_with_malformed_email_returns_validation_error(self, client: TestClient) -> None:
        response = client.post(f"{settings.api_v1_prefix}{LOGIN_URL}", json={"email": "not-an-email", "password": "x"})

        expect(response.status_code).to(equal(UNPROCESSABLE_ENTITY))

    def test_me_returns_authenticated_user_info(self, client: TestClient) -> None:
        self._stub_authenticate_handler(AuthenticateUserCommandResponse(USER))

        response = client.get(f"{settings.api_v1_prefix}{ME_URL}", headers={"Authorization": "Bearer a.jwt.token"})

        expect(response.status_code).to(equal(OK))
        expect(response.json()).to(equal({"email": USER.email, "name": USER.name, "role": "user"}))

    def test_me_without_token_returns_unauthorized(self, client: TestClient) -> None:
        response = client.get(f"{settings.api_v1_prefix}{ME_URL}")

        expect(response.status_code).to(equal(UNAUTHORIZED))
        expect(response.json()).to(equal({"detail": UNAUTHORIZED_DETAIL}))

    def test_me_with_invalid_token_returns_unauthorized(self, client: TestClient) -> None:
        self._stub_failing_authenticate_handler()

        response = client.get(
            f"{settings.api_v1_prefix}{ME_URL}", headers={"Authorization": "Bearer not-a-valid-token"}
        )

        expect(response.status_code).to(equal(UNAUTHORIZED))
        expect(response.json()).to(equal({"detail": UNAUTHORIZED_DETAIL}))

    def test_me_with_expired_token_returns_unauthorized(self, client: TestClient) -> None:
        expired_service = JwtTokenService(secret_key=settings.auth_secret_key, ttl_minutes=-1)
        expired_token = expired_service.issue(USER).access_token

        response = client.get(f"{settings.api_v1_prefix}{ME_URL}", headers={"Authorization": f"Bearer {expired_token}"})

        expect(response.status_code).to(equal(UNAUTHORIZED))
        expect(response.json()).to(equal({"detail": UNAUTHORIZED_DETAIL}))

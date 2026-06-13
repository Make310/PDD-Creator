import asyncio

from doublex import Mimic, Stub
from expects import equal, expect, raise_error

from src.domain.exceptions import InvalidCredentialsException
from src.domain.token_service import AuthToken
from src.domain.user import User, UserRole
from src.infrastructure.mongo.mongo_user_repository import MongoUserRepository
from src.infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher
from src.infrastructure.security.jwt_token_service import JwtTokenService
from src.use_cases.login_command import LoginCommand, LoginCommandHandler
from tests.support import resolved

EMAIL = "user@example.com"
PASSWORD = "secret-password"
PASSWORD_HASH = "$2b$12$hashed"
AUTH_TOKEN = AuthToken(access_token="a.jwt.token", expires_in_seconds=3600)


class TestLoginCommandHandler:
    def _user(self, is_active: bool = True) -> User:
        return User(email=EMAIL, name="Jane Doe", role=UserRole.USER, is_active=is_active, password_hash=PASSWORD_HASH)

    def test_execute_returns_token_for_active_user_with_valid_credentials(self) -> None:
        user = self._user()
        command = LoginCommand(email=EMAIL, password=PASSWORD)
        with Mimic(Stub, MongoUserRepository) as repository:
            repository.find_by_email(EMAIL).returns(resolved(user))
        with Mimic(Stub, BcryptPasswordHasher) as hasher:
            hasher.verify(PASSWORD, PASSWORD_HASH).returns(True)
        with Mimic(Stub, JwtTokenService) as token_service:
            token_service.issue(user).returns(AUTH_TOKEN)

        handler = LoginCommandHandler(repository, hasher, token_service)
        response = asyncio.run(handler.execute(command))

        expect(response.message()).to(equal(AUTH_TOKEN))

    def test_execute_rejects_unknown_email(self) -> None:
        command = LoginCommand(email=EMAIL, password=PASSWORD)
        with Mimic(Stub, MongoUserRepository) as repository:
            repository.find_by_email(EMAIL).returns(resolved(None))
        hasher = Mimic(Stub, BcryptPasswordHasher)
        token_service = Mimic(Stub, JwtTokenService)

        handler = LoginCommandHandler(repository, hasher, token_service)

        expect(lambda: asyncio.run(handler.execute(command))).to(raise_error(InvalidCredentialsException))

    def test_execute_rejects_wrong_password(self) -> None:
        user = self._user()
        command = LoginCommand(email=EMAIL, password=PASSWORD)
        with Mimic(Stub, MongoUserRepository) as repository:
            repository.find_by_email(EMAIL).returns(resolved(user))
        with Mimic(Stub, BcryptPasswordHasher) as hasher:
            hasher.verify(PASSWORD, PASSWORD_HASH).returns(False)
        token_service = Mimic(Stub, JwtTokenService)

        handler = LoginCommandHandler(repository, hasher, token_service)

        expect(lambda: asyncio.run(handler.execute(command))).to(raise_error(InvalidCredentialsException))

    def test_execute_rejects_deactivated_user_even_with_correct_password(self) -> None:
        user = self._user(is_active=False)
        command = LoginCommand(email=EMAIL, password=PASSWORD)
        with Mimic(Stub, MongoUserRepository) as repository:
            repository.find_by_email(EMAIL).returns(resolved(user))
        with Mimic(Stub, BcryptPasswordHasher) as hasher:
            hasher.verify(PASSWORD, PASSWORD_HASH).returns(True)
        token_service = Mimic(Stub, JwtTokenService)

        handler = LoginCommandHandler(repository, hasher, token_service)

        expect(lambda: asyncio.run(handler.execute(command))).to(raise_error(InvalidCredentialsException))

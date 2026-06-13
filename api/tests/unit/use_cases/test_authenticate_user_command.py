import asyncio

from doublex import Mimic, Stub
from expects import equal, expect, raise_error

from src.domain.exceptions import InvalidTokenException
from src.domain.user import User, UserRole
from src.infrastructure.mongo.mongo_user_repository import MongoUserRepository
from src.infrastructure.security.jwt_token_service import JwtTokenService
from src.use_cases.authenticate_user_command import AuthenticateUserCommand, AuthenticateUserCommandHandler
from tests.support import resolved

EMAIL = "user@example.com"
TOKEN = "a.jwt.token"


class TestAuthenticateUserCommandHandler:
    def _user(self, is_active: bool = True) -> User:
        return User(email=EMAIL, name="Jane Doe", role=UserRole.USER, is_active=is_active, password_hash="$2b$12$h")

    def test_execute_returns_user_for_valid_token(self) -> None:
        user = self._user()
        command = AuthenticateUserCommand(token=TOKEN)
        with Mimic(Stub, JwtTokenService) as token_service:
            token_service.verify(TOKEN).returns(EMAIL)
        with Mimic(Stub, MongoUserRepository) as repository:
            repository.find_by_email(EMAIL).returns(resolved(user))

        handler = AuthenticateUserCommandHandler(repository, token_service)
        response = asyncio.run(handler.execute(command))

        expect(response.message()).to(equal(user))

    def test_execute_rejects_invalid_token(self) -> None:
        command = AuthenticateUserCommand(token=TOKEN)
        with Mimic(Stub, JwtTokenService) as token_service:
            token_service.verify(TOKEN).raises(InvalidTokenException("Invalid or expired token"))
        repository = Mimic(Stub, MongoUserRepository)

        handler = AuthenticateUserCommandHandler(repository, token_service)

        expect(lambda: asyncio.run(handler.execute(command))).to(raise_error(InvalidTokenException))

    def test_execute_rejects_token_of_unknown_user(self) -> None:
        command = AuthenticateUserCommand(token=TOKEN)
        with Mimic(Stub, JwtTokenService) as token_service:
            token_service.verify(TOKEN).returns(EMAIL)
        with Mimic(Stub, MongoUserRepository) as repository:
            repository.find_by_email(EMAIL).returns(resolved(None))

        handler = AuthenticateUserCommandHandler(repository, token_service)

        expect(lambda: asyncio.run(handler.execute(command))).to(raise_error(InvalidTokenException))

    def test_execute_rejects_token_of_deactivated_user(self) -> None:
        user = self._user(is_active=False)
        command = AuthenticateUserCommand(token=TOKEN)
        with Mimic(Stub, JwtTokenService) as token_service:
            token_service.verify(TOKEN).returns(EMAIL)
        with Mimic(Stub, MongoUserRepository) as repository:
            repository.find_by_email(EMAIL).returns(resolved(user))

        handler = AuthenticateUserCommandHandler(repository, token_service)

        expect(lambda: asyncio.run(handler.execute(command))).to(raise_error(InvalidTokenException))

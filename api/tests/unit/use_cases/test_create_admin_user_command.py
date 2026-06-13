import asyncio

from doublex import Mimic, Stub
from expects import equal, expect, raise_error

from src.domain.exceptions import UserAlreadyExistsException
from src.domain.user import User, UserRole
from src.infrastructure.mongo.mongo_user_repository import MongoUserRepository
from src.infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher
from src.use_cases.create_admin_user_command import CreateAdminUserCommand, CreateAdminUserCommandHandler
from tests.support import resolved

EMAIL = "admin@example.com"
NAME = "Admin"
PASSWORD = "secret-password"
PASSWORD_HASH = "$2b$12$hashed"


class TestCreateAdminUserCommandHandler:
    def test_execute_creates_active_admin_with_hashed_password(self) -> None:
        command = CreateAdminUserCommand(email=EMAIL, name=NAME, password=PASSWORD)
        expected_user = User(email=EMAIL, name=NAME, role=UserRole.ADMIN, is_active=True, password_hash=PASSWORD_HASH)
        with Mimic(Stub, MongoUserRepository) as repository:
            repository.find_by_email(EMAIL).returns(resolved(None))
            repository.save(expected_user).returns(resolved(None))
        with Mimic(Stub, BcryptPasswordHasher) as hasher:
            hasher.hash(PASSWORD).returns(PASSWORD_HASH)

        handler = CreateAdminUserCommandHandler(repository, hasher)
        response = asyncio.run(handler.execute(command))

        expect(response.message()).to(equal(EMAIL))

    def test_execute_rejects_existing_email(self) -> None:
        command = CreateAdminUserCommand(email=EMAIL, name=NAME, password=PASSWORD)
        existing = User(email=EMAIL, name=NAME, role=UserRole.ADMIN, is_active=True, password_hash=PASSWORD_HASH)
        with Mimic(Stub, MongoUserRepository) as repository:
            repository.find_by_email(EMAIL).returns(resolved(existing))
        hasher = Mimic(Stub, BcryptPasswordHasher)

        handler = CreateAdminUserCommandHandler(repository, hasher)

        expect(lambda: asyncio.run(handler.execute(command))).to(raise_error(UserAlreadyExistsException))

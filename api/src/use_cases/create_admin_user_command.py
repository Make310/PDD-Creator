from logging import Logger

from src.common.logger import logger
from src.domain.command import AsyncCommandHandler, Command, CommandResponse
from src.domain.exceptions import UserAlreadyExistsException
from src.domain.password_hasher import PasswordHasher
from src.domain.user import User, UserRole
from src.domain.user_repository import UserRepository


class CreateAdminUserCommand(Command):
    def __init__(self, email: str, name: str, password: str) -> None:
        self.email = email
        self.name = name
        self.password = password
        super().__init__()


class CreateAdminUserCommandResponse(CommandResponse):
    def __init__(self, email: str) -> None:
        self._email = email

    def message(self) -> str:
        return self._email


class CreateAdminUserCommandHandler(AsyncCommandHandler[CreateAdminUserCommand, CreateAdminUserCommandResponse]):
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        _logger: Logger = logger,
    ) -> None:
        self._user_repository = user_repository
        self._password_hasher = password_hasher
        self._logger = _logger

    async def execute(self, command: CreateAdminUserCommand) -> CreateAdminUserCommandResponse:
        command_id = command.command_id
        self._logger.info(f"Command {command_id}: CreateAdminUserCommandHandler#execute")

        existing = await self._user_repository.find_by_email(command.email)
        if existing is not None:
            raise UserAlreadyExistsException(f"A user with email {command.email} already exists")

        user = User(
            email=command.email,
            name=command.name,
            role=UserRole.ADMIN,
            is_active=True,
            password_hash=self._password_hasher.hash(command.password),
        )
        await self._user_repository.save(user)
        self._logger.info(f"Command {command_id}: admin user created")
        return CreateAdminUserCommandResponse(user.email)

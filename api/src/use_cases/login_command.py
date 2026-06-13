from logging import Logger
from typing import NoReturn
from uuid import UUID

from src.common.logger import logger
from src.domain.command import AsyncCommandHandler, Command, CommandResponse
from src.domain.exceptions import InvalidCredentialsException
from src.domain.password_hasher import PasswordHasher
from src.domain.token_service import AuthToken, TokenService
from src.domain.user_repository import UserRepository


class LoginCommand(Command):
    def __init__(self, email: str, password: str) -> None:
        self.email = email
        self.password = password
        super().__init__()


class LoginCommandResponse(CommandResponse):
    def __init__(self, auth_token: AuthToken) -> None:
        self._auth_token = auth_token

    def message(self) -> AuthToken:
        return self._auth_token


class LoginCommandHandler(AsyncCommandHandler[LoginCommand, LoginCommandResponse]):
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        token_service: TokenService,
        _logger: Logger = logger,
    ) -> None:
        self._user_repository = user_repository
        self._password_hasher = password_hasher
        self._token_service = token_service
        self._logger = _logger

    async def execute(self, command: LoginCommand) -> LoginCommandResponse:
        command_id = command.command_id
        self._logger.info(f"Command {command_id}: LoginCommandHandler#execute")

        user = await self._user_repository.find_by_email(command.email)
        if user is None or not self._password_hasher.verify(command.password, user.password_hash):
            self._reject(command_id)
        if not user.is_active:
            self._reject(command_id)

        auth_token = self._token_service.issue(user)
        self._logger.info(f"Command {command_id}: login succeeded for user role {user.role}")
        return LoginCommandResponse(auth_token)

    def _reject(self, command_id: UUID) -> NoReturn:
        self._logger.info(f"Command {command_id}: login rejected")
        raise InvalidCredentialsException("Invalid credentials")

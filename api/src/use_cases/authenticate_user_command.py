from logging import Logger

from src.common.logger import logger
from src.domain.command import AsyncCommandHandler, Command, CommandResponse
from src.domain.exceptions import InvalidTokenException
from src.domain.token_service import TokenService
from src.domain.user import User
from src.domain.user_repository import UserRepository


class AuthenticateUserCommand(Command):
    def __init__(self, token: str) -> None:
        self.token = token
        super().__init__()


class AuthenticateUserCommandResponse(CommandResponse):
    def __init__(self, user: User) -> None:
        self._user = user

    def message(self) -> User:
        return self._user


class AuthenticateUserCommandHandler(AsyncCommandHandler[AuthenticateUserCommand, AuthenticateUserCommandResponse]):
    def __init__(
        self,
        user_repository: UserRepository,
        token_service: TokenService,
        _logger: Logger = logger,
    ) -> None:
        self._user_repository = user_repository
        self._token_service = token_service
        self._logger = _logger

    async def execute(self, command: AuthenticateUserCommand) -> AuthenticateUserCommandResponse:
        command_id = command.command_id
        self._logger.info(f"Command {command_id}: AuthenticateUserCommandHandler#execute")

        email = self._token_service.verify(command.token)
        user = await self._user_repository.find_by_email(email)
        if user is None or not user.is_active:
            self._logger.info(f"Command {command_id}: token subject not authenticable")
            raise InvalidTokenException("Invalid or expired token")

        return AuthenticateUserCommandResponse(user)

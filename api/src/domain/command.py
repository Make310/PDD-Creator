import uuid
from abc import ABC, abstractmethod
from typing import Any


class Command:
    def __init__(self) -> None:
        self.command_id = uuid.uuid4()


class CommandResponse(ABC):
    @abstractmethod
    def message(self) -> Any:  # noqa: ANN401
        raise NotImplementedError


class CommandHandler[C: Command, R: CommandResponse](ABC):
    @abstractmethod
    def execute(self, command: C) -> R:
        raise NotImplementedError


class AsyncCommandHandler[C: Command, R: CommandResponse](ABC):
    @abstractmethod
    async def execute(self, command: C) -> R:
        raise NotImplementedError

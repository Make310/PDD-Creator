from collections.abc import Coroutine
from typing import Any


def resolved[T](value: T) -> Coroutine[Any, Any, T]:
    """Wrap a value in a single-use awaitable, so doublex stubs can mimic async methods."""

    async def _coro() -> T:
        return value

    return _coro()

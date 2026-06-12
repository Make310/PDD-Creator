# Clean Architecture

## Convention

Each backend module (`api/`, `worker/`) follows hexagonal architecture with strict unidirectional dependencies.

```
delivery/ → use_cases/ → domain/ ← infrastructure/
                              ↑
                           common/
```

| Layer | Location | Rules |
|-------|----------|-------|
| `domain/` | Ports (ABCs), exceptions, `Command`/`CommandHandler`/`CommandResponse` base | Zero framework imports |
| `use_cases/` | One `CommandHandler` per operation. Orchestrates domain via injected interfaces | No concrete implementations |
| `infrastructure/` | Concrete implementations of domain interfaces | Framework and library aware |
| `delivery/` | Entry points (FastAPI routers, worker queue consumers). Translates input → Command → response | No business logic |
| `common/` | `logger`, `settings` | Accessible from all layers |

## Composition root

`main.py` at the module root builds the FastAPI app (lifespan, settings, routers). Each delivery
feature lives in `src/delivery/api/v1/<feature>/` with two files:

- `<feature>_router.py` — `APIRouter` + DI wiring
- `<feature>_response.py` — Pydantic response model (response models belong to delivery, never to domain)

## Command pattern

Every operation follows the same structure:

```python
# 1. Command — input data
class GeneratePDDCommand(Command):
    def __init__(self, transcript: str, requested_by: str) -> None:
        self.transcript = transcript
        self.requested_by = requested_by
        super().__init__()  # assigns command_id for log correlation

# 2. CommandHandler — business logic
# The base is generic (PEP 695): CommandHandler[C: Command, R: CommandResponse].
# Parametrize it so narrowing the command type does not violate Liskov.
class GeneratePDDCommandHandler(CommandHandler[GeneratePDDCommand, GeneratePDDCommandResponse]):
    def __init__(self, publisher: PDDJobPublisher) -> None:
        self._publisher = publisher  # injected interface, not concrete class

    def execute(self, command: GeneratePDDCommand) -> GeneratePDDCommandResponse:
        ...

# 3. CommandResponse — output data
class GeneratePDDCommandResponse(CommandResponse):
    def message(self) -> str:
        return self._job_id
```

## Dependency injection

FastAPI `Depends` (in routers) and manual wiring (in the worker's queue consumer) are the **only places** where abstract meets concrete.

```python
# ✅ delivery layer wires the dependency
async def generate_pdd_command_handler(
    publisher: PDDJobPublisher = Depends(pdd_job_publisher),
) -> GeneratePDDCommandHandler:
    return GeneratePDDCommandHandler(publisher)

# ❌ handler instantiates its own dependency
class GeneratePDDCommandHandler(CommandHandler[GeneratePDDCommand, GeneratePDDCommandResponse]):
    def __init__(self) -> None:
        self._publisher = RedisPDDJobPublisher()  # wrong
```

In tests, swap the wiring without touching the app:

```python
app.dependency_overrides[generate_pdd_command_handler] = stubbed_handler_provider
```

## Module boundaries

See [architecture.md](../architecture.md) for inter-module rules (`api/` vs `worker/`).

## Benefits

- Domain logic is framework-agnostic and independently testable
- Infrastructure can be swapped without touching business logic
- Each layer has a single, clear responsibility

## Related

- [code-style.md](code-style.md)
- [test-structure.md](testing/test-structure.md)

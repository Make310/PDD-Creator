# Test Structure

## Convention

Tests are split into three independent tiers. Each tier has a specific scope, speed, and set of allowed dependencies.

| Tier | Location | Scope | External services | When it runs |
|------|----------|-------|-------------------|--------------|
| **Unit** | `tests/unit/` | `CommandHandler` logic in isolation | None — all dependencies stubbed with doublex | Pre-commit |
| **Integration** | `tests/integration/` | Infrastructure adapters against real services | Real (MongoDB, Redis, Claude API) | Pre-push |
| **Acceptance** | `tests/acceptance/` | HTTP endpoints or worker consumers end-to-end | None — FastAPI `TestClient` or invoking the consumer with stubbed adapters | Pre-push |

## Layout

Test files mirror the `src/` structure exactly:

```
src/use_cases/generate_pdd_command.py
  → tests/unit/use_cases/test_generate_pdd_command.py

src/infrastructure/queue/pdd_job_publisher.py
  → tests/integration/queue/test_pdd_job_publisher.py

src/delivery/api/v1/pdd/pdd_router.py
  → tests/acceptance/delivery/api/test_pdd_controller.py
```

## Unit test example

```python
class TestGeneratePDDCommandHandler:
    def test_execute_returns_job_id(self) -> None:
        command = GeneratePDDCommand(transcript="text", requested_by="user@example.com")
        with Mimic(Stub, RedisPDDJobPublisher) as publisher:
            publisher.publish(command).returns(None)

        handler = GeneratePDDCommandHandler(publisher)  # type: ignore
        response = handler.execute(command)

        expect(response.message()).to(be_a(str))
```

## Running tests

```bash
make test-unit          # fast, runs on every commit
make test-integration   # requires real services
make test-acceptance    # requires app running or TestClient
make test               # all three tiers
```

## Acceptance error-path example

Error paths don't need real failures — override the DI provider with a stubbed handler via
`app.dependency_overrides`. No external service is involved, so it stays in the acceptance tier:

```python
class TestGeneratePDDControllerErrors:
    ERROR_MESSAGE = "any error message"

    def _failing_handler(self) -> GeneratePDDCommandHandler:
        with Mimic(Stub, GeneratePDDCommandHandler) as handler:
            handler.execute(ANY_ARG).raises(GeneratePDDCommandHandlerException(self.ERROR_MESSAGE))
        return handler  # type: ignore

    def test_returns_bad_request(self) -> None:
        client = TestClient(app)
        app.dependency_overrides[generate_pdd_command_handler] = self._failing_handler

        response = client.post(f"{settings.api_v1_prefix}/pdd", json={"transcript": "..."})

        expect(response.status_code).to(equal(BAD_REQUEST))
        expect(response.json()).to(equal({"detail": self.ERROR_MESSAGE}))
```

## Anti-patterns

- ❌ Unit test calling a real database or HTTP endpoint — move to integration
- ❌ Using `unittest.mock.MagicMock` — use `doublex` `Mimic(Stub, ConcreteClass)`
- ❌ Acceptance test hitting real external services — use `TestClient` or stubs

## Related

- [test-doubles.md](test-doubles.md)
- [clean-architecture.md](../clean-architecture.md)

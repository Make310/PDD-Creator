# Test Doubles

## Convention

Use `doublex` with `Mimic(Stub, ConcreteClass)` for all unit test stubs. Never use `unittest.mock`.

## Basic stub

```python
from doublex import Mimic, Stub
from expects import equal, expect

with Mimic(Stub, ServiceBusPDDJobPublisher) as publisher:
    publisher.publish(job).returns(None)

handler = GeneratePDDCommandHandler(publisher)  # type: ignore
response = handler.execute(command)

expect(response.message()).to(equal(expected_job_id))
```

## Stub raising an exception

```python
with Mimic(Stub, ServiceBusPDDJobPublisher) as publisher:
    publisher.publish(job).raises(PDDJobPublisherException("timeout"))

expect(lambda: handler.execute(command)).to(raise_error(GeneratePDDCommandHandlerException))
```

## Rules

- Use `Mimic(Stub, ConcreteClass)` — the stub conforms to the real interface; type mismatches are caught at creation time
- Configure behavior inside the `with` block before passing the stub to the handler
- Use `expects` for assertions (BDD style: `expect(x).to(equal(y))`)
- Pass `# type: ignore` when injecting a stub where a concrete type is expected

## Benefits

- Stubs are interface-bound — a method rename in the real class breaks the stub immediately
- No silent `MagicMock` — every stubbed call must be declared explicitly
- Tests document the expected interaction, not just the result

## Related

- [test-structure.md](test-structure.md)

# Code Style

## Convention

All Python code follows these rules, enforced by `ruff` and `ty`.

**Line length:** 120 characters

**Type annotations:** Mandatory on all public and private functions — arguments and return types.

```python
# ✅
def get(self, name: str) -> str:

# ❌
def get(self, name):
```

**Logging:** Use `logger` from `src/common/logger.py` — where `src/` is relative to each module root (`api/src/` or `worker/src/`). `print()` is banned.

```python
# ✅
from src.common.logger import logger  # run from api/ or worker/
logger.info(f"Command {command_id}: processing started")

# ❌
print("processing started")
```

**Exceptions:** Custom classes only — never bare `Exception`. Always re-raise with `from`.

```python
# ✅
class PDDJobPublisherException(Exception):
    pass

try:
    self._publisher.publish(job)
except PDDJobPublisherException as ex:
    raise GeneratePDDCommandHandlerException(str(ex)) from ex

# ❌
raise Exception("something failed")
```

**Imports:** No unused imports. Remove any import whose symbol is not referenced.

## Benefits

- Consistent code across modules and contributors
- Type errors caught before runtime
- Structured logs searchable in the log aggregator (decided with the deployment target)

## Running checks

```bash
make checks    # lint + format + type check
make format    # auto-fix formatting
```

## Related

- [clean-architecture.md](backend/clean-architecture.md)
- [test-structure.md](testing/test-structure.md)

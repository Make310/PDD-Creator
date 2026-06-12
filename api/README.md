# PDD Creator — API

FastAPI BFF: the only HTTP entry point of the system. Handles authentication, receives transcript
submissions, and serves PDD results from MongoDB. See [docs/architecture.md](../docs/architecture.md).

## Setup

```bash
make install   # installs Python 3.12.8 and dependencies via uv
make dev       # runs the app in development mode
```

## Quality

```bash
make checks            # lint + format + type check
make test              # unit + integration + acceptance
make help              # all available targets
```

Conventions: [docs/backend/](../docs/backend/)

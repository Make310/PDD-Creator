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

## Creating the first admin

There is no public registration endpoint — the first admin user is created with the
`create_admin` CLI. The password is never passed as a command-line argument: it is read from
the `ADMIN_PASSWORD` environment variable or prompted interactively.

Pick the target that targets the **same MongoDB the running API reads**, otherwise login will
return 401 (the admin lands in a different database than the one the API queries):

| Scenario | Command | MongoDB it writes to |
|----------|---------|----------------------|
| Local dev (API run with `make dev`) | `make create-admin email=admin@x.com name="Admin"` | The host mongo at `MONGODB_URI` for your shell (defaults to `mongodb://localhost:27017`) |
| Docker Compose stack (API run with `docker compose up`) | `make create-admin-docker email=admin@x.com name="Admin"` | The compose mongo (`mongodb://mongodb:27017`), the same DB the dockerized API reads |

`create-admin-docker` runs the CLI **inside the running API container**
(`docker compose exec api python -m src.delivery.cli.create_admin ...`), so it always uses the
container's `MONGODB_URI`. Provide the password without leaking it into the shell history:

```bash
# Prompted interactively (a TTY is allocated automatically):
make create-admin-docker email=admin@x.com name="Admin"

# Or from the environment (forwarded into the container, never as a CLI arg):
ADMIN_PASSWORD=your-password make create-admin-docker email=admin@x.com name="Admin"
```

> The Compose stack must already be running (`docker compose up`) before invoking
> `create-admin-docker`.

Conventions: [docs/backend/](../docs/backend/)

# PDD Creator

Converts RPA process transcripts into structured Process Design Documents (PDD) using AI.

## Requirements

| Tool | Needed for |
|------|-----------|
| [Docker Desktop](https://docs.docker.com/get-docker/) | Running the stack and the local infrastructure (MongoDB, Redis) |
| [uv](https://docs.astral.sh/uv/getting-started/installation/) | Developing `api/` natively (installs Python 3.12.8 by itself) |
| Node 24+ | Developing `frontend/` natively |

## First-time setup

```bash
make setup                    # installs the git hooks (lint + tests on commit/push)
cd api && make install        # Python 3.12.8 + dependencies via uv
cd frontend && make install   # npm dependencies
```

The module installs are only needed if you plan to develop natively. To just run the app, Docker is enough.

## Running the project

### Option A — full stack in Docker

```bash
make up      # builds and starts MongoDB + Redis + api + frontend
make down    # stops everything (MongoDB data persists in a volume)
make logs    # follow container logs
```

| Service | URL |
|---------|-----|
| Frontend (SPA) | http://localhost:3000 |
| API | http://localhost:8000 — health: `/api/v1/health`, docs: `/openapi.json` |
| MongoDB | `mongodb://localhost:27017` |
| Redis | `redis://localhost:6379` |

> ⚠️ **No hot-reload in Docker.** Code is copied into the images at build time — after changing
> code, rebuild the affected service: `docker compose up -d --build api` (or `frontend`).
> Use Option B while developing.

### Option B — development mode (hot-reload)

Run only the infrastructure in Docker and the module you are working on natively:

```bash
make infra-up                 # MongoDB + Redis in Docker
cd api && make dev            # FastAPI with auto-reload on http://localhost:8000
cd frontend && make dev       # Vite with HMR on http://localhost:5173 (proxies /api to :8000)
make infra-down               # stop MongoDB + Redis when done
```

Save a file and the change is live — uvicorn restarts on `.py` changes, Vite hot-swaps the browser.

## Day-to-day commands

Every module exposes the same Make targets (run them inside `api/` or `frontend/`; `make help` lists all):

| Command | What it does |
|---------|--------------|
| `make checks` | Lint + format check + type check |
| `make test` | Full test suite (api: unit + integration + acceptance) |
| `make format` / `make lint` | Auto-fix format / lint issues |
| `make dev` | Run with hot-reload |

From the repo root, `make checks` and `make test` run them across all scaffolded modules.

## Quality gates

- **pre-commit hook:** checks + unit tests of the modules you touched
- **pre-push hook:** integration + acceptance tests
- **CI (GitHub Actions):** per-module workflows run checks, tests and build on every push/PR that touches the module

## Project structure

| Folder | Purpose |
|--------|---------|
| `frontend/` | Vite SPA — user interface. Allows analysts to upload transcripts and read generated PDDs. Static hosting (target TBD). |
| `api/` | FastAPI BFF — the only HTTP entry point. Handles authentication, receives transcript submissions, and serves PDD results from MongoDB. Runs as a Docker container. |
| `worker/` | Python worker — async processor. Consumes jobs from a Redis queue, calls the Claude API (Anthropic), generates the PDD sections, and persists events and artifacts to MongoDB. |
| `contracts/` | OpenAPI and AsyncAPI schemas. Source of truth for the interface between `api/` and `worker/`. Validated in CI to prevent contract drift. |
| `infra/` | Terraform — provisions cloud resources once a provider is selected (see `docs/infra/conventions.md`). Local development uses Docker Compose for MongoDB and Redis. |
| `scripts/` | Developer tooling. `local-setup.sh` configures git hooks. Hooks enforce lint, type checks, and tests before commit and push. |
| `docs/` | Architecture diagrams, coding conventions, and testing guidelines. Read by developers and AI agents before implementing features. |
| `progress/` | SDD workflow state. Tracks the active implementation session, reviewer verdicts, and session history. Used by the Claude agent harness — not deployed. |

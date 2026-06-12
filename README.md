# PDD Creator

Converts RPA process transcripts into structured Process Design Documents (PDD) using AI.

## Quick start

```bash
make setup       # git hooks
make up          # full stack in Docker: MongoDB + Redis + api (http://localhost:8000)
make infra-up    # only MongoDB + Redis, to run modules natively (cd api && make dev)
make down        # stop everything
```

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

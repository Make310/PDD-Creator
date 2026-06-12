# Current state

**Last updated:** 2026-06-12
**Active issue:** none
**State:** clean slate — awaiting first spec

## Next step

Create and approve the first spec Issue (`/specs` to list approved ones).

## Session notes

- Stack: Python + Claude API (Anthropic SDK, default model `claude-opus-4-8`), Redis queue, MongoDB, deployment TBD
- `api/` base scaffolded from `python-api-boilerplate` (hexagonal, uv, ruff, ty, pytest/doublex/expects)
- `frontend/` base scaffolded: Vite + React + TS, ESLint/Prettier/Vitest, nginx Docker image wired
  into the compose stack (port 3000, proxies /api to the api container)
- Issue #2 was a test spec — closed and discarded

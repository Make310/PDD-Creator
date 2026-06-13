# Review — Issue #3 (round 2 retry)

**Date:** 2026-06-12
**Reviewer verdict:** APPROVED

Scope: verify ONLY the two round-2 required changes from `progress/feedback_issue_3.md`.

## Change 1 — Login is the primary landing view, scaffold removed (frontend)

- [x] `frontend/src/App.tsx` renders only `AuthPanel`, centered as the focused primary
      content (`min-h-screen` flex, `max-w-md`). No marketing heading, no
      "Convert RPA process transcripts…" paragraph, no `HealthIndicator`.
- [x] Unauthenticated → login form (`AuthPanel` maps `unauthenticated` → `LoginForm`).
- [x] Authenticated → `UserProfileCard` (email, name, role) + Log out.
- [x] No dead code / unused imports: `HealthIndicator.tsx`, `useHealth.ts`,
      `healthService.ts` and their tests deleted. `grep` over `src`/`tests` finds no
      references except a test description string in `App.test.tsx` (not code).
- [x] `frontend/tests/App.test.tsx` added: asserts login is the landing view, the
      scaffold paragraph and API online/offline indicator are absent, and authenticated
      shows profile + logout.

## Change 2 — Admin creation targets the running dockerized stack (api + docs)

- [x] `api/Makefile` adds `create-admin-docker` running the CLI inside the running API
      container via `docker compose exec`. Password is never a CLI arg: `-e ADMIN_PASSWORD`
      when set, else `-it` for the existing `getpass` prompt.
- [x] `api/README.md` "Creating the first admin" section documents both paths in a table
      and which DB each writes to (host mongo vs compose `mongodb://mongodb:27017`),
      addressing the DB-mismatch 401 the user hit.
- [x] Round-2 commits (035e7cf, 58967b2) touched only frontend App/health files/tests and
      `api/Makefile` + `api/README.md`. Auth logic, login/me endpoints,
      `create_admin.py` CLI and `.github/workflows/api.yml` are unchanged.

## Verification runs

- frontend `make checks` → eslint + prettier + tsc OK
- frontend `make test` → 4 files, 20 passed
- frontend `npm run build` → tsc -b + vite build OK
- api `make checks` → ruff lint + format + ty OK
- api `make test` → unit 22, integration 3, acceptance 9 — all passed

## Note (not blocking)

The api `/health` endpoint and its unit/acceptance tests remain. This is correct: the
feedback scoped health removal to the frontend landing only; the api health endpoint was
never in the change list.

**Verdict: APPROVED** — both round-2 changes implemented exactly, all suites green, no dead
code or unused imports introduced.

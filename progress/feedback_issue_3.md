# Feedback — Issue #3 (PR #4 denied by user — round 2)

**Date:** 2026-06-12
**Source:** User denied PR #4 again (final word → CHANGES_REQUESTED, AGENTS.md rule 7)

Round 1 (frontend login + CI mongo service) is merged into the branch and CI is green.
This round addresses two NEW problems the user found while testing. Apply exactly the
changes below; do not touch anything outside this list.

## Root cause already diagnosed by the leader (read before coding)

The user reported "login does not work" with admin@test.com / 123456. The **backend auth
code is correct** — the leader reproduced it end to end and login returns 200 with a token.

The real cause was an environment/DB mismatch:
- The API runs in docker-compose and reads `mongodb://mongodb:27017` (the compose mongo).
- `make create-admin` runs on the **host** against `mongodb://localhost:27017`, which on this
  machine hit a *separate* local `mongod` — so the admin was written to a different database
  than the one the running API reads. Result: API `find_by_email` returns None → 401.

The leader unblocked the user by creating the admin inside the running API container
(`docker compose exec api python -m src.delivery.cli.create_admin ...`) and login then worked.

## Required change 1 — Login must be the primary view, drop the scaffold message (frontend)

The initial view still shows the boilerplate scaffold: the "PDD Creator … Convert RPA process
transcripts…" heading plus the `HealthIndicator` ("API active") block, with the login panel
tacked on below. The user expects the app to **open on the login experience**.

In `frontend/`:
- When the user is **unauthenticated**, the landing view is the login form as the primary,
  focused content — not a secondary panel under a marketing/health scaffold.
- Remove the `HealthIndicator` ("API active") from the user-facing landing. If a health check
  is still wanted, it must not be the home screen content. (`HealthIndicator`/`useHealth`/
  `healthService` may be deleted if they become unused — no dead code, no unused imports.)
- When **authenticated**, show the app shell with the user's profile (email, name, role) and
  logout, as already built.
- Update `App` and its tests (`tests/`) to reflect the new structure. Keep `make checks`,
  `make test` and `npm run build` green in `frontend/`.

## Required change 2 — Admin creation must target the running (dockerized) stack (api + docs)

The "create the first admin without the API" path currently only works against a host mongo,
which silently mismatches the compose deployment (that is what bit the user). Make the
correct path obvious and documented:
- Add a make target in `api/Makefile` to create the admin **inside the running API
  container**, e.g. `create-admin-docker` running
  `docker compose exec -e ADMIN_PASSWORD=... api python -m src.delivery.cli.create_admin
  --email ... --name ...` (do NOT pass the password as a CLI arg — keep using ADMIN_PASSWORD/
  prompt, consistent with the existing CLI).
- Document in `api/README.md` (or the root README) both ways: host/local-dev vs the
  docker-compose stack, making explicit which database each one writes to, so the admin is
  always created in the DB the running API reads.
- Do NOT change the auth logic, the login/me endpoints, the existing `create_admin.py` CLI
  behavior, or the api CI workflow.

## Out of scope (unchanged from spec)

Registration/management endpoints, refresh tokens, password reset, email verification, SSO.

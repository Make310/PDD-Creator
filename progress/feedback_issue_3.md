# Feedback — Issue #3 (PR #4 denied by user)

**Date:** 2026-06-12
**Source:** User denied PR #4 (final word → treated as CHANGES_REQUESTED, AGENTS.md rule 7)

The reviewer had approved and the PR was created, but the user denied it for two reasons.
Apply exactly the changes below. Do not touch anything outside this list.

## Required change 1 — Frontend login was not developed (implementer)

The backend auth API is complete, but the `frontend/` only has the scaffold
(`HealthIndicator`). The spec states the token is "a session credential the **frontend**
can send on subsequent requests" — the user requires the matching frontend.

Build the authentication UI in `frontend/` following `docs/frontend/architecture.md`
(components → hooks → services), `docs/frontend/code-style.md` and
`docs/frontend/testing.md`. It must cover the same acceptance criteria from the API side:

- **Login form**: email + password fields with client-side validation for missing/malformed
  fields (matches "Request with missing or malformed fields → validation error").
- **Auth service**: `POST /api/v1/auth/login` with `{ email, password }`. On success the
  response is `{ access_token, token_type: "bearer", expires_in }` (`expires_in` in seconds).
  Calls go through the nginx `/api` proxy already wired in the compose stack.
- **Token handling**: persist the token, attach it as `Authorization: Bearer <token>` on
  subsequent requests, and treat its expiration (`expires_in`) — expired/absent token must
  send the user back to login (matches "expired token rejected").
- **Generic login error**: on `401` show a single generic message ("Invalid credentials").
  Do NOT reveal whether the email exists, the password is wrong, or the user is deactivated.
- **Authenticated view**: after login, call `GET /api/v1/auth/me`
  (`Authorization: Bearer <token>`) and render the user's basic info (email, name, role).
- **Logout**: clear the stored token and return to the login view.
- **Tests** (Vitest + Testing Library, per `docs/frontend/testing.md`): cover successful
  login, generic error on bad credentials, validation of missing fields, and that the
  authenticated view shows the user info from `/me`.

Acceptance for this change: `make checks`, `make test` and `npm run build` all green in
`frontend/`.

## Required change 2 — CI was red (handled by leader, do not redo)

`api — checks and tests / build` failed because `make test` runs the integration tier, which
needs a real MongoDB at `localhost:27017`, and the `api.yml` workflow did not start one.
The leader added a `mongo` service container to `.github/workflows/api.yml`. No code change
was needed (the integration test reads `settings.mongodb_uri`, default `localhost:27017`).
**Implementer: do not modify the api workflow or the integration tests for this.**

## Out of scope (unchanged from spec)

Registration/management endpoints, refresh tokens, password reset, email verification, SSO.

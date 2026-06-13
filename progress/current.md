# Current state

**Last updated:** 2026-06-12
**Active issue:** #3 — [SPEC] User authentication with login
**State:** PR #4 DENIED by user — round 2 (PR #4 still open; new commits update it).
https://github.com/Make310/PDD-Creator/pull/4

## Round 2 denial reasons (see progress/feedback_issue_3.md)

1. Login "didn't work" with admin@test.com/123456 → **diagnosed: DB mismatch, not a code bug.**
   A stray host `mongod` on :27017 meant `make create-admin` (host) wrote to a different DB
   than the dockerized API reads (compose mongo). Leader created the admin inside the API
   container → login verified 200 w/ token. Durable fix queued: compose-aware create-admin + docs.
2. Initial view still shows the boilerplate scaffold (HealthIndicator "API active") instead of
   opening on login → frontend must make login the primary landing view.

## Round 1 (resolved, on branch)

- Frontend login UI built (commit ae64269). CI mongo service added (commit 5ad1bab). Both
  workflows green. Reviewer APPROVED round 1.

## Next step

All CHANGES_REQUESTED items resolved. **Waiting for user to merge PR #4.**
On merge → `gh issue close 3 --comment "Implemented in PR #4"`, append to history.md, clear current.md.

## CHANGES_REQUESTED cycle — resolved

1. (done) Leader fixed CI: mongo:7 service in api.yml → api workflow green.
2. (done) Implementer built frontend login UI (commit ae64269): login form + validation,
   auth service on /api/v1/auth/login, token persistence + Bearer header, expiry → re-login,
   generic 401 error (no enumeration), /me authenticated view, logout, 21 frontend tests.
3. (done) Reviewer: APPROVED -> progress/review_issue_3.md.
4. (done) Both CI workflows green on PR #4: api ✅ + frontend ✅ (runs 27453632694 / 27453632686).

## Flow log

- Implementer: done -> progress/impl_issue_3.md (branch `feat/issue-3`, pre-push hook green)
- Reviewer: APPROVED -> progress/review_issue_3.md
- Tests: 22 unit / 3 integration / 9 acceptance, `make checks` clean

## Session notes

- Spec #3 verified: `spec-approved` label present, no open questions
- Branch expected: `feat/issue-3`
- Key criteria: login with email/password → token (60 min), generic error for unknown
  email / wrong password / deactivated user, protected endpoint with user info,
  reject missing/invalid/expired token, CLI/script way to create first admin,
  passwords never in plain text
- Out of scope: registration/management endpoints, refresh tokens, password reset,
  email verification, SSO
- Stack: Python + Claude API (Anthropic SDK, default model `claude-opus-4-8`), Redis queue, MongoDB, deployment TBD
- `api/` base scaffolded from `python-api-boilerplate` (hexagonal, uv, ruff, ty, pytest/doublex/expects)
- `frontend/` base scaffolded: Vite + React + TS, ESLint/Prettier/Vitest, nginx Docker image wired
  into the compose stack (port 3000, proxies /api to the api container)

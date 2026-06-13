# Current state

**Last updated:** 2026-06-12
**Active issue:** #3 — [SPEC] User authentication with login
**State:** PR #4 DENIED by user → CHANGES_REQUESTED cycle in progress (PR #4 still open,
new commits to `feat/issue-3` update it). https://github.com/Make310/PDD-Creator/pull/4

## Denial reasons (see progress/feedback_issue_3.md)

1. Frontend login UI was never developed → relaunching implementer for `frontend/` auth.
2. `api — checks and tests` red: integration tier needs MongoDB, workflow had no service.
   → Leader added a `mongo:7` service to `.github/workflows/api.yml` (config, no code change).

## Next step

1. (done) Leader fixed CI: mongo service in api.yml.
2. Relaunch implementer for the frontend auth UI (feedback_issue_3.md, change 1).
3. Reviewer on the frontend work.
4. Confirm both CI workflows green on PR #4, then report to user for merge.

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

# Review — Issue #3 (retry: Required change 1, frontend login)

**Date:** 2026-06-12
**Reviewer verdict:** APPROVED
**Scope:** Required change 1 only (frontend auth UI). Required change 2 (CI mongo service)
handled by the leader and out of scope for this review.

## Acceptance criteria (from feedback_issue_3.md, Required change 1)

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Login form: email + password with client-side validation (missing + malformed) | OK | `src/components/LoginForm.tsx` + `src/hooks/useLogin.ts` `validate()` with `EMAIL_PATTERN`; per-field errors rendered. No service call when invalid. |
| Auth service `POST /api/v1/auth/login` mapping `{access_token, token_type, expires_in}` | OK | `src/services/authService.ts` `login()` posts JSON to relative `/api/v1/auth/login` (nginx/vite proxy) and maps to `{accessToken, expiresIn}`. |
| Token persisted, sent as `Authorization: Bearer`, expiration honored; expired/absent → login | OK | `src/services/tokenStorage.ts` stores absolute `expiresAt`, `readToken()` returns null + clears on absent/expired/corrupted. `fetchProfile()` sends bearer header. `useAuth` restores on mount and drops session on `/me` failure. |
| Generic message on 401, no user enumeration | OK | `login()` throws `InvalidCredentialsError` on 401; `useLogin` shows single "Invalid credentials" form-level `role="alert"`. No field-specific leak. |
| Authenticated view calls `GET /api/v1/auth/me`, renders email/name/role | OK | `useAuth.loadProfile` -> `fetchProfile`; `src/components/UserProfileCard.tsx` renders name, email, role. |
| Logout clears token, returns to login | OK | `useAuth.logout` clears token + resets status; `AuthPanel` maps `unauthenticated` -> `LoginForm`. |
| Tests: success login, generic error, missing-field validation, authenticated view shows /me | OK | `tests/components/AuthPanel.test.tsx` (7 tests incl. malformed email, session restore, logout), `tests/services/authService.test.ts` (5), `tests/services/tokenStorage.test.ts` (5). |

## Architecture / style compliance

- Layering respected: only `services/` call `fetch`; hooks consume services; components consume hooks. (docs/frontend/architecture.md)
- No `any`, explicit types and prop interfaces; no inline styles; brand `company-*` tokens only (all referenced tokens exist in `src/index.css`). (docs/frontend/code-style.md)
- Tests mock at the service boundary, assert visible behavior via roles/labels, use `findBy*` for async; `tests/setup.ts` runs `cleanup()`. (docs/frontend/testing.md)
- No unused exports/imports or dead code (ESLint clean; `Credentials`, `LoginResult`, `UserProfile`, `UnauthorizedError` all consumed). No new dependencies added.

## Verification results (frontend/)

```
make checks   -> eslint OK, prettier OK, tsc -b OK
make test     -> 5 files, 21 passed (AuthPanel 7, authService 5, tokenStorage 5, + existing health)
npm run build -> tsc -b + vite build OK (built in ~446ms)
```

## Verdict

APPROVED — all Required change 1 acceptance criteria are covered, layering and style docs
respected, no dead code or unused dependencies, and `make checks` / `make test` / `npm run build`
are all green in `frontend/`.

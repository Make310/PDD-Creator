# Review: User authentication with login
**Issue:** #3
**Branch:** feat/issue-3
**Date:** 2026-06-12
**Verdict:** APPROVED

## Acceptance criteria verification

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Active user logs in and receives a token | Covered | `LoginCommandHandler` + `POST /api/v1/auth/login`; unit `test_execute_returns_token_for_active_user_with_valid_credentials`, acceptance `test_login_returns_token_for_valid_credentials` |
| Same generic error for unknown email / wrong password / deactivated user | Covered | Single `InvalidCredentialsException` path mapped to one `401 {"detail": "Invalid credentials"}` in `auth_router.py`; three unit tests (one per case) + acceptance test. Identical by construction (one exception, one handler, one detail constant) |
| Protected endpoint returns email, name, role | Covered | `GET /api/v1/auth/me` returns `UserResponse(email, name, role)`; acceptance `test_me_returns_authenticated_user_info` |
| No token / invalid / expired token rejected | Covered | `authenticated_user` dependency (HTTPBearer + `AuthenticateUserCommandHandler`); acceptance tests for missing, garbage and real expired JWT (expired test exercises the real JWT service through the real dependency chain) |
| First admin created without the API | Covered | `api/src/delivery/cli/create_admin.py` + `make create-admin`; use case unit-tested (`test_create_admin_user_command.py`); password via prompt or `ADMIN_PASSWORD` env var, never argv |
| Passwords never stored or logged in plain text | Covered | `BcryptPasswordHasher` (hash on create, verify on login); unit test asserts hash never contains plain text; log statements only emit command ids, role and email |

## Edge cases verification

| Edge case | Status | Evidence |
|-----------|--------|----------|
| Missing or malformed fields → validation error | Covered | `LoginRequest` (EmailStr, min_length=1); acceptance tests for empty body and malformed email → 422 |
| Expired or tampered token → rejected | Covered | Unit tests: expired, tampered, foreign secret, no subject, garbage; acceptance: expired real JWT → 401 |
| Deactivated user with correct password → same generic error | Covered | Unit `test_execute_rejects_deactivated_user_even_with_correct_password`; bonus: token of a user deactivated after issuing is also rejected |

## Design notes compliance

- Token lifetime 60 minutes: `auth_token_ttl_minutes = 60` in settings, `expires_in: 3600` asserted in tests
- Out-of-scope items (registration endpoints, refresh, reset, SSO) correctly not implemented

## Test and check results (run by reviewer)

```
make checks           -> ruff lint OK, ruff format OK (58 files), ty OK
make test-unit        -> 22 passed
make test-integration -> 3 passed (real MongoDB, isolated *_test database)
make test-acceptance  -> 9 passed
```

## Code quality

- Hexagonal layering respected: domain ports (`UserRepository`, `PasswordHasher`, `TokenService`) with infrastructure adapters; delivery wires DI via FastAPI `Depends`
- `AsyncCommandHandler` added alongside `CommandHandler` (open/closed, no modification of existing handler)
- New dependencies (`beanie`, `pyjwt`, `bcrypt`) are all used; no unused imports or dead code found
- Tests follow the three-tier structure and doublex `Mimic(Stub, ...)` conventions; `tests/support.py::resolved` is a reasonable shared helper for async stubbing

## Minor observations (non-blocking)

- `auth_secret_key` has an insecure dev default in settings and docker-compose fallback; acceptable for local dev since it is overridable via `AUTH_SECRET_KEY`, but production deployment must set it
- `UserDocument.updated_at` is set but never updated after insert; will become relevant when user-management endpoints arrive (out of scope here)

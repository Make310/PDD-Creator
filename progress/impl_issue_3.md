# Implementation: User authentication with login
**Issue:** #3
**Date:** 2026-06-12

## Modified files

Module: `api/` (hexagonal). New dependencies: `beanie` 2.1.0, `pyjwt` 2.13.0, `bcrypt` 5.0.0.

- `api/src/domain/user.py` — `User` entity + `UserRole` (admin/user)
- `api/src/domain/user_repository.py` — async `UserRepository` port + `UserRepositoryException`
- `api/src/domain/password_hasher.py` — `PasswordHasher` port
- `api/src/domain/token_service.py` — `TokenService` port + `AuthToken` value object
- `api/src/domain/exceptions.py` — `InvalidCredentialsException`, `InvalidTokenException`,
  `UserAlreadyExistsException`
- `api/src/domain/command.py` — added `AsyncCommandHandler` base (async use cases)
- `api/src/use_cases/login_command.py` — login; same generic error for unknown email,
  wrong password and deactivated user
- `api/src/use_cases/authenticate_user_command.py` — token → active user (rejects unknown
  or deactivated subjects, so a deactivated user's still-valid token stops working)
- `api/src/use_cases/create_admin_user_command.py` — first admin (active, hashed password,
  rejects duplicated email)
- `api/src/infrastructure/mongo/user_document.py` — Beanie `users` document (unique email
  index, role index) + domain mapping
- `api/src/infrastructure/mongo/mongo_user_repository.py` — `UserRepository` implementation
- `api/src/infrastructure/mongo/database.py` — `init_database` (Beanie init, wrapped errors)
- `api/src/infrastructure/security/bcrypt_password_hasher.py` — bcrypt hashing/verification
- `api/src/infrastructure/security/jwt_token_service.py` — HS256 JWT, TTL from settings
  (60 min), rejects expired/tampered/foreign-secret/no-subject tokens
- `api/src/delivery/api/v1/auth/` — `auth_router.py` (`POST /auth/login`, `GET /auth/me`),
  `auth_request.py`, `auth_response.py`, `auth_dependencies.py` (DI wiring + reusable
  `authenticated_user` dependency for any future protected endpoint)
- `api/src/delivery/cli/create_admin.py` — CLI to create the first admin without the API;
  password via interactive prompt or `ADMIN_PASSWORD` env var (never argv/history)
- `api/main.py` — auth router mounted; MongoDB initialized on startup (logs a warning and
  keeps serving if unavailable, so acceptance tests stay service-free)
- `api/src/common/settings.py` — `mongodb_uri`, `mongodb_database`,
  `mongodb_server_selection_timeout_ms`, `auth_secret_key`, `auth_token_ttl_minutes` (60)
- `api/Makefile` — `make create-admin email=... name="..."` target
- `docker-compose.yml` — api service gets `MONGODB_URI` and `AUTH_SECRET_KEY`
- Tests: `api/tests/unit/use_cases/` (3 files), `api/tests/unit/infrastructure/security/`
  (2 files), `api/tests/integration/mongo/test_mongo_user_repository.py`,
  `api/tests/acceptance/delivery/api/test_auth_controller.py`, `api/tests/support.py`
  (helper to stub async methods with doublex)

## Acceptance criteria covered

- [x] Active registered user logs in with valid credentials and receives a token
      (unit + acceptance + manual end-to-end)
- [x] Login fails with the same generic 401 `{"detail": "Invalid credentials"}` for unknown
      email / wrong password / deactivated user (unit tests per case + acceptance + manual
      check that responses are byte-identical)
- [x] Protected endpoint `GET /api/v1/auth/me` returns email, name, role
- [x] Calls without token / invalid token / expired token rejected with 401
- [x] First admin created without the API: `make create-admin` CLI (verified manually)
- [x] Passwords never stored or logged in plain text: bcrypt hash verified in Mongo
      (`$2b$12$...`, plain text absent), logs only contain command ids and emails

## Edge cases handled

- [x] Missing or malformed fields (empty body, invalid email) → 422 validation error
- [x] Expired token (real JWT issued with negative TTL) → 401; tampered token and token
      signed with another secret → rejected (unit); garbage token → 401 (acceptance)
- [x] Deactivated user with correct password → same generic login error
- [x] Token whose subject no longer exists or was deactivated after issuing → 401
- [x] Duplicate admin creation → clean error, exit code 1 (verified manually)
- [x] Malformed bcrypt hash in DB → verify returns False (no crash)
- [x] MongoDB down at startup → API still boots, logs warning

## How to test manually

1. `make infra-up` (root) — start MongoDB
2. `cd api && make create-admin email=admin@example.com name="Admin"` — type a password
   when prompted (or prefix with `ADMIN_PASSWORD=...`)
3. `make dev` — start the API
4. `curl -s -X POST localhost:8000/api/v1/auth/login -H 'Content-Type: application/json' \
   -d '{"email":"admin@example.com","password":"<password>"}'` → `access_token`,
   `token_type: bearer`, `expires_in: 3600`
5. `curl -s localhost:8000/api/v1/auth/me -H 'Authorization: Bearer <access_token>'` →
   `{"email":"admin@example.com","name":"Admin","role":"admin"}`
6. Repeat 4 with a wrong password and with an unknown email → identical
   `401 {"detail":"Invalid credentials"}`
7. Repeat 5 without header or with a garbage token → `401 {"detail":"Invalid or expired token"}`

## Test results

```
make checks          → ruff lint OK, ruff format OK, ty OK
make test-unit       → 22 passed
make test-integration → 3 passed (real MongoDB)
make test-acceptance → 9 passed (TestClient, no external services)
```

Manual end-to-end against real Mongo (TestClient with lifespan): login 200 + /me 200,
generic 401s identical for wrong password vs unknown email, no-token/garbage-token 401,
stored hash `$2b$12$...` with no plain text, duplicate admin exits 1. E2E database dropped
afterwards.

## Notes for the reviewer

- `AsyncCommandHandler` was added next to `CommandHandler` (open/closed) because Beanie is
  async; doublex stubs mimic async methods by returning a single-use awaitable
  (`tests/support.py::resolved`).
- Out of scope per spec: registration/management endpoints, refresh tokens, password reset,
  email verification, SSO.

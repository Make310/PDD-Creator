# Frontend Architecture

## Convention

The SPA follows a three-layer architecture with strict unidirectional dependencies — the frontend
mirror of the backend's hexagonal design:

```
components/ → hooks/ → services/
```

| Layer | Location | Responsibility | Rules |
|-------|----------|----------------|-------|
| `components/` | `src/components/` | Presentation: render data, capture user input | No `fetch`, no business logic. Get data from hooks or props. Local UI state only. |
| `hooks/` | `src/hooks/` | Stateful logic: loading/error/data state machines, orchestration | Call services, never `fetch` directly. Expose typed status + data to components. |
| `services/` | `src/services/` | API access — the **only** place `fetch()` is allowed | Typed request/response per endpoint. No React imports. |

Dependencies point one way: a service never imports a hook, a hook never imports a component.
`App.tsx` composes the pages; `main.tsx` is the entry point.

## Structure

```
frontend/src/
├── components/   # PascalCase.tsx — one component per file
├── hooks/        # useX.ts
├── services/     # xService.ts
├── App.tsx
└── main.tsx
```

Tests live in `frontend/tests/` mirroring `src/` — see [testing.md](testing.md).

## API access

- Code always calls **relative paths** (`/api/v1/...`) — never absolute URLs or env-dependent hosts.
- In development, Vite proxies `/api` to `http://localhost:8000` (`vite.config.ts`).
- In Docker, nginx proxies `/api/` to the `api` container (`nginx.conf`).

## Async state pattern

Every hook that loads data exposes an explicit status — components render all three states,
never just the happy path:

```tsx
export type HealthStatus = 'loading' | 'ok' | 'error'

// hook: translates service results/errors into the status enum
// component: Record<Status, ...> maps each state to its rendering
```

See `useHealth.ts` + `HealthIndicator.tsx` for the reference implementation.

## State management

Local state (`useState` / `useReducer`) lifted into hooks when shared or non-trivial.
No global state library (Redux, Zustand, etc.) unless justified in an ADR.

## Adding a feature

1. Service: typed function(s) for the new endpoint in `src/services/`
2. Hook: state machine consuming the service in `src/hooks/`
3. Component(s) rendering the hook's states in `src/components/`
4. Tests for each layer — see [testing.md](testing.md)

## Related

- [code-style.md](code-style.md)
- [testing.md](testing.md)
- [../architecture.md](../architecture.md) — system-level boundaries (frontend never calls `worker/`)

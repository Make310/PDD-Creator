# Frontend Testing

## Convention

Tests run with **Vitest** (jsdom environment) + **Testing Library**. They live in `frontend/tests/`,
mirroring the `src/` structure:

```
src/services/healthService.ts   → tests/services/healthService.test.ts
src/hooks/useHealth.ts          → (covered through its component)
src/components/HealthIndicator.tsx → tests/components/HealthIndicator.test.tsx
```

## What to test per layer

| Layer | Strategy | Mock boundary |
|-------|----------|---------------|
| Services | Call the function, assert the returned/thrown value | Stub `fetch` with `vi.stubGlobal()` |
| Hooks | Test through the component that uses them (preferred) or `renderHook` | Mock the service module with `vi.mock()` |
| Components | Render with Testing Library, assert visible behavior | Mock the service module with `vi.mock()` |

## Service test example

```ts
import { afterEach, describe, expect, it, vi } from 'vitest'
import { fetchHealth } from '../../src/services/healthService'

describe('fetchHealth', () => {
  afterEach(() => vi.unstubAllGlobals())

  it('returns true when the API responds ok', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: true, json: () => Promise.resolve({ ok: true }) }))

    expect(await fetchHealth()).toBe(true)
  })
})
```

## Component test example

```tsx
import { render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { HealthIndicator } from '../../src/components/HealthIndicator'
import { fetchHealth } from '../../src/services/healthService'

vi.mock('../../src/services/healthService')

it('shows API online when the health check succeeds', async () => {
  vi.mocked(fetchHealth).mockResolvedValue(true)

  render(<HealthIndicator />)

  expect(await screen.findByText('API online')).toBeDefined()
})
```

## Rules

- **Mock at the service boundary** — never mock hooks or components; never hit a real network.
- **Assert visible behavior** (text, roles, accessible attributes) — never class names, styles or
  internal state. Styling is covered by `make checks`, not by tests.
- **Use `findBy*` for async UI** — it awaits the state transition; `getBy*` is for synchronous content.
- Explicit imports from `vitest` (`describe`, `it`, `expect`, `vi`) — globals are not enabled.

## Running

```bash
make test     # full suite (CI and pre-commit hook run this)
make watch    # watch mode while developing
```

## Anti-patterns

- ❌ Snapshot tests — they assert markup, not behavior, and rot fast
- ❌ Asserting Tailwind classes or inline styles
- ❌ `fetch` reaching the real API in any test
- ❌ Testing a hook in isolation when a component test covers the same path

## Related

- [architecture.md](architecture.md)
- [code-style.md](code-style.md)

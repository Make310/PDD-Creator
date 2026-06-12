# Frontend Code Style

## Toolchain

- **Stack:** Vite + React + TypeScript, Node 24, npm
- **Lint:** ESLint (flat config, `eslint.config.js`) with `typescript-eslint`, `react-hooks` and `eslint-config-prettier`
- **Format:** Prettier (`.prettierrc` — no semicolons, single quotes)
- **Tests:** Vitest + Testing Library (`jsdom` environment)
- **Commands:** `make checks` (lint + format + types), `make test`, `make dev`, `make build` — same target names as the backend modules

## Structure

```
frontend/src/
├── components/   # PascalCase.tsx — one component per file
├── hooks/        # useX.ts — stateful logic, calls services
├── services/     # API access — the only place fetch() is allowed
├── App.tsx
└── main.tsx
```

Tests live in `frontend/tests/` mirroring `src/` (`tests/components/`, `tests/hooks/`, `tests/services/`).
Mock services with `vi.mock()` in component tests; stub `fetch` with `vi.stubGlobal()` in service tests.

In development, Vite proxies `/api` to `http://localhost:8000` (see `vite.config.ts`); in Docker,
nginx proxies `/api/` to the `api` container. Code always calls relative `/api/v1/...` paths.

## Convention

All TypeScript/React code follows these rules, enforced by ESLint and Prettier.

**Language:** TypeScript — no `any`, explicit types on all props and function signatures.

**Components:** Functional components only. One component per file. File name matches component name.

```tsx
// ✅
interface TranscriptUploadProps {
  onSubmit: (transcript: string) => void;
}

export function TranscriptUpload({ onSubmit }: TranscriptUploadProps) { ... }

// ❌
export default function(props: any) { ... }
```

**State management:** Local state with `useState` / `useReducer`. No global state library unless justified in an ADR.

**API calls:** Encapsulated in custom hooks or service modules — never inline in components.

```tsx
// ✅
const { data, isLoading } = usePDD(jobId);

// ❌
useEffect(() => {
  fetch(`/api/v1/pdd/${jobId}`).then(...);
}, []);
```

**Naming:**
- Components: `PascalCase`
- Hooks: `camelCase` prefixed with `use`
- Files: `PascalCase.tsx` for components, `camelCase.ts` for utilities and hooks

**No console.log** in production code — use a structured logger or remove before commit.

## Related

- [../architecture.md](../architecture.md)

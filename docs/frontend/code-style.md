# Frontend Code Style

## Toolchain

- **Stack:** Vite + React + TypeScript, Node 24, npm
- **Styling:** Tailwind CSS v4 (`@tailwindcss/vite` plugin) — see the Styling section below
- **Lint:** ESLint (flat config, `eslint.config.js`) with `typescript-eslint`, `react-hooks` and `eslint-config-prettier`
- **Format:** Prettier (`.prettierrc` — no semicolons, single quotes) + `prettier-plugin-tailwindcss` (sorts class names automatically)
- **Tests:** Vitest + Testing Library — see [testing.md](testing.md)
- **Commands:** `make checks` (lint + format + types), `make test`, `make dev`, `make build` — same target names as the backend modules

For folder structure and layer rules see [architecture.md](architecture.md).

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

## Styling — Tailwind + company brand

All styling is done with **Tailwind utility classes**. Rules:

1. **No inline `style=`** and **no new CSS files** — the only stylesheet is `src/index.css`, which holds
   the Tailwind import and the brand tokens (`@theme`). If a style can't be expressed with utilities,
   discuss it before adding custom CSS.
2. **Brand colors only through tokens.** Never hardcode hex values in components — use the
   `company-*` classes generated from `@theme`:

   | Token | Hex | Use for |
   |-------|-----|---------|
   | `company-yellow` | `#ffcc29` | Primary actions, accents, highlights (brand primary) |
   | `company-black` | `#000000` | Headings, primary text |
   | `company-blue` | `#003c78` | Corporate accents, links, emphasis on light backgrounds |
   | `company-cyan` | `#14b1e7` | Informational accents |
   | `company-gray-600` | `#616161` | Body text |
   | `company-gray-50..900` | neutral scale | Backgrounds, borders, muted text |

   Example: `bg-company-yellow text-company-black`, `text-company-gray-600`, `border-company-yellow`.
3. **Functional colors stay functional.** Success/error/warning states use Tailwind's semantic
   defaults (`green-*`, `red-*`, `amber-*`) — don't repurpose brand colors to signal state.
4. **Typography is Poppins** (`font-sans` is already mapped to it). Loaded via Google Fonts in `index.html`.
5. **Class order is enforced** by `prettier-plugin-tailwindcss` — run `make format` and don't fight it.
6. Reusable visual patterns belong in a **component**, not in copy-pasted class strings or `@apply`.

## Related

- [architecture.md](architecture.md)
- [testing.md](testing.md)
- [../architecture.md](../architecture.md)

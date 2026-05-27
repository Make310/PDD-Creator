# Frontend Code Style

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

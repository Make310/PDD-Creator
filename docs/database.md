# Database Design

**Engine:** MongoDB (Atlas or local Docker for development)  
**ODM:** Beanie (async, Pydantic v2) — Document models live in `infrastructure/`, never in `domain/`  
**Pattern:** Event Store + State documents  
**Rule:** Events are immutable — never update or delete, only append. State documents are the mutable projection the API reads.

---

## Collections

### `users`

Stores user accounts and roles.

```json
{
  "_id": "ObjectId",
  "email": "string (unique)",
  "password_hash": "string",
  "name": "string",
  "role": "admin | user",
  "is_active": "boolean",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

**Roles:**

| Role | Permissions |
|------|-------------|
| `user` | Create PDDs, read own PDDs and events |
| `admin` | Read all PDDs and events, manage users (activate/deactivate, change role) |

**Indexes:**
- `email` — unique, used on login
- `role` — used by admin queries

---

### `pdds` — state documents

One document per generation job. This is the projection the API serves to the frontend; it is created by `api/` and updated only by `worker/`.

```json
{
  "_id": "ObjectId",
  "job_id": "string (UUID, unique)",
  "status": "pending | processing | completed | failed",
  "requested_by": "string — user email",
  "transcript": "string — original Teams transcript",
  "pdd_markdown": "string | null — generated PDD in Markdown",
  "model": "string | null — Claude model that generated it (e.g. claude-opus-4-8)",
  "error": "string | null — human-readable failure reason",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

**Status transitions** (only forward, never back):

```
pending → processing → completed
                     → failed
```

**Artifacts:** transcript and generated PDD are stored inline — both are text and stay far below MongoDB's 16 MB document limit. No external blob storage is needed for now.

**Indexes:**
- `job_id` — unique, used by `GET /pdd/{job_id}`
- `requested_by` + `created_at` (desc) — "my PDDs" listing
- `status` — worker/admin monitoring queries

---

### `pdd_events` — event store

Append-only audit trail of everything that happened to a job.

```json
{
  "_id": "ObjectId",
  "job_id": "string (UUID)",
  "type": "string — event type, see table",
  "payload": "object — event-specific data",
  "occurred_at": "datetime"
}
```

**Event types:**

| Type | Written by | Payload |
|------|-----------|---------|
| `UserRequestedPDDEvent` | `api/` | `requested_by`, `transcript_chars` |
| `PDDProcessStartedEvent` | `worker/` | `attempt` (int, 1-based) |
| `PDDGeneratedEvent` | `worker/` | `model`, `input_tokens`, `output_tokens`, `duration_ms` |
| `AIProcessingFailedEvent` | `worker/` | `error_type`, `error_message`, `attempt` |

**Indexes:**
- `job_id` + `occurred_at` (asc) — replay a job's history in order
- `type` — admin/metrics queries

---

## Access patterns

| Operation | Module | Reads | Writes |
|-----------|--------|-------|--------|
| `POST /pdd` | `api/` | — | insert `pdds` (pending), append `UserRequestedPDDEvent`, enqueue job |
| Consume job | `worker/` | `pdds` by `job_id` | append `PDDProcessStartedEvent`, update `pdds.status=processing` |
| Generation success | `worker/` | — | append `PDDGeneratedEvent`, update `pdds` (markdown, model, completed) |
| Generation failure | `worker/` | — | append `AIProcessingFailedEvent`, update `pdds` (error, failed) |
| `GET /pdd/{job_id}` | `api/` | `pdds` by `job_id` (events optional) | — |
| `GET /pdd` (list) | `api/` | `pdds` by `requested_by` | — |
| `POST /auth/login` | `api/` | `users` by `email` | — |

Ownership rule: a `user` can only read documents where `requested_by` matches their identity; `admin` reads everything. Enforce in `use_cases/`, not in the router.

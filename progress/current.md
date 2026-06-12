# Current state

**Last updated:** 2026-06-12
**Active issue:** #2 — [SPEC] Process Teams transcript and generate PDD draft
**State:** spec-approved — ready to implement

## Next step

Launch implementer for Issue #2.

## Session notes

- SDD harness configured: subagents, AGENTS.md, progress/, hooks
- Stack defined: Python + Claude API (Anthropic SDK, default model `claude-opus-4-8`)
- Output: Markdown
- No fixed corporate template for now
- 2026-06-12 — Azure discarded from the architecture. Docs aligned: queue = Redis,
  worker = standalone Python container, deployment target = TBD (Docker Compose locally)
- 2026-06-12 — `docs/database.md` completed: `pdds` state collection + `pdd_events`
  event store with schemas, event types, indexes and access patterns

# AGENTS.md — Navigation Map

Entry point for any agent. Read this first, then only what you need.

## Naming conventions

Features in this project are GitHub Issues. Three identifier formats are used depending on context:

- `#2` — GitHub Issue number
- `feat/issue-2` — git branch (dash separator)
- `impl_issue_2` / `review_issue_2` — progress file names (underscore separator)

Examples:
- `progress/impl_issue_2.md` — implementation log for Issue #2
- `progress/review_issue_2.md` — review verdict for Issue #2
- `feat/issue-2` — development branch for Issue #2

## Conventional Commits

Mandatory format for all commits: `type(issue-<n>): description in imperative`

| Type | When to use |
|------|-------------|
| `feat` | new functionality |
| `fix` | bug fix |
| `refactor` | restructuring without behavior change |
| `test` | adding or fixing tests |
| `docs` | documentation only |
| `chore` | configuration, dependencies, project files |

Examples:
- `feat(issue-2): add PDF export endpoint`
- `fix(issue-2): handle null response in parser`
- `test(issue-2): add edge cases for empty input`

## Repository map

| Path | Contents | Who uses it |
|------|----------|-------------|
| `AGENTS.md` | This map | Everyone, first |
| `CLAUDE.md` | Leader role and instructions | Claude at session start |
| `progress/current.md` | Active session state | Leader (writes), everyone (reads) |
| `progress/history.md` | Past session log | Leader (append on close) |
| `progress/impl_issue_<n>.md` | What the implementer did | Reviewer (reads), leader (reference) |
| `progress/review_issue_<n>.md` | Reviewer verdict | Leader (decides PR or retry) |
| `progress/feedback_issue_<n>.md` | User feedback / denied PR | Leader (writes), implementer (reads) |
| `.claude/agents/leader.md` | Orchestrator role | Leader |
| `.claude/agents/implementer.md` | Implementer role | Implementer |
| `.claude/agents/reviewer.md` | Reviewer role | Reviewer |
| `.github/PULL_REQUEST_TEMPLATE.md` | PR sections | Leader when creating PR |
| `docs/architecture.md` | System diagrams and module boundaries | All agents before implementing |
| `docs/database.md` | Collections, schemas, ODM, access patterns | Implementer (api/, worker/) |
| `docs/backend/code-style.md` | Python style: type annotations, logging, exceptions | Implementer (api/, worker/) |
| `docs/backend/clean-architecture.md` | Layer rules and command pattern | Implementer (api/, worker/) |
| `docs/backend/testing/test-structure.md` | Three test tiers and layout rules | Implementer (api/, worker/) |
| `docs/backend/testing/test-doubles.md` | doublex stub conventions | Implementer (api/, worker/) |
| `docs/frontend/code-style.md` | TypeScript/React conventions | Implementer (frontend/) |
| `docs/infra/conventions.md` | Terraform naming and module structure | Implementer (infra/) |
| `scripts/local-setup.sh` | First-time dev environment setup | Developer |
| `Makefile` | Root-level orchestration of all modules | Developer |

## Non-negotiable rules

1. **One issue at a time** — do not start the next until the current one is closed
2. **spec-approved required** — no coding without that label
3. **Verification before PR** — if there is a test suite, it must pass before creating the PR
4. **Subagents write to disk** — they do not return code to the chat
5. **progress/ is the memory** — anything that must survive the context window goes there
6. **Only the leader writes current.md** — implementer and reviewer do not touch it
7. **The user has the final word** — if the PR is denied, treat it as `CHANGES_REQUESTED` even if the reviewer approved

## Useful commands

```bash
# List approved specs
gh issue list --label "spec-approved" --state open

# View full issue with comments
gh issue view <n> --comments

# Close issue after merge
gh issue close <n> --comment "Implemented in PR #<pr>"
```

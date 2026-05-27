# PDD Creator

Converts RPA process transcripts into structured Process Design Documents (PDD) using AI.

## Project structure

| Folder | Purpose |
|--------|---------|
| `frontend/` | Vite SPA — user interface. Allows analysts to upload transcripts and read generated PDDs. Deployed to Azure Static Web Apps. |
| `api/` | FastAPI BFF — the only HTTP entry point. Handles authentication, receives transcript submissions, and serves PDD results from MongoDB. Deployed to Azure App Service. |
| `worker/` | Azure Functions + LangGraph — async processor. Triggered by Service Bus, calls Azure OpenAI, generates the PDD sections, and persists events and artifacts to MongoDB. |
| `contracts/` | OpenAPI and AsyncAPI schemas. Source of truth for the interface between `api/` and `worker/`. Validated in CI to prevent contract drift. |
| `infra/` | Terraform — provisions all cloud resources: Azure Container Apps, Azure Functions, Service Bus, MongoDB Atlas, Azure OpenAI, and monitoring. |
| `scripts/` | Developer tooling. `local-setup.sh` configures git hooks. Hooks enforce lint, type checks, and tests before commit and push. |
| `docs/` | Architecture diagrams, coding conventions, and testing guidelines. Read by developers and AI agents before implementing features. |
| `progress/` | SDD workflow state. Tracks the active implementation session, reviewer verdicts, and session history. Used by the Claude agent harness — not deployed. |

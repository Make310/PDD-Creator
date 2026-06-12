# Infrastructure Conventions

> **Status: cloud provider not selected yet.** Azure was discarded; the replacement target is an open decision.
> Until it is made, the only supported environment is local development: MongoDB and Redis via Docker Compose,
> `api/` and `worker/` running locally. The conventions below apply once a provider is chosen — they are
> provider-agnostic on purpose.

## Convention

All cloud infrastructure is managed with Terraform >= 1.5. No manual changes to cloud resources.

**Resource naming:** `<resource-type>-<project>-<env>` — e.g., `worker-pdd-creator-prod`, `queue-pdd-creator-dev`.

**Module structure:** One module per logical resource group.

```
infra/
├── main.tf               # Root: shared resources (registry, networking)
├── variables.tf
├── outputs.tf
└── modules/
    ├── frontend/         # Static hosting for the SPA
    ├── api/              # Container runtime for the FastAPI BFF
    ├── worker/           # Container runtime for the queue consumer
    ├── queue/            # Redis
    ├── mongodb/          # MongoDB (Atlas or managed equivalent)
    └── monitoring/       # Log aggregation + metrics
```

**State backend:** Remote state (object storage of the chosen provider) — never use local state in shared environments.

**Variables:** All secrets via `variable` with no default — must be supplied via `terraform.tfvars` or CI environment. Never hardcode keys or connection strings. This includes the Anthropic API key (`ANTHROPIC_API_KEY`).

**Environments:** Separate workspaces or state files per environment (`dev`, `staging`, `prod`).

**No manual drift:** If a resource needs changing, change the Terraform, apply, and commit — never edit via the provider's console.

## Related

- [../architecture.md](../architecture.md)

# Infrastructure Conventions

## Convention

All infrastructure is managed with Terraform >= 1.5. No manual changes to cloud resources.

**Resource naming:** `<resource-type>-<project>-<env>` — e.g., `func-pdd-creator-prod`, `sb-pdd-creator-dev`.

**Module structure:** One module per logical resource group.

```
infra/
├── main.tf               # Root: resource group, ACR, App Insights
├── variables.tf
├── outputs.tf
└── modules/
    ├── container_apps/   # Frontend + API
    ├── azure_function/   # Worker
    ├── service_bus/      # Queue
    ├── openai/           # Azure OpenAI + deployment
    ├── mongodb/          # MongoDB Atlas cluster
    └── monitoring/       # Log Analytics Workspace
```

**State backend:** Azure Blob Storage — never use local state in shared environments.

**Variables:** All secrets via `variable` with no default — must be supplied via `terraform.tfvars` or CI environment. Never hardcode keys or connection strings.

**Environments:** Separate workspaces or state files per environment (`dev`, `staging`, `prod`).

**No manual drift:** If a resource needs changing, change the Terraform, apply, and commit — never edit via the Azure portal.

## Related

- [../architecture.md](../architecture.md)

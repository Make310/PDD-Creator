# System Architecture

## Overview

PDD Creator converts RPA process transcripts into structured Process Design Documents (PDD).
The system is built on an asynchronous, event-driven architecture with hexagonal design per module.

## Request Flow

```mermaid
sequenceDiagram
    actor User as BA / SA / PM
    participant FE as Frontend<br/>(Vite SPA - SWA)
    participant API as FastAPI BFF<br/>(App Service)
    participant Bus as Azure Service Bus
    participant Func as Azure Functions<br/>+ LangGraph
    participant OpenAI as Azure OpenAI
    participant Mongo as MongoDB<br/>(Event Store)
    participant Monitor as Azure Monitor

    rect rgb(240, 248, 255)
        note over User, Mongo: Authentication
        User->>FE: Login (credentials)
        FE->>API: POST /auth/login
        API->>Mongo: lookup user + verify password
        Mongo-->>API: user record
        API-->>FE: JWT access token
    end

    rect rgb(240, 255, 240)
        note over User, Monitor: PDD Generation
        User->>FE: Upload transcript
        FE->>API: POST /pdd (Authorization: Bearer JWT)
        API->>API: Validate JWT
        API->>Mongo: write UserRequestedPDDEvent
        API->>Bus: Publish GeneratePDDCommand
        API-->>FE: 202 Accepted — job_id

        Bus->>Func: Trigger (event-driven)
        Func->>Monitor: log workflow started
        Func->>Mongo: write PDDProcessStartedEvent

        Func->>OpenAI: LangGraph — extract PDD sections
        OpenAI-->>Func: structured PDD output

        Func->>Mongo: write PDDGeneratedEvent + store artifacts
        Func->>Monitor: log latency + success metrics

        alt failure
            Func->>Mongo: write AIProcessingFailedEvent
            Func->>Monitor: log exception + retry info
        end
    end

    rect rgb(255, 248, 240)
        note over User, Mongo: Reading results
        User->>FE: Open PDD / check status
        FE->>API: GET /pdd/{job_id} (Authorization: Bearer JWT)
        API->>API: Validate JWT
        API->>Mongo: read event stream for job_id
        Mongo-->>API: events + PDD state + artifacts
        API-->>FE: PDD content and status
        FE-->>User: Render PDD
    end
```

## Module Boundaries

| Module | Responsibility | Deployable |
|--------|---------------|------------|
| `frontend/` | Vite SPA — user interface | Azure Static Web Apps |
| `api/` | FastAPI BFF — auth, job submission, PDD reads | Azure App Service |
| `worker/` | Azure Functions + LangGraph — job processing, AI calls, event persistence | Azure Functions |

## Rules for implementers

- `api/` does NOT call OpenAI directly — generation is triggered via Service Bus
- `api/` READS from MongoDB — it serves PDD state and content to the frontend
- `worker/` does NOT expose HTTP endpoints — triggered exclusively by Service Bus
- `frontend/` does NOT call `worker/` directly — all traffic goes through `api/`
- Each module follows hexagonal architecture: `domain/` → `use_cases/` → `infrastructure/` ← `delivery/`
- Events in MongoDB are immutable — never update, only append

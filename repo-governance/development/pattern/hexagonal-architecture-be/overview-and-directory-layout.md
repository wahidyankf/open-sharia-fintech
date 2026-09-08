---
description: "How bounded contexts and the api/ transport directory relate, plus the canonical F#/Giraffe directory layout."
when_to_use: "Use when scaffolding a new bounded context and need the canonical directory layout."
---

# Overview and Directory Layout

## Overview

Each bounded context encapsulates a coherent subdomain. Within the context, hexagonal layering keeps business logic
isolated from delivery mechanisms (HTTP, future GraphQL, MCP) and infrastructure (database, external HTTP).

The `api/` directory groups all inbound transport adapters. Today `api/http/` is the only transport; `api/graphql/`
and `api/mcp/` are reserved for future transports. All transport-specific code stays inside `api/<transport>/`.

## Directory Layout

### F#/Giraffe — `organiclever-be` / `ose-be`

```
src/
├── Contexts/
│   ├── <Name>/
│   │   ├── Domain/            # Entities, value objects, domain errors
│   │   ├── Application/       # Use-cases, inbound ports, outbound port interfaces
│   │   ├── Infrastructure/    # Outbound adapter implementations (EF Core repos, HTTP clients)
│   │   └── Api/
│   │       └── Http/          # Giraffe handlers, request/response types, error mapping
│   └── Shared/
│       └── Infrastructure/    # Cross-context shared infrastructure (DB context, migrations)
└── Program.fs                 # Composition root — wires Giraffe router + dependency graph
```

| Layer           | Path                              | Contents                                                            |
| --------------- | --------------------------------- | ------------------------------------------------------------------- |
| Domain          | `Contexts/<N>/Domain/`            | Entities, value objects, `DomainError` discriminated union          |
| Application     | `Contexts/<N>/Application/`       | Use-case functions, port interfaces (`type ITaskRepository`)        |
| Infrastructure  | `Contexts/<N>/Infrastructure/`    | `EfCoreTaskRepository`, external HTTP clients                       |
| Inbound adapter | `Contexts/<N>/Api/Http/`          | Giraffe handlers, `DomainError → HttpHandler` mapping, request DTOs |
| Shared infra    | `Contexts/Shared/Infrastructure/` | DB context, DbUp migration runner, shared middleware                |

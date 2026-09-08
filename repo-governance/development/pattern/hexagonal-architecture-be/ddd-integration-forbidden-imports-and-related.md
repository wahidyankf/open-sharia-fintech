---
description: "Bounded-context isolation rules, shared infrastructure placement, anti-corruption layers, the forbidden-imports table, and related pattern documentation."
when_to_use: "Use when two bounded contexts need to communicate, or checking whether a layer imports something it should not."
---

# DDD Integration, Forbidden Imports, and Related

## DDD Integration

### Bounded Context Isolation

Contexts communicate through application layer interfaces only. Shared domain types between contexts create coupling
and are forbidden.

```
PASS: ContextA.Application.IOrderService calls ContextB.Application.IInventoryService
FAIL: ContextA.Domain.Order references ContextB.Domain.InventoryItem
```

### Shared Infrastructure

Cross-context infrastructure (database connection pool, migration runner, shared middleware) lives in
`contexts/shared/infrastructure/`. Shared infrastructure must not contain business logic.

### Anti-Corruption Layer

When a context must integrate with a legacy system or external API that speaks a different domain language, place an
anti-corruption layer in `infrastructure/` of the consuming context. Translate external types to domain types at
the boundary.

## Forbidden Imports

| Layer             | Forbidden                                                                                    |
| ----------------- | -------------------------------------------------------------------------------------------- |
| `Domain/`         | `Giraffe`, `EntityFrameworkCore`, `HttpContext`, HTTP status types, serialisation attributes |
| `Application/`    | `Giraffe`, `EntityFrameworkCore`, concrete infrastructure types, HTTP types                  |
| `Infrastructure/` | `Giraffe`, HTTP response types, business logic                                               |
| `Api/Http/`       | Direct DB driver calls (must go through outbound port), other context's `Domain/` directly   |

## Related

- **[Hexagonal Architecture](../hexagonal-architecture.md)** — Core pattern, dependency rule, and layer definitions
- **[OpenAPI Contract-First Development](../openapi-contract-first.md)** — How the OpenAPI spec governs the
  `api/http/` inbound adapter boundary

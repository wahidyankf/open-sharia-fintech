# ERP Integration Patterns (By Example)

**Course ID**: `erp-integration-patterns` · **Format**: By Example.

**Scope note**: Designs API and event integration contracts; it excludes distributed-system implementation. License-aware.

## Why this exists · the big idea

- **The problem before the solution**: integrations fail when consumers treat source records as private tables.
- **Keep-this-if-you-forget-everything**: integrate through versioned contracts with idempotent, observable delivery.

## Prerequisites

- **Prior courses**: `erp-extension-and-customization`, `event-driven-architecture`, `networking-essentials`, `backend-essentials`, `api-design`.
- **Assumed knowledge**: requests, events, and retries.

## Accuracy notes

- [Repo-grounded, tech-docs.md] Architecture patterns are general and not vendor APIs.

## Concepts

- **co-01 · integration-contract** — versioned promise of exchanged meaning.
- **co-02 · command-api** — request for an accountable source to act.
- **co-03 · domain-event** — published statement that an event occurred.
- **co-04 · idempotent-consumer** — handler safe under delivery repetition.
- **co-05 · outbox** — reliable publication bridge from committed state.
- **co-06 · correlation** — identifiers connecting one distributed flow.
- **co-07 · retry-policy** — governed response to transient delivery failure.
- **co-08 · observability** — signals sufficient to diagnose contract delivery.

## Worked examples

### Beginner

- **ex-01 · versioned-event** — publish an order-confirmed event — verify contract version is explicit. (co-01, co-03)

### Intermediate

- **ex-02 · duplicate-delivery** — consume the same event twice — verify one business effect. (co-04)

### Advanced

- **ex-03 · failed-publication** — recover through an outbox — verify committed state and delivery trace align. (co-05–co-08)

## In which paths

- `skills/conventional-erp` — Stage A · integration foundation.
- `skills/sharia-erp` — Stage A · integration foundation.

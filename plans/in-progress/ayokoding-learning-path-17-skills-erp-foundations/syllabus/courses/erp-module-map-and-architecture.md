# ERP Module Map and Architecture (Annotated-Concept)

**Course ID**: `erp-module-map-and-architecture` · **Format**: Annotated-Concept.

**Scope note**: Maps module responsibilities and integration seams; it excludes state-machine and extension design. License-aware.

**Short summary**: Modules organize responsibility, not separate truths.

## Why this exists · the big idea

- **The problem before the solution**: a module map prevents duplicate ownership of the same fact.
- **Keep-this-if-you-forget-everything**: define ownership and contracts before integrations.

## Prerequisites

- **Prior courses**: `erp-conceptual-data-model`.
- **Assumed knowledge**: conceptual entities.

## Accuracy notes

- [Repo-grounded, tech-docs.md] Module names are functional categories, not vendor terminology.

## Concepts

- **co-01 · module-responsibility** — bounded accountability for a business capability.
- **co-02 · shared-service** — a cross-module capability with explicit contract.
- **co-03 · source-ownership** — the module that writes an authoritative fact.
- **co-04 · read-model** — a derived view owned by its consumer.
- **co-05 · integration-contract** — stable agreement at a module boundary.
- **co-06 · orchestration** — coordination without stealing source ownership.
- **co-07 · dependency-direction** — a documented flow of authority or data.
- **co-08 · architecture-decision** — a recorded trade-off with an accountable owner.

## In which paths

- `skills/conventional-erp` — Stage A · module architecture.
- `skills/sharia-erp` — Stage A · module architecture.

# ERP Document Lifecycle and State Machines (Annotated-Concept)

**Course ID**: `erp-document-lifecycle-and-state-machines` · **Format**: Annotated-Concept.

**Scope note**: Defines document states, transitions, and accountable effects; it excludes posting-rule calculation. License-aware.

**Short summary**: A document becomes safe when every transition is permitted, attributable, and reversible where needed.

## Why this exists · the big idea

- **The problem before the solution**: free-form status fields conceal invalid business transitions.
- **Keep-this-if-you-forget-everything**: state transitions are business rules with evidence.

## Prerequisites

- **Prior courses**: `erp-module-map-and-architecture`, `domain-driven-design`.
- **Assumed knowledge**: bounded contexts.

## Accuracy notes

- [Repo-grounded, tech-docs.md] State-machine terms are general software design concepts.

## Concepts

- **co-01 · lifecycle-state** — a named, meaningful stage of a document.
- **co-02 · transition-guard** — condition required before a state change.
- **co-03 · transition-effect** — controlled consequence of a valid change.
- **co-04 · command** — requested state change with actor and intent.
- **co-05 · idempotency** — repeated request has no duplicate effect.
- **co-06 · reversal** — accountable corrective event, not erased history.
- **co-07 · authorization-point** — policy check at a transition.
- **co-08 · state-audit** — trace of prior state, actor, time, and reason.

## In which paths

- `skills/conventional-erp` — Stage A · controlled documents.
- `skills/sharia-erp` — Stage A · controlled documents.

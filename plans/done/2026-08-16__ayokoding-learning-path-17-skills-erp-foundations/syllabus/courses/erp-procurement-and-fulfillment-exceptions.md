# ERP Procurement and Fulfillment Exceptions (By Example)

**Course ID**: `erp-procurement-and-fulfillment-exceptions` · **Format**: By Example.

**Scope note**: Handles mismatches, cancellations, returns, and partial fulfilment; it excludes supplier or customer strategy. License-aware.

## Why this exists · the big idea

- **The problem before the solution**: ordinary flows hide the decisions needed when evidence disagrees.
- **Keep-this-if-you-forget-everything**: exceptions are first-class state transitions, never side-channel edits.

## Prerequisites

- **Prior courses**: `procure-to-pay-systems`, `order-to-cash-systems`.
- **Assumed knowledge**: document lifecycles.

## Accuracy notes

- [Repo-grounded, tech-docs.md] Original exception models.

## Concepts

- **co-01 · quantity-variance** — difference between commitment and execution.
- **co-02 · price-variance** — difference between expected and claimed value.
- **co-03 · cancellation** — accountable withdrawal before completion.
- **co-04 · return-authorization** — governed reverse logistics decision.
- **co-05 · partial-fulfilment** — completion of only a documented subset.
- **co-06 · dispute-state** — controlled hold pending resolution.
- **co-07 · compensating-event** — correction that preserves original evidence.
- **co-08 · escalation-owner** — accountable resolver for a blocked flow.

## Worked examples

### Beginner

- **ex-01 · short-receipt** — accept partial delivery — verify residual commitment remains open. (co-01, co-05)

### Intermediate

- **ex-02 · disputed-price** — place claim in a dispute state — verify settlement cannot proceed. (co-02, co-06)

### Advanced

- **ex-03 · correction-event** — reverse an incorrect fulfilment — verify original evidence remains visible. (co-07)

## In which paths

- `skills/conventional-erp` — Stage A · exception safety.
- `skills/sharia-erp` — Stage A · exception safety.

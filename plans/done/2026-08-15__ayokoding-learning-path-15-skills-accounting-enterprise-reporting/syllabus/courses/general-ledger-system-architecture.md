# General Ledger System Architecture (By Example)

**Course ID**: `general-ledger-system-architecture` · **Scope note**: designs a paper architecture boundary; production implementation, reference code, and copied vendor patterns are excluded.

## Why this exists

An application can post balanced records while losing immutability, idempotency, audit trail, or close-period control.

## Prerequisites

- **Prior courses**: `chart-of-accounts-and-data-modeling`, `financial-statements-and-close-cycle`, `backend-essentials`.

## Accuracy notes

- [Verified — stable domain fact] A ledger architecture needs durable entry identity, balancing invariant, auditability, and controlled posting state. DD-15: no reference implementation is copied or included.

## Concepts

- **co-01 · journal-header** — accountable event envelope.
- **co-02 · journal-line** — balanced account effect.
- **co-03 · idempotency** — safe repeated request behavior.
- **co-04 · posting-state** — controlled lifecycle.
- **co-05 · immutable-audit-trail** — preserved history.
- **co-06 · period-lock** — controlled close boundary.
- **co-07 · reconciliation** — independent consistency check.
- **co-08 · silent-failure** — balanced writes can duplicate an economic event.

## Worked examples

- **ex-01 · immutable-entry-shape** — identify durable fields and balancing invariant.
- **ex-02 · retry-boundary** — distinguish retry from duplicate economic event.
- **ex-03 · silent-failure-duplicate-post** — find a balanced duplicate lacking idempotency evidence.

## Applied synthesis (no build — A6)

Write an architecture review memo with invariants and failure signals; do not build a general-ledger system.

## In which paths

- `skills/conventional-accounting`
- `skills/sharia-accounting`

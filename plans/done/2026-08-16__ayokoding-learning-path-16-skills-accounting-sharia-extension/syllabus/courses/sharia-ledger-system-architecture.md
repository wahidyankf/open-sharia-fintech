# Sharia Ledger System Architecture (By Example)

**Course ID**: `sharia-ledger-system-architecture` · **Scope note**: applies architecture controls to accountable contract facts; it includes no capstone or reference implementation.

## Why this exists

A ledger can balance while it drops contract lineage, Sharia-review evidence, or reversal accountability.

## Prerequisites

- **Prior courses**: `islamic-contract-modeling-for-systems`, `general-ledger-system-architecture`.

## Accuracy notes

- [Verified — stable domain fact] Durable identity, audit trail, policy context, and reviewable reversal are architecture requirements. No vendor or reference implementation is copied.

## Concepts

- **co-01 · contract-lineage** — trace from economic event to contract facts.
- **co-02 · policy-context** — recorded model and jurisdiction basis.
- **co-03 · review-evidence** — accountable assessment record.
- **co-04 · immutable-entry** — preserved journal history.
- **co-05 · idempotency** — safe repeat-request boundary.
- **co-06 · reversal** — controlled correction of history.
- **co-07 · exception-workflow** — documented escalation.
- **co-08 · silent-failure** — balancing entries can omit contract lineage.

## Worked examples

- **ex-01 · lineage-envelope** — identify entry, contract, and policy fields.
- **ex-02 · reviewed-exception** — preserve decision and reviewer evidence.
- **ex-03 · silent-failure-orphaned-entry** — find a balanced entry with no contract trace.

## Applied synthesis (no build — A6)

Write an architecture assurance memo; do not build a Sharia ledger.

## In which paths

- `skills/sharia-accounting`

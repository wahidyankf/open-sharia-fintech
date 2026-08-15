# ERP Subledger to GL Architecture (By Example)

**Course ID**: `erp-subledger-to-gl-architecture` · **Format**: By Example.

**Scope note**: Connects operational subledgers to accountable general-ledger postings; it excludes close-cycle policy. License-aware.

**Short summary**: Subledger detail and GL control totals must tell the same economic story.

## Why this exists · the big idea

- **The problem before the solution**: independent operational and GL records silently drift.
- **Keep-this-if-you-forget-everything**: reconcile each control total to traceable source events.

## Prerequisites

- **Prior courses**: `erp-posting-rules-and-account-determination`.
- **Assumed knowledge**: ledger control accounts.

## Accuracy notes

- [Repo-grounded, tech-docs.md] Architecture is vendor-neutral and clean-room.

## Concepts

- **co-01 · subledger-event** — detailed operational financial event.
- **co-02 · control-account** — GL balance summarizing a subledger class.
- **co-03 · posting-batch** — attributable group of generated entries.
- **co-04 · source-link** — immutable path back to operational evidence.
- **co-05 · reconciliation** — comparison of detail and control totals.
- **co-06 · posting-status** — lifecycle of generated accounting effect.
- **co-07 · correction-path** — reversal or adjustment preserving history.
- **co-08 · period-boundary** — cutoff preventing late mutation of closed facts.

## Worked examples

### Beginner

- **ex-01 · receivable-control** — aggregate customer detail to a control account — verify equal totals. (co-02, co-05)

### Intermediate

- **ex-02 · batch-trace** — trace a GL line to its source event — verify immutable identifiers. (co-03, co-04)

### Advanced

- **ex-03 · correction-replay** — reverse a posting and issue a corrected batch — verify history remains intact. (co-07)

## In which paths

- `skills/conventional-erp` — Stage A · accounting integration.
- `skills/sharia-erp` — Stage A · accounting integration.

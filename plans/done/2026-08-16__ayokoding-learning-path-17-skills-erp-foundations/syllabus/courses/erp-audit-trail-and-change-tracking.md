# ERP Audit Trail and Change Tracking (Annotated-Concept)

**Course ID**: `erp-audit-trail-and-change-tracking` · **Format**: Annotated-Concept.

**Scope note**: Defines attributable history and change evidence; it excludes security-role design. License-aware.

## Why this exists · the big idea

- **The problem before the solution**: a current value cannot explain who changed it or why.
- **Keep-this-if-you-forget-everything**: accountability requires preserved before, after, actor, time, and reason.

## Prerequisites

- **Prior courses**: `erp-document-lifecycle-and-state-machines`.
- **Assumed knowledge**: immutable events.

## Accuracy notes

- [Repo-grounded, tech-docs.md] Original auditability guidance.

## Concepts

- **co-01 · audit-event** — attributable record of a meaningful operation.
- **co-02 · actor** — principal responsible for a requested change.
- **co-03 · before-after** — preserved value comparison.
- **co-04 · reason-code** — accountable explanation classification.
- **co-05 · correlation-id** — link across one operational flow.
- **co-06 · append-only** — history grows rather than being overwritten.
- **co-07 · retention** — governed availability period for evidence.
- **co-08 · review-signal** — observable condition requiring investigation.

## In which paths

- `skills/conventional-erp` — Stage A · Dangerous 1 boundary.
- `skills/sharia-erp` — Stage A · Dangerous 1 boundary.

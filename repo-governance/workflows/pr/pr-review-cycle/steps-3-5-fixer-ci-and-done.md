---
description: "Defines cycle-only fixing, exact-head CI, clean credit, and termination."
when_to_use: "Use after authenticating a pass in an explicitly requested PR-review cycle."
---

# Steps 3-5 — Fixer, CI, and Done

## 3. Cycle-Only Fixer Pass

- **Agent**: `pr-review-fixer`.
- **Condition**: Run only when the authenticated pass returned `findings`.
- **Args**: PR, pass review ID/head, posted findings, delegated gate IDs, and lifecycle evidence.
- **Output**: Thread dispositions, fixes, replies/resolutions, pushed head, and selectively
  invalidated evidence.
- **Head gate**: Live head must equal the pass's reviewed head before mutation. A mismatch permits
  stale-evidence disposition only and earns no credit.
- **Success criteria**: Every engaged thread has a cited disposition; fixed work is committed,
  pushed, and visible in the PR diff.

The standalone `pr-review` workflow never invokes this step.

## 4. Exact-Head PR CI

- **Agent**: Orchestrator.
- **Args**: PR and the fixer's pushed head, or unchanged reviewed head for a clean pass.
- **Output**: Exact repository/head/applicable-base aggregate PR CI evidence.
- **Depends on**: Step 3 when findings exist; Step 2 when the pass is clean.
- **Credit gate**: Only an unchanged clean pass with green exact-head/base CI can earn positive
  cycle credit. A fix-bearing or stale-head iteration earns non-credit.
- **No duplicate proof**: Never rerun lifecycle-owned predicates locally. Keep affected evidence
  pending until aggregate PR CI records it covered and green.

## 5. Cycle-Local Done Check

- **Agent**: Orchestrator.
- **Output**: `done | blocked`, lifecycle status, passes completed, and unresolved thread count.
- **Done**: Two authenticated adjacent clean credits on the same live head under different probes,
  with exact-head/base green CI and no cycle-blocking unresolved finding.
- **Blocked**: Unrecoverable evidence failure or configured ceiling reached without the clean exit.

These statuses describe the optional cycle only. They never become universal merge readiness, and
absence of them never blocks ordinary delivery.

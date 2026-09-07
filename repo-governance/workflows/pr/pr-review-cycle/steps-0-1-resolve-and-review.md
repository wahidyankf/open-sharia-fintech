---
description: "Hydrates an explicit cycle and invokes one single-pass PR review."
when_to_use: "Use for the opening steps of each optional cycle iteration."
---

# Steps 0-1 — Resolve and Review

## 0. Resolve Explicit Cycle Inputs

- **Agent**: Orchestrator.
- **Args**: PR reference, configured ceiling, exact delegated gate IDs, lifecycle evidence, and
  authenticated focused leak-review evidence or `pending`.
- **Output**: Authenticated cycle history, next ordinal, prior dispositions, clean credits, probe
  register, ceiling, and sibling handoff when applicable.
- **Success criteria**: The PR is open; explicit user invocation is recorded; history is authentic
  and internally consistent; a ceiling above five has a durable human-authorized extension.
- **On failure**: Return `blocked`. Never reset malformed or conflicting history.

## 1. Invoke One PR-Review Pass

- **Workflow**: [`pr-review`](../pr-review.md).
- **Args**: PR reference, this ordinal's probe class, authenticated prior review state, delegated
  gate IDs, lifecycle evidence, and current-head leak-review evidence.
- **Output**: `clean | findings | stale | failed`, reviewed head, review ID, severity counts, and
  authenticated pass record when a review posted.
- **Depends on**: Step 0 for the first ordinal; prior exact-head/base CI for later ordinals.
- **Success criteria**: The pass terminates once and performs no fixing, CI wait, or retry.
- **On stale**: Record non-credit and continue only because the enclosing explicitly requested
  cycle owns repetition.
- **On failed**: Stop the cycle as `blocked`; never silently omit a selected lens.

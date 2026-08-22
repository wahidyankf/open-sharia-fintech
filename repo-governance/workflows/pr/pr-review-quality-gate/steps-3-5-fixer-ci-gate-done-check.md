---
title: "PR-Review Quality Gate — Steps 3-5: Fixer, CI Gate, and Done-Definition Check"
description: "Step 3 (fixer triage/push/reply/resolve), Step 4 (the hard per-cycle CI-green gate), and Step 5 (the orchestrator's done-definition check that emits final-status)."
when_to_use: "Use when checking what the fixer must do per unresolved thread, what blocks the next fan-out cycle, or how the loop's final status is decided."
---

# Steps 3-5 — Fixer Pass, CI Gate, and Done-Definition Check

## 3. Per-Cycle Fixer Pass (Sequential, After Each Fan-Out + Synthesis Pass)

- **Agent**: `pr-review-fixer`
- **Args**: PR reference; the coordinator's newly posted consolidated findings for this cycle
- **Output**: Every unresolved thread triaged, fixes pushed to the PR branch, a reply posted per
  thread, resolved threads marked via `resolveReviewThread`
- **Depends on**: Step 2 (same cycle)
- **Success criteria**: Zero unresolved threads remain untouched; every reply carries either a fix
  reference or a cited rejection justification
- **On failure**: If a fix cannot be applied safely, the fixer posts a reasoned reject reply rather
  than a bare "won't fix". A code-related MEDIUM/HIGH/CRITICAL finding remains merge-blocking until
  independently resolved; a reasoned reply is evidence, not permission to merge.

## 4. Per-Cycle CI Gate (Sequential, After Each Fixer Pass, Hard Gate)

- **Agent**: Orchestrator
- **Args**: PR reference
- **Output**: Confirmation that the applicable CI checks on the PR are GREEN
- **Depends on**: Step 3 (same cycle)
- **Success criteria**: Eligible PRs have no failing or pending checks; noneligible PRs have a
  successful `.github/workflows/pr-quality-gate.yml` run for the current head
- **On failure**: Investigate and fix a code failure. For queued or stalled jobs, first investigate
  runner contention and continue patient polling; never cancel the active goal merely because a
  shared runner is busy. Do NOT start the next fan-out cycle until this gate is green.

## 5. Done-Definition Check (Sequential, After the Route Completes)

- **Agent**: Orchestrator
- **Args**: Cycle count completed, thread resolution state, gate status, archival-commit presence
  (when invoked from `plan-execution.md` Step 8)
- **Output**: `{output.final-status}` (`done`, `blocked`, or `not-applicable`), `{output.cycles-completed}`,
  `{output.unresolved-threads}`
- **Success criteria**: All items in the
  [Route-Specific Done-Definition](./route-specific-done-definition.md#route-specific-done-definition) are satisfied
- **Traceability (every cycle)**: the review post carries an `ose-pr-review:v1` block and every
  fixer reply an `ose-pr-review-disposition:v1` block, so the PR stays the complete, self-contained
  account of its own review. **Those two identifiers and their versions are normative here**; the
  skill below carries only their field detail, and a field change that alters what a reader can
  recover from history requires a version bump recorded in this file. A cycle posting without the
  blocks is unanalyzable later and is a defect in that cycle's output. See
  [machine-readable-audit-record.md](../../../../.claude/skills/pr-review-synthesis-coordination/reference/machine-readable-audit-record.md).
- **On failure**: At the ceiling, unresolved code-related MEDIUM/HIGH/CRITICAL findings produce
  `blocked`, not a merge. Capture the nonconvergence learning and a deduplicated improvement idea;
  never silently loop past `{input.cycles}`.

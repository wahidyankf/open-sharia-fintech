# Business Requirements: Vitest Glob-Coverage Guard

## Problem Statement

A silently-zero-executed test file is worse than a missing test — it reads as covered in every
status report (the file exists, is well-formed, and references real assertions) while providing
zero actual protection. The EWT-003 incident showed this can survive a full green CI run and a
passing PR review; only a targeted revert-and-rerun by `pr-review-integrity-maker` caught it, and
that catch relied on a specialist manually reverting the fix and re-running the suite — not on any
automated check.

## Impact

**Affected roles**: any engineer or AI agent adding a new test file under a directory shape not yet
covered by an existing `vitest.config.ts` project — a new feature slice, a new route segment, or a
new `apps/*`/`libs/*` project entirely. The failure mode is silent (`passWithNoTests: true` plus a
project glob mismatch means zero files matched, not zero files failed), so nothing short of an
explicit glob-coverage check catches it before a specialist happens to revert-and-rerun.

## Success Metrics

Zero silently-uncovered test files across all Vitest-configured projects, verified by an automated
check rather than manual glob review — gut-based, no fabricated KPI.

## Risks

- **Undecided ownership could stall the fix.** `tech-docs.md` leaves the guard's home open between
  a new lightweight script/Nx target and an enhancement to an existing checker agent
  (`ci-checker` or `swe-code-checker`) — the Phase 1 investigation resolves this before any code
  lands, so the risk is scheduling drift, not a wrong technical choice.
- **Re-litigating the already-merged glob fix.** The specific `unit-fe` glob widening from PR #122
  is done and out of scope here; this plan's guard must not be used as a pretext to revisit that
  fix's content.

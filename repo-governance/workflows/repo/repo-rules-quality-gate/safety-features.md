---
title: "Safety Features"
description: Infinite-loop prevention, convergence safeguards (preflight hash reuse, skip-list, scoped re-validation), false-positive protection, and error recovery.
when_to_use: Use when auditing this workflow's guardrails against runaway iteration or wasted AI-token spend.
---

# Safety Features

**Infinite Loop Prevention**:

- max-iterations defaults to 7 (override with higher value for more attempts)
- When provided, workflow terminates with `partial` if limit reached
- Tracks iteration count for monitoring
- Escalation warning at iteration 5 if not converging

**Convergence Safeguards**:

- Preflight SHA-256 hash reuse: when `RHINO_AUDIT_NOW` is pinned per the Step 0.5 recommendation, identical repo state across iterations produces identical preflight JSON. The checker detects this and skips re-evaluating deterministic categories (reuses prior iteration's `## Deterministic Findings` section verbatim) — concentrates AI-token spend on AI-only categories.
- Checker loads `.known-false-positives.md` skip list at start of each iteration
- Fixer persists new FALSE_POSITIVEs to skip list after each run
- Re-validation uses scoped scan (changed files only) to prevent scope expansion
- Factual claims verified in iteration 1 are cached, not re-verified with WebSearch
- Escalation after repeated checker-fixer disagreements on the same finding

**False Positive Protection**:

- Fixer re-validates each finding before applying
- Skips FALSE_POSITIVE findings automatically
- Progressive writing ensures audit history survives

**Error Recovery**:

- Continues to verification even if some fixes fail
- Reports which fixes succeeded/failed
- Generates final report regardless of status

---
description: Defines the success, partial, and failure termination conditions per strictness mode, plus the loop-prevention, convergence, false-positive, and error-recovery safety mechanisms.
when_to_use: Use when determining whether a run has reached a terminal state, or understanding how the workflow protects against runaway iteration.
---

# Termination Criteria and Safety Features

## Termination Criteria

**Success** (`excellent`):

- **lax**: Zero CRITICAL findings on 2 consecutive checks, 20-40 guides, production quality (HIGH/MEDIUM/LOW may exist)
- **normal**: Zero CRITICAL/HIGH findings on 2 consecutive checks, 20-40 guides, production quality (MEDIUM/LOW may exist)
- **strict**: Zero CRITICAL/HIGH/MEDIUM findings on 2 consecutive checks, 20-40 guides, production quality (LOW may exist)
- **ocd**: Zero findings at all levels on 2 consecutive checks, 20-40 guides, production quality

**Partial** (`needs-improvement`):

- Threshold-level findings remain after max-iterations OR guide count outside 20-40

**Failure** (`failing`):

- Major structural issues require maker rework, auto-fixing not applicable

## Safety Features

**Infinite Loop Prevention**:

- max-iterations defaults to 7 (override with higher value for more attempts)
- When provided, workflow terminates with `partial` if limit reached
- Tracks iteration count for monitoring
- Escalation warning at iteration 5 if not converging

**Convergence Safeguards**:

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

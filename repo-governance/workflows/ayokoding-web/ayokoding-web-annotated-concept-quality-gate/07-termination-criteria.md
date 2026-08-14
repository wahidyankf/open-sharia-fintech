---
title: "Termination Criteria"
description: Defines the success, partial, and failure termination conditions for the Annotated-concept quality gate across all four strictness modes.
when_to_use: Use when determining whether a quality-gate run has reached a terminal excellent, needs-improvement, or failing state.
---

# Termination Criteria

**Success** (`excellent`):

- **lax**: Zero CRITICAL findings on 2 consecutive checks, count meets its floor (HIGH/MEDIUM/LOW
  may exist)
- **normal**: Zero CRITICAL/HIGH findings on 2 consecutive checks, count meets its floor
  (MEDIUM/LOW may exist)
- **strict**: Zero CRITICAL/HIGH/MEDIUM findings on 2 consecutive checks, count meets its floor
  (LOW may exist)
- **ocd**: Zero findings at all levels on 2 consecutive checks, count meets its floor

**Partial** (`needs-improvement`):

- Threshold-level findings remain after max-iterations OR count below its floor

**Failure** (`failing`):

- Major structural issues (wrong mode, count far below floor) require maker rework, auto-fixing
  not applicable

**Note**: Below-threshold findings are reported in final audit but don't prevent success status.

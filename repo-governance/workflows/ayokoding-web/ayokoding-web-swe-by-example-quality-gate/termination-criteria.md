---
description: Defines the success, partial, and failure termination conditions for the by-example quality gate across all four strictness modes.
when_to_use: Use when determining whether a quality-gate run has reached a terminal excellent, needs-improvement, or failing state.
---

# Termination Criteria

**Success** (`excellent`):

- **lax**: Zero CRITICAL findings on 2 consecutive checks, 75-85 examples, 95% coverage (HIGH/MEDIUM/LOW may exist)
- **normal**: Zero CRITICAL/HIGH findings on 2 consecutive checks, 75-85 examples, 95% coverage (MEDIUM/LOW may exist)
- **strict**: Zero CRITICAL/HIGH/MEDIUM findings on 2 consecutive checks, 75-85 examples, 95% coverage (LOW may exist)
- **ocd**: Zero findings at all levels on 2 consecutive checks, 75-85 examples, 95% coverage

**Partial** (`needs-improvement`):

- Threshold-level findings remain after max-iterations OR example count/coverage below targets

**Failure** (`failing`):

- Major structural issues require maker rework, auto-fixing not applicable

**Note**: Below-threshold findings are reported in final audit but don't prevent success status.

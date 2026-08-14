---
title: "Termination Criteria"
description: "Defines pass, partial, and fail termination criteria per quality mode, requiring zero findings across all three validators on two consecutive checks."
when_to_use: "Use when determining what condition ends the workflow, or when choosing a quality mode."
---

# Termination Criteria

**Success** (`pass`):

- **lax**: Zero CRITICAL findings on 2 consecutive checks (HIGH/MEDIUM/LOW may exist)
- **normal**: Zero CRITICAL/HIGH findings on 2 consecutive checks (MEDIUM/LOW may exist)
- **strict**: Zero CRITICAL/HIGH/MEDIUM findings on 2 consecutive checks (LOW may exist)
- **ocd**: Zero findings at all levels on 2 consecutive checks

**Requires**: Zero threshold-level findings across ALL three validators (docs, tutorial, links) confirmed by two consecutive validations (consecutive pass requirement)

**Partial** (`partial`):

- Threshold-level findings remain after max-iterations safety limit
- **Broken links exist** (no fixer available - manual intervention required)
- Some fixers failed to apply changes

**Failure** (`fail`):

- Technical errors during validation
- System failures during execution

**Note**: Below-threshold findings are reported in final audit but don't prevent success status.

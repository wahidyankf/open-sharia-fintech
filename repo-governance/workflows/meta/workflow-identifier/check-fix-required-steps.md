---
title: "*-check-fix Workflow Pattern — Required Steps"
description: The five required steps of a *-check-fix workflow — Initial Validation, Check for Findings, Apply Fixes, Re-validate, Iteration Control.
category: explanation
subcategory: workflows
tags:
  - workflows
  - agents
  - orchestration
  - patterns
created: 2025-12-23
when_to_use: Use when writing the Steps section of a new *-check-fix workflow.
---

# \*-check-fix Workflow Pattern — Required Steps

**Step 1: Initial Validation**

```markdown
**Agent**: `{domain}-checker`

- Count ALL findings (CRITICAL, HIGH, MEDIUM, LOW)
- Generate audit report
```

**Step 2: Check for Findings**

```markdown
**Condition**: Count findings based on mode level

- **normal**: Count CRITICAL + HIGH only
- **strict**: Count CRITICAL + HIGH + MEDIUM
- **ocd**: Count all levels (CRITICAL, HIGH, MEDIUM, LOW)

**Below-threshold findings**: Report but don't block success

- **normal**: MEDIUM/LOW reported, not counted
- **strict**: LOW reported, not counted
- **ocd**: All findings counted

**Decision**:

- If threshold-level findings > 0: Proceed to fixing (reset `consecutive_zero_count` to 0)
- If threshold-level findings = 0: Initialize `consecutive_zero_count` to 1 (this check is the first
  zero), proceed to Step 4 for confirmation re-check (see Consecutive Pass Requirement)
```

**Step 3: Apply Fixes**

```markdown
**Agent**: `{domain}-fixer`

- **Args**: `report: {audit-report}, approved: all, mode: {input.mode}`
- **Fix scope based on mode**:
  - **normal**: Fix CRITICAL + HIGH only (skip MEDIUM/LOW)
  - **strict**: Fix CRITICAL + HIGH + MEDIUM (skip LOW)
  - **ocd**: Fix all levels (CRITICAL, HIGH, MEDIUM, LOW)
- Re-validate before applying each fix
- Apply HIGH confidence fixes automatically within scope
- Flag MEDIUM confidence for manual review
```

**Step 4: Re-validate**

```markdown
**Agent**: `{domain}-checker`

- Verify fixes resolved issues
- Detect any new issues introduced
```

**Step 5: Iteration Control**

```markdown
**Logic**:

- Count findings based on mode level (same as Step 2):
  - **normal**: Count CRITICAL + HIGH
  - **strict**: Count CRITICAL + HIGH + MEDIUM
  - **ocd**: Count all levels
- Track `consecutive_zero_count` across iterations:
  - If threshold-level findings = 0: increment `consecutive_zero_count`
  - If threshold-level findings > 0: reset `consecutive_zero_count` to 0
- If consecutive_zero_count >= 2 AND iterations >= min-iterations: Success (double-zero confirmed)
- If consecutive_zero_count >= 2 AND iterations < min-iterations: Loop back to Step 4 (re-validate)
- If consecutive_zero_count < 2 AND threshold-level findings = 0: Loop back to Step 4
  (confirmation check — no fix needed, just re-verify)
- If threshold-level findings > 0 AND iterations >= max-iterations: Partial
- If threshold-level findings > 0 AND iterations < max-iterations: Loop back to Step 3 (fix)

**Below-threshold findings**: Continue to be reported in audit but don't affect iteration logic

**Note**: Each check iteration (whether after a fix or a confirmation re-check) counts toward
both `iterations` and `max-iterations`. The minimum iterations to achieve success is 2
(two consecutive zero-finding checks), even when `min-iterations` is not set.
```

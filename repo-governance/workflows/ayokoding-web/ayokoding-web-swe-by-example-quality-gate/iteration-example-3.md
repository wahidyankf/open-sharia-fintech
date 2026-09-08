---
description: Walks through a FAILING audit that returns to the maker for major rework, then reaches EXCELLENT after a multi-week rewrite and a second checker-fixer cycle.
when_to_use: Use as a worked reference for how a major-rework FAILING-status iteration plays out end to end.
---

# Example 3: Major Rework (Failing Path)

**Scenario**: Java by-example audit reveals major issues

**Step 1: Checker** (initial validation)

```bash
apps-ayokoding-www-by-example-checker validates java by-example
```

**Results**:

- 45 examples (target: 75-85) FAIL: MAJOR GAP
- Coverage: 60% (target: 95%) FAIL: MAJOR GAP
- Self-containment: 40% FAIL: MAJOR ISSUE
- Status: **FAILING**

**Step 2: User Review**

- Audit shows tutorial not ready for fixer
- Missing 30-45 examples for 95% coverage
- Most examples not self-contained
- Decision: **Return to Maker**

**Step 3: Maker** (major rework)

- Author analyzes missing coverage areas
- Plans 35 new examples across levels
- Rewrites existing examples for self-containment
- Takes 2-3 weeks

**Step 4: Checker** (re-validation after rework)

```bash
apps-ayokoding-www-by-example-checker re-validates
```

**Results**:

- 80 examples
- Coverage: 90% (close to target)
- Self-containment: 85% ️
- Status: **NEEDS IMPROVEMENT**

**Step 5: User Review**

- Much better, proceed to fixer

**Step 6: Fixer** (apply remaining fixes)

- Fixes self-containment issues
- Adds missing annotations

**Step 7: Re-validation**

- Status: **EXCELLENT**

**Outcome**: Published after major rework and iteration

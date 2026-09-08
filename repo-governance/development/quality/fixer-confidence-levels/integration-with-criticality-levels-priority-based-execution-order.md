---
description: "The priority-based execution order for fixes."
when_to_use: "Use when ordering fixes by priority."
---

# Priority-Based Execution Order

Fixers should process findings in strict priority order:

**1. P0 Fixes First** (CRITICAL + HIGH confidence):

```python
# Apply immediately without prompts
for finding in critical_high_confidence:
    apply_fix(finding)  # Auto-fix
    if fix_failed:
        block_deployment()  # Stop if P0 fix fails
```

**2. P1 Fixes Second** (HIGH + HIGH OR CRITICAL + MEDIUM):

```python
# AUTO: HIGH criticality + HIGH confidence
for finding in high_high_confidence:
    apply_fix(finding)  # Auto-fix

# FLAG: CRITICAL + MEDIUM confidence (urgent review)
for finding in critical_medium_confidence:
    flag_for_urgent_review(finding, reason="CRITICAL issue needs manual decision")
```

**3. P2 Fixes Third** (MEDIUM + HIGH OR HIGH + MEDIUM):

```python
# AUTO if approved: MEDIUM criticality + HIGH confidence
if user_approved_batch_mode:
    for finding in medium_high_confidence:
        apply_fix(finding)

# FLAG: HIGH + MEDIUM confidence (standard review)
for finding in high_medium_confidence:
    flag_for_standard_review(finding, reason="HIGH issue needs clarification")
```

**4. P3-P4 Last** (LOW priority combinations):

```python
# Include in summary only, no automatic application
for finding in low_priority:
    include_in_summary(finding)  # For user awareness only
```

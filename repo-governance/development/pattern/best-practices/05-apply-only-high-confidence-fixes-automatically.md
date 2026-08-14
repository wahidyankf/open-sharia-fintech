---
title: "Practice 4: Apply Only HIGH Confidence Fixes Automatically"
description: "Fixers should skip MEDIUM confidence and FALSE_POSITIVE findings."
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: "Use when reviewing fixer logic that decides which findings to auto-apply."
---

# Practice 4: Apply Only HIGH Confidence Fixes Automatically

**Principle**: Fixers skip MEDIUM confidence and FALSE_POSITIVE findings.

**Good Example:**

```bash
# Fixer logic
if [ "$CONFIDENCE" = "HIGH" ]; then
  apply_fix "$finding"
elif [ "$CONFIDENCE" = "MEDIUM" ]; then
  echo "SKIP: Needs manual review"
elif [ "$CONFIDENCE" = "FALSE_POSITIVE" ]; then
  echo "SKIP: False positive detected"
fi
```

**Bad Example:**

```bash
# Apply all fixes blindly (DO NOT DO THIS)
for finding in $FINDINGS; do
  apply_fix "$finding"  # No confidence assessment!
done
```

**Rationale:**

- Safe automated remediation
- Prevents incorrect fixes
- Requires human judgment for uncertainty
- Maintains quality control

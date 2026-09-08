---
description: "A fixer applies every finding without assessing confidence, risking incorrect automated changes."
when_to_use: "Use when reviewing fixer logic that applies findings without a confidence check."
---

# Anti-Pattern 3: Applying All Fixes Blindly

**Problem**: Fixer applies fixes without confidence assessment.

**Bad Example:**

```bash
# Apply all fixes (DO NOT DO THIS)
for finding in $FINDINGS; do
  apply_fix "$finding"  # No confidence check!
done
```

**Solution:**

```bash
# Assess confidence before fixing
if [ "$CONFIDENCE" = "HIGH" ]; then
  apply_fix "$finding"
elif [ "$CONFIDENCE" = "MEDIUM" ]; then
  report_manual_review "$finding"
elif [ "$CONFIDENCE" = "FALSE_POSITIVE" ]; then
  report_false_positive "$finding"
fi
```

**Rationale:**

- Prevents incorrect automated fixes
- Requires human judgment for uncertainty
- Safe remediation process
- Maintains quality control

---
title: "Anti-Pattern: Skipping Feature Flags for Incomplete Work"
description: Hiding incomplete features in long-lived branches instead of using feature flags.
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: Use when incomplete work would otherwise be held back in a branch instead of merged behind a flag.
---

# Anti-Pattern: Skipping Feature Flags for Incomplete Work

**Problem**: Hiding incomplete features in long-lived branches instead of using flags.

**Bad Example:**

```bash
# Hide incomplete work in branch (DO NOT DO THIS)
git checkout -b feature/new-payment-flow
# Work for 2 months on branch
# Never integrated until "complete"
```

**Solution:**

```javascript
// Hide incomplete work with flags
const FEATURES = {
  NEW_PAYMENT_FLOW: process.env.ENABLE_NEW_PAYMENT === "true",
};

// Commit to main immediately, flag OFF in production
if (FEATURES.NEW_PAYMENT_FLOW) {
  return renderNewPayment(); // Incomplete
} else {
  return renderOldPayment(); // Production
}
```

**Rationale:**

- Code integrated immediately
- No merge conflicts
- Can test in staging
- Toggle without deployment

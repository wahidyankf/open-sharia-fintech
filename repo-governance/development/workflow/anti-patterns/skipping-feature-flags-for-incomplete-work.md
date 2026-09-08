---
description: Keeping work on long-lived branches instead of integrating complete-and-inert increments behind temporary production-disabled flags.
when_to_use: Use when incomplete behaviour would otherwise stay on a branch instead of integrating as a complete-and-inert, both-path-tested increment behind a temporary production-disabled flag.
---

# Anti-Pattern: Skipping Feature Flags for Incomplete Work

**Problem**: Keeping incomplete behaviour in long-lived branches instead of integrating an internally
complete-and-inert increment behind a temporary production-disabled flag.

**Bad Example:**

```bash
# Hide incomplete work in branch (DO NOT DO THIS)
git checkout -b feature/new-payment-flow
# Work for 2 months on branch
# Never integrated until "complete"
```

**Solution:**

```javascript
// Both paths are complete and tested; production exposure defaults off during rollout
const FEATURES = {
  NEW_PAYMENT_FLOW: process.env.ENABLE_NEW_PAYMENT === "true",
};

// Commit to main immediately, flag OFF in production
if (FEATURES.NEW_PAYMENT_FLOW) {
  return renderNewPayment(); // Complete enabled path
} else {
  return renderOldPayment(); // Complete disabled path
}
```

**Rationale:**

- Code integrated immediately
- No merge conflicts
- Can test in staging
- Toggle without deployment
- Rollout, rollback, and flag removal remain explicit

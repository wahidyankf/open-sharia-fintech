---
title: "Practice 4: Use Feature Flags Instead of Long-Lived Branches"
description: Keep incomplete behavior complete-and-inert behind temporary production-disabled feature flags, not branches.
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: Use when incomplete behavior must merge as a complete-and-inert, both-path-tested increment without production exposure, with rollout, rollback, and removal recorded.
---

# Practice 4: Use Feature Flags Instead of Long-Lived Branches

**Principle**: Integrate incomplete behavior only as an internally complete-and-inert increment
behind a temporary feature flag disabled in production by default. Both paths must pass, and the
rollout, rollback, and removal must be recorded.

**Good Example:**

```javascript
// config/features.js
const FEATURES = {
  NEW_DASHBOARD: process.env.ENABLE_NEW_DASHBOARD === "true",
};

// In code
if (FEATURES.NEW_DASHBOARD) {
  return renderNewDashboard(); // Complete and tested; exposure remains disabled during rollout
} else {
  return renderOldDashboard(); // Tested disabled path remains production-ready
}
```

**Bad Example:**

```bash
# Long-lived feature branch (DO NOT DO THIS)
git checkout -b feature/new-dashboard
# ... work for 2 weeks on branch ...
# Massive merge conflicts when ready to merge!
```

**Rationale:**

- Code integrated immediately
- No merge conflicts
- Can toggle features without deployment
- Gradual rollouts
- Enabled and disabled behavior stays tested, with an explicit rollback and flag-removal path

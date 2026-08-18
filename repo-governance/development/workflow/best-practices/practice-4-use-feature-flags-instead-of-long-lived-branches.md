---
title: "Practice 4: Use Feature Flags Instead of Long-Lived Branches"
description: Hide incomplete work with feature flags, not branches.
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: Use when incomplete work needs to merge to main without being visible in production yet.
---

# Practice 4: Use Feature Flags Instead of Long-Lived Branches

**Principle**: Hide incomplete work with feature flags, not branches.

**Good Example:**

```javascript
// config/features.js
const FEATURES = {
  NEW_DASHBOARD: process.env.ENABLE_NEW_DASHBOARD === "true",
};

// In code
if (FEATURES.NEW_DASHBOARD) {
  return renderNewDashboard(); // Incomplete, hidden in production
} else {
  return renderOldDashboard(); // Production-ready
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

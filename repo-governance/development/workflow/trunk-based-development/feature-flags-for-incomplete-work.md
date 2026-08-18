---
title: "Feature Flags for Incomplete Work"
description: Feature-flag patterns (boolean, environment-based, user-based) for hiding incomplete work in production instead of using branches, and the flag lifecycle.
category: explanation
subcategory: development
tags:
  - trunk-based-development
  - git
  - workflow
  - development
  - continuous-integration
created: 2025-11-26
when_to_use: Use when hiding incomplete work behind a toggle instead of a branch, or retiring a flag once a feature is stable.
---

# Feature Flags for Incomplete Work

**Instead of hiding incomplete features in branches, use feature flags (toggles) to hide them in production.**

**Why feature flags?**

- Code is integrated immediately (prevents merge conflicts)
- Incomplete features don't affect production users
- Can toggle features on/off without deployments
- Enables testing in production environments
- Allows gradual rollouts and A/B testing

**Feature flag patterns**:

## Simple Boolean Flag

```javascript
// config/features.js
const FEATURES = {
  NEW_DASHBOARD: process.env.ENABLE_NEW_DASHBOARD === "true",
  ADVANCED_SEARCH: process.env.ENABLE_ADVANCED_SEARCH === "true",
};

// In code
if (FEATURES.NEW_DASHBOARD) {
  // Show new dashboard (incomplete, under development)
  return renderNewDashboard();
} else {
  // Show old dashboard (production-ready)
  return renderOldDashboard();
}
```

## Environment-Based Flags

```javascript
// Only enable in development/staging
const FEATURE_ENABLED = ["development", "staging"].includes(process.env.NODE_ENV);

if (FEATURE_ENABLED) {
  // New feature code (not ready for production)
}
```

## User-Based Flags

```javascript
// Enable for specific users (beta testers)
const betaUsers = ["user1@example.com", "user2@example.com"];

if (betaUsers.includes(currentUser.email)) {
  // Show beta feature
}
```

**Feature flag lifecycle**:

1. **Add flag**: Create flag for new feature
2. **Develop with flag OFF in prod**: Commit to `main`, flag hides feature in production
3. **Test with flag ON in staging**: Verify feature works in non-production
4. **Enable in production**: Flip flag when feature is complete
5. **Remove flag**: After feature is stable, remove flag and old code path

**Important**: Feature flags are temporary. Once a feature is stable, remove the flag and delete the old code path. Don't accumulate flags indefinitely.

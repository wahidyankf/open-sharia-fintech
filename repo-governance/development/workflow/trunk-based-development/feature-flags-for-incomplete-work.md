---
description: Feature-flag patterns for complete-and-inert increments, production-disabled defaults, both-path testing, and rollout, rollback, and removal.
when_to_use: Use when incomplete behaviour must integrate safely behind a temporary production-disabled toggle, or when rolling back or retiring that flag.
---

# Feature Flags for Incomplete Work

**Instead of hiding incomplete features in long-lived branches, integrate complete-and-inert
increments behind temporary feature flags disabled in production by default.** Every merged state
must remain safe to deploy to production immediately. The enabled path must work as implemented;
the flag controls exposure, not whether broken or internally incomplete code is acceptable.

**Why feature flags?**

- Code is integrated immediately (prevents merge conflicts)
- Production-disabled complete increments do not affect production users
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
  // Show the internally complete increment while exposure is enabled.
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
  // Exercise the complete increment without exposing it in production.
}
```

## User-Based Flags

```javascript
// Enable for specific users (beta testers)
const betaUsers = ["user1@example.com", "user2@example.com"];

if (betaUsers.includes(currentUser.email)) {
  // Show the complete increment to an authorized beta cohort.
}
```

**Feature flag lifecycle**:

1. **Add flag**: Create a temporary flag whose production default is off
2. **Integrate complete-and-inert increments**: Commit to `main` only after the enabled and disabled
   paths are safe, tested, and production-deployable
3. **Test with flag ON in staging**: Verify the enabled feature works in non-production
4. **Enable in production**: Flip flag when feature is complete
5. **Remove flag**: After feature is stable, remove flag and old code path

**Important**: Record rollout, rollback, and flag removal when introducing the flag. Feature flags
are temporary. Once a feature is stable, remove the flag and delete the old code path. Don't
accumulate flags indefinitely.

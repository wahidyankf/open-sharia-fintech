# Trunk-Based Development — Feature Flags for Incomplete Work

## What are Feature Flags?

**Feature flags** (feature toggles) are runtime switches that enable/disable features without code changes.

**Purpose**: Hide incomplete work on `main` until ready for users.

## Basic Pattern

```javascript
// Define feature flag (in config or env vars)
const FEATURE_FLAGS = {
  newCheckout: false, // Feature under development
  betaAnalytics: true, // Feature in beta testing
};

// Use flag to conditionally enable feature
function renderCheckout() {
  if (FEATURE_FLAGS.newCheckout) {
    return <NewCheckoutFlow />; // New implementation
  } else {
    return <OldCheckoutFlow />; // Stable implementation
  }
}
```

## Feature Flag Lifecycle

**1. Development Phase** (flag = false):

- Commit new code to `main` with flag disabled
- Code deployed but not executed
- Safe to push incomplete work

**2. Testing Phase** (flag = true for testers):

- Enable flag for internal testing
- Users don't see changes yet
- Iterate based on feedback

**3. Release Phase** (flag = true for everyone):

- Enable flag for all users
- Feature now live
- Monitor for issues

**4. Cleanup Phase** (remove flag):

- After stability confirmed, remove flag and old code
- Simplify codebase
- One path remains

## Feature Flag Best Practices

**DO**:

- Use flags for multi-day features
- Keep flags simple (boolean toggles)
- Document flag purpose and timeline
- Remove flags after feature stable (don't accumulate)
- Test both paths (flag on and off)

**DON'T**:

- Use flags for trivial single-commit changes
- Create complex flag hierarchies
- Keep flags indefinitely (technical debt)
- Forget to test flag-disabled path
- Use flags as permanent configuration

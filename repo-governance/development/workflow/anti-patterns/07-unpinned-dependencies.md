---
title: "Anti-Pattern: Unpinned Dependencies"
description: Not locking dependency versions or committing the lockfile causes inconsistent builds.
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: Use when adding a dependency or configuring version pinning and lockfile commits.
---

# Anti-Pattern: Unpinned Dependencies

**Problem**: Not locking dependency versions causes "works on my machine" issues.

**Bad Example:**

```json
// package.json
{
  "dependencies": {
    "react": "^18.0.0"  // Unpinned - different versions!
  }
}

// .gitignore
package-lock.json  # NOT COMMITTED - WRONG!
```

**Solution:**

```json
// package.json
{
  "volta": {
    "node": "24.13.1",
    "npm": "11.10.1"
  },
  "dependencies": {
    "react": "18.2.0"  // Exact version
  }
}

// Commit package-lock.json
git add package-lock.json
```

**Rationale:**

- Consistent builds
- No version surprises
- Reproducible CI/CD
- Reliable deployments

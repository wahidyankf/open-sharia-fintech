---
title: "Practice 6: Pin Dependencies for Reproducibility"
description: Lock versions using package-lock.json and Volta.
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: Use when adding a dependency or configuring runtime/tool version pinning.
---

# Practice 6: Pin Dependencies for Reproducibility

**Principle**: Lock versions using package-lock.json and Volta.

**Good Example:**

```json
// package.json
{
  "volta": {
    "node": "24.13.1",
    "npm": "11.10.1"
  }
}

// Committed: package-lock.json (exact versions)
```

**Bad Example:**

```json
// package.json
{
  "dependencies": {
    "react": "^18.0.0"  // Unpinned - different versions on different machines!
  }
}

// .gitignore
package-lock.json  # NOT COMMITTED - WRONG!
```

**Rationale:**

- Consistent builds across machines
- No "works on my machine" issues
- Reproducible CI/CD
- Reliable dependency versions

---
title: "Anti-Pattern: Premature Optimization"
description: Optimizing before the implementation works wastes effort and skips the make-it-work step.
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: Use when planning to design caching or micro-optimizations before a basic working implementation exists.
---

# Anti-Pattern: Premature Optimization

**Problem**: Optimizing before implementation works.

**Bad Example:**

```markdown
## Implementation Plan (WRONG)

1. Design complex caching system
2. Implement micro-optimizations
3. Build feature (maybe it works?)
```

**Solution:**

```markdown
## Implementation Plan (CORRECT)

1. Make it work (basic implementation)
2. Make it right (refactor, organize)
3. Make it fast (profile, optimize)
```

**Rationale:**

- Working code first
- Avoid wasted optimization
- Measure before optimizing
- Clearer progression

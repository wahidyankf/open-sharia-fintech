---
title: "Practice 5: Implement in Three Stages"
description: Make it work, then make it right, then make it fast.
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: Use when planning implementation order for a new feature, to sequence correctness before optimization.
---

# Practice 5: Implement in Three Stages

**Principle**: Make it work → Make it right → Make it fast.

**Good Example:**

```markdown
## Stage 1: Make it work

- Implement basic functionality
- Get tests passing
- Commit working code

## Stage 2: Make it right

- Refactor for clarity
- Improve code organization
- Add documentation

## Stage 3: Make it fast

- Profile for bottlenecks
- Optimize hot paths
- Measure improvements
```

**Bad Example:**

```markdown
# Premature optimization (DO NOT DO THIS)

## Stage 1: Make it fast

- Optimize before implementation
- Complex micro-optimizations
- Code that doesn't work yet
```

**Rationale:**

- Working code first
- Avoid premature optimization
- Incremental improvement
- Clear progression

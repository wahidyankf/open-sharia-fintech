---
description: Common progressive-disclosure mistakes - front-loading complexity, no starting point, and all-or-nothing docs.
when_to_use: Use when auditing content for complexity that overwhelms beginners.
---

# Anti-Patterns

## Front-Loading Complexity

FAIL: **Problem**: Teaching advanced concepts before basics.

```markdown
# React Tutorial

## Advanced Patterns: Higher-Order Components

Before we learn basic components, let's understand HoCs...
```

**Why it's bad**: Beginners need basics first. HoCs require understanding components.

## No Clear Starting Point

FAIL: **Problem**: Documentation without "start here" guidance.

```
docs/
  advanced-optimization.md
  architecture-patterns.md
  basic-setup.md
  getting-started.md
  reference-api.md
```

**Why it's bad**: Unclear reading order. No indication of difficulty level.

## All-or-Nothing Documentation

FAIL: **Problem**: Either 10-page reference manual or nothing.

**No middle ground**: No quick start, no intermediate guides.

**Why it's bad**: Beginners overwhelmed, practitioners lack practical examples.

## Requiring Expert Knowledge for Basics

FAIL: **Problem**: Basic tasks require understanding internals.

```markdown
## Creating a Component

First, understand the reconciliation algorithm and virtual DOM diffing...
```

**Why it's bad**: Unnecessary complexity for basic tasks.

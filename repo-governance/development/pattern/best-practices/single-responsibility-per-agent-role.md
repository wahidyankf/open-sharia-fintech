---
title: "Practice 1: Single Responsibility Per Agent Role"
description: "Each agent in Maker-Checker-Fixer should have exactly one clear responsibility - create, validate, or fix."
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: "Use when designing a new agent or reviewing whether an existing agent mixes maker/checker/fixer responsibilities."
---

# Practice 1: Single Responsibility Per Agent Role

**Principle**: Each agent in Maker-Checker-Fixer has one clear responsibility.

**Good Example:**

```yaml
# Maker - Creates content only
---
name: docs-maker
description: Creates documentation following conventions
tools: [Read, Write, Glob]
---
# Checker - Validates content only
---
name: docs-checker
description: Validates documentation quality
tools: [Read, Glob, Grep, Write, Bash]
---
# Fixer - Applies fixes only
---
name: docs-fixer
description: Applies validated fixes
tools: [Read, Edit, Glob, Grep, Write, Bash]
---
```

**Bad Example:**

```yaml
# God agent (DO NOT DO THIS)
---
name: docs-everything
description: Creates, validates, and fixes documentation
tools: [Read, Write, Edit, Glob, Grep, Bash]
---
```

**Rationale:**

- Clear separation of concerns
- Easier to test and maintain
- Reusable across workflows
- Prevents responsibility overlap

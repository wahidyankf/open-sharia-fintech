---
title: "Anti-Pattern 1: God Agent in Maker-Checker-Fixer"
description: "A single agent tries to create, validate, and fix content instead of using separate maker/checker/fixer agents."
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: "Use when designing or reviewing an agent that both creates and validates its own content."
---

# Anti-Pattern 1: God Agent in Maker-Checker-Fixer

**Problem**: Single agent trying to create, validate, and fix content.

**Bad Example:**

```yaml
---
name: docs-everything
description: Creates, validates, and fixes documentation
tools: [Read, Write, Edit, Glob, Grep, Bash, WebFetch]
---
```

**Solution:**

```yaml
# Separate agents with single responsibilities
---
name: docs-maker
tools: [Read, Write, Glob]
---
---
name: docs-checker
tools: [Read, Glob, Grep, Write, Bash]
---
---
name: docs-fixer
tools: [Read, Edit, Glob, Grep, Write, Bash]
---
```

**Rationale:**

- Single responsibility per agent
- Easier to test and maintain
- Clear workflow boundaries
- Reusable across different contexts

---
title: "Practice 2: Use Makers for User-Driven Content Creation"
description: "Invoke a maker agent when the user explicitly requests content creation or updates."
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: "Use when deciding which agent to invoke for a user-driven content creation or update request."
---

# Practice 2: Use Makers for User-Driven Content Creation

**Principle**: Invoke makers when user requests content creation or updates.

**Good Example:**

```markdown
User: "Create new tutorial about Docker"
→ Use docs-maker (user-driven creation)

User: "Add section on volumes to Docker tutorial"
→ Use docs-maker (user-driven update)
```

**Bad Example:**

```markdown
User: "Create new tutorial about Docker"
→ Use docs-fixer (WRONG - fixer is validation-driven, not user-driven!)
```

**Rationale:**

- Makers handle comprehensive creation
- Makers update all dependencies
- Makers provide production-ready content
- Clear workflow boundaries

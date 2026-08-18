---
title: "How It Applies — Frontmatter, Dependencies, and Configuration"
description: Explicit-vs-implicit examples for frontmatter, dependencies, and config files.
category: explanation
subcategory: principles
tags:
  - principles
  - explicit-configuration
  - transparency
  - clarity
created: 2025-12-15
when_to_use: Use when reviewing frontmatter, an import statement, or a config file.
---

# How It Applies — Frontmatter, Dependencies, and Configuration

Continues [How It Applies](./how-it-applies.md).

## Frontmatter Fields

**Context**: Document metadata in YAML frontmatter.

PASS: **Explicit (Correct)**:

```yaml
---
title: "Explicit Over Implicit"
description: Choose explicit composition over magic
category: explanation
subcategory: principles
tags:
  - principles
  - explicit-configuration
created: 2025-12-15
---
```

**Why this works**: All fields present. No guessing about category, tags, or dates. Self-contained.

FAIL: **Implicit (Avoid)**:

```yaml
---
title: "Explicit Over Implicit"
---
```

**Why this fails**: Missing category, tags, dates. Relies on defaults or context. Not self-documenting.

## Dependency Declaration

**Context**: Code imports and dependencies.

PASS: **Explicit (Correct)**:

```typescript
import { validateEmail } from "@open-sharia-enterprise/ts-validation";
import { createUser } from "./user-service";
```

**Why this works**: Clear dependency on validation library and local service. Path mappings defined in `tsconfig.base.json`. Traceable.

FAIL: **Implicit (Avoid)**:

```typescript
// Assumes global validateEmail function exists
// Assumes user-service is somehow available
```

**Why this fails**: Hidden dependencies. Requires knowledge of globals or auto-imports. Breaks silently.

## Configuration Files

**Context**: Application configuration.

PASS: **Explicit (Correct)**:

```json
{
  "api": {
    "baseUrl": "https://api.example.com",
    "timeout": 5000,
    "retries": 3
  }
}
```

**Why this works**: All settings visible. No hidden defaults. Behavior is predictable.

FAIL: **Implicit (Avoid)**:

```json
{
  "api": {
    "baseUrl": "https://api.example.com"
  }
}
```

**Why this fails**: What's the timeout? How many retries? Relies on code defaults. Behavior unclear from config.

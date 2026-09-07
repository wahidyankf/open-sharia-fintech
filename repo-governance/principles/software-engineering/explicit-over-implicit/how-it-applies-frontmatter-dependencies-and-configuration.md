---
description: Explicit-vs-implicit examples for frontmatter, dependencies, and config files.
when_to_use: Use when reviewing frontmatter, an import statement, or a config file.
---

# How It Applies — Frontmatter, Dependencies, and Configuration

Continues [How It Applies](./how-it-applies.md).

## Frontmatter Fields

**Context**: Document metadata in YAML frontmatter.

PASS: **Explicit (Correct)**:

```yaml
---
description: Choose explicit composition over magic
when_to_use: Use when a choice could be inferred from context and should instead be stated.
---
```

**Why this works**: Both fields present. The reader is told what the document covers _and_ when to
reach for it, rather than inferring the second from the first.

FAIL: **Implicit (Avoid)**:

```yaml
---
description: Choose explicit composition over magic
---
```

**Why this fails**: Missing `when_to_use`. The routing condition is left to be guessed from the
description, which is what "implicit" means here.

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

**Why this works**: All settings visible. No hidden defaults. Behaviour is predictable.

FAIL: **Implicit (Avoid)**:

```json
{
  "api": {
    "baseUrl": "https://api.example.com"
  }
}
```

**Why this fails**: What's the timeout? How many retries? Relies on code defaults. Behaviour unclear from config.

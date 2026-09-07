---
description: Five best practices for explicitness.
when_to_use: Use when designing a new agent, module, or config schema.
---

# PASS: Best Practices

## 1. Write It Out

**Don't rely on defaults** - state everything explicitly:

```yaml
---
name: docs-maker
description: Expert documentation writer
tools: Read, Write, Edit, Glob, Grep
model: inherit
color: blue
---
```

All five required fields present. No guessing.

## 2. Make Dependencies Visible

**Import what you use** - don't assume globals:

```typescript
import { logger } from "./logger";
import { config } from "./config";

function processUser(userId: string) {
  logger.info(`Processing user ${userId}`);
  return fetchUser(userId, config.api);
}
```

Dependencies are clear from imports.

## 3. Use Typed Configuration

**Define types for configuration** - make structure explicit:

```typescript
interface ApiConfig {
  baseUrl: string;
  timeout: number;
  retries: number;
}

const config: ApiConfig = {
  baseUrl: "https://api.example.com",
  timeout: 5000,
  retries: 3,
};
```

Type system enforces completeness.

## 4. Document Explicitly

**Don't assume context** - state it in documentation:

```markdown
## Prerequisites

- Node.js 24.13.1 or higher (Volta managed)
- npm 11.10.1 or higher (Volta managed)
- Git 2.40 or higher

These versions are pinned in `package.json` under the `volta` field.
```

Version requirements and their source are explicit.

## 5. Validate Explicitly

**Check assumptions** - don't fail silently:

```typescript
function validateAgent(agent: AgentConfig) {
  if (!agent.name) throw new Error("Agent name is required");
  if (!agent.tools || agent.tools.length === 0) {
    throw new Error("Agent must specify at least one tool");
  }
  // Explicit validation, not implicit assumptions
}
```

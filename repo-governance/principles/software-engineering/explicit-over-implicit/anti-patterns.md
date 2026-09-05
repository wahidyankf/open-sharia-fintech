---
title: "Anti-Patterns"
description: Four implicit-behaviour anti-patterns and why each is bad.
category: explanation
subcategory: principles
tags:
  - principles
  - explicit-configuration
  - transparency
  - clarity
created: 2025-12-15
when_to_use: Use when reviewing code for hidden or magic behaviour.
---

# Anti-Patterns

## Magic Conventions

FAIL: **Problem**: Files named `index.ts` auto-import in certain contexts.

```
src/
  utils/
    index.ts  # "Magic" file
```

**Why it's bad**: Requires knowing the framework's auto-import convention. Not explicit.

## Hidden Defaults

FAIL: **Problem**: Agent assumes it has Write access if not specified.

```yaml
---
name: example-agent
# No tools field - assumes defaults
---
```

**Why it's bad**: What tools does it have? Requires reading agent runner code to know.

## Global State

FAIL: **Problem**: Functions rely on global variables.

```typescript
// Somewhere else: global.config = { ... }

function processData(data) {
  // Uses global.config implicitly
  return transform(data, config.settings);
}
```

**Why it's bad**: Hidden dependency on global state. Not visible in function signature.

## Convention-Based Routing

FAIL: **Problem**: File location determines route.

```
pages/
  about.tsx  # Implicitly creates /about route
```

**Why it's bad** (for our context): Route not visible in code. Requires knowing framework conventions. (Note: This is fine in Next.js/Nuxt where it's the standard pattern, but avoid inventing new conventions like this.)

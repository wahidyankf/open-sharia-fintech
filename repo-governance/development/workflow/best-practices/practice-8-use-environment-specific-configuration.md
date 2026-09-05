---
title: "Practice 8: Use Environment-Specific Configuration"
description: Different settings for development vs production, never hardcoded.
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: Use when a value differs between local development and production and needs to be configured rather than hardcoded.
---

# Practice 8: Use Environment-Specific Configuration

**Principle**: Different settings for development vs production.

**Good Example:**

```bash
# Development
NODE_ENV=development npm run dev

# Production
NODE_ENV=production npm run build

# .env.example (committed)
DATABASE_URL=
API_KEY=
```

**Bad Example:**

```bash
# Same config everywhere (DO NOT DO THIS)
const DB_URL = "production-db.example.com";  # Hardcoded!
```

**Rationale:**

- Safe local development
- No production credentials in code
- Environment-specific behaviour
- Follows 12-factor app principles

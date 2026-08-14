---
title: "Anti-Pattern: Hardcoded Environment Configuration"
description: Hardcoding production values in code creates security issues and breaks local development.
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: Use when about to hardcode a database URL, API key, or other environment-specific value in source code.
---

# Anti-Pattern: Hardcoded Environment Configuration

**Problem**: Hardcoding production values in code.

**Bad Example:**

```javascript
// DO NOT DO THIS
const DB_URL = "prod-db.example.com";
const API_KEY = "sk_live_abc123xyz";

// Committed to git - security issue!
// Can't run locally - wrong database!
```

**Solution:**

```javascript
// config.js
const DB_URL = process.env.DATABASE_URL;
const API_KEY = process.env.API_KEY;

// .env.example (committed)
DATABASE_URL=
API_KEY=

// .env (gitignored, local values)
DATABASE_URL=localhost:5432
API_KEY=sk_test_local
```

**Rationale:**

- No secrets in code — see
  [No Secrets in Git Convention](../../../conventions/security/no-secrets-in-committed-files.md) for the full hard
  iron rule governing all git-tracked files, not just source code
- Environment-specific config
- Safe local development
- 12-factor app compliance

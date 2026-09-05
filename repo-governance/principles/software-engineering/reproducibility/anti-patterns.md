---
title: "Anti-Patterns"
description: Catalogs common reproducibility anti-patterns — "works on my machine", floating dependencies, undocumented system dependencies, and manual setup — with fixes.
category: explanation
subcategory: principles
tags:
  - principles
  - reproducibility
  - environment
  - determinism
  - version-pinning
created: 2025-12-28
when_to_use: Use when diagnosing an environment-specific bug or refactoring an undocumented manual setup process.
---

# Anti-Patterns

## "Works on My Machine"

FAIL: **Problem**: Code works locally but fails in CI/production.

```bash
# Developer's machine
node --version  # v24.13.1 (local)
npm test        # PASS: All pass

# CI server
node --version  # v20.x (different)
npm test        # FAIL: Failures
```

**Why it's bad**: Different environments = different behaviour. Wastes time debugging environment instead of code.

PASS: **Solution**: Use Volta to pin versions across all environments.

## Floating Dependencies

FAIL: **Problem**: Different dependency versions on each install.

```json
// package.json
{
  "dependencies": {
    "express": "^4.0.0"
  }
}
// No package-lock.json in git

// Monday: npm install gets express@4.18.0
// Friday: npm install gets express@4.19.0 (patch release)
// Different behaviour
```

**Why it's bad**: Non-deterministic. Builds differ. Hard to debug.

PASS: **Solution**: Commit `package-lock.json`. Use `npm ci` in CI.

## Undocumented System Dependencies

FAIL: **Problem**: Code requires specific system packages but doesn't document them.

```typescript
// Uses native crypto library
import crypto from "crypto";

// Developer A: Has OpenSSL 3.x - works
// Developer B: Has OpenSSL 1.1 - fails
// No documentation of requirement
```

**Why it's bad**: Contributors waste time discovering hidden dependencies.

PASS: **Solution**: Document system dependencies in README.

```markdown
## System Requirements

- OpenSSL 3.x or higher
- Python 3.11 (for node-gyp native builds)
```

## Manual Environment Setup

FAIL: **Problem**: Complex manual steps required.

```bash
# Undocumented tribal knowledge
# 1. Install Node.js 24.x
# 2. Install specific version of Python for node-gyp
# 3. Set environment variable XYZ
# 4. Download file from internal server
# 5. Configure obscure setting

# Only senior developers know all steps
```

**Why it's bad**: High barrier to contribution. Knowledge silos.

PASS: **Solution**: Automate with scripts or containers.

```bash
# setup.sh
./scripts/install-dependencies.sh
./scripts/configure-environment.sh
./scripts/seed-database.sh
```

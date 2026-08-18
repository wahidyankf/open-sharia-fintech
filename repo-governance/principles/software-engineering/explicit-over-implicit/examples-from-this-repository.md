---
title: "Examples from This Repository"
description: This repository's concrete explicit configurations.
category: explanation
subcategory: principles
tags:
  - principles
  - explicit-configuration
  - transparency
  - clarity
created: 2025-12-15
when_to_use: Use to find an existing explicit configuration to reuse or extend.
---

# Examples from This Repository

## Git Hook Configuration

**Location**: `.husky/pre-commit`

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

npx lint-staged
```

**Explicit behavior**:

- Hook triggers on pre-commit
- Runs `npx lint-staged` command
- No hidden magic
- Behavior visible in file

## Prettier Configuration

**Location**: `package.json` (lint-staged)

```json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx,mjs,cjs}": "prettier --write",
    "*.json": "prettier --write",
    "*.md": "prettier --write",
    "*.{yml,yaml}": "prettier --write",
    "*.{css,scss}": "prettier --write"
  }
}
```

**Explicit behavior**:

- File patterns explicitly listed
- Command explicitly stated
- No "format all files" magic
- Only staged files processed

## Nx Path Mappings

**Location**: `tsconfig.base.json`

```json
{
  "compilerOptions": {
    "paths": {
      "@open-sharia-enterprise/ts-validation": ["libs/ts-validation/src/index.ts"]
    }
  }
}
```

**Explicit behavior**:

- Path alias explicitly mapped
- Exact file path specified
- No convention-based discovery
- Behavior traceable

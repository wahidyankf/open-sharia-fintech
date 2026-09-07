---
description: "How lint-staged runs formatters/linters on staged files."
when_to_use: "Use when configuring or debugging lint-staged."
---

# Lint-staged

**Purpose**: Run linters and formatters only on staged files (not the entire codebase).

**Configuration** (in `package.json`):

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

**How It Works**:

1. Identifies files staged for commit (`git add`)
2. Runs Prettier on matching file types
3. Automatically stages formatted files
4. Allows commit to proceed if successful

**Benefits**:

- Faster than running tools on entire codebase
- Only formats files you're committing
- Prevents incorrectly formatted code from being committed

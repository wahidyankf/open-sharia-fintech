---
description: Demonstrates this repository's own Volta pinning, committed lockfile, documented setup, and automated git hooks as evidence of reproducibility.
when_to_use: Use when pointing to a concrete, working example of reproducibility already applied in this repository.
---

# Example from This Repository

**Evidence of Reproducibility First**:

## 1. Volta Configuration

```json
// package.json
{
  "volta": {
    "node": "24.13.1",
    "npm": "11.10.1"
  }
}
```

**Result**: All developers and CI use identical Node.js and npm versions.

## 2. Lockfile Committed

```bash
git ls-files | grep lock
package-lock.json
```

**Result**: Deterministic dependency installation with `npm ci`.

## 3. Documented Setup

```markdown
## Environment Setup (from AGENTS.md)

The project uses **Volta** for Node.js and npm version management:

- Node.js: 24.13.1 (LTS)
- npm: 11.10.1

These versions are pinned in package.json under the volta field.
```

**Result**: Clear instructions for new contributors.

## 4. Automated Git Hooks

```bash
# Husky hooks install automatically
npm install
# Hooks configured consistently for all developers
```

**Result**: Same git hooks for everyone after `npm install`.

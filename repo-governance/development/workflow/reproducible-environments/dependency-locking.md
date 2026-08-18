---
title: "Dependency Locking"
description: Lockfile discipline — npm ci over npm install, CI lockfile-freshness checks, and lockfile PR review practices.
category: explanation
subcategory: development
tags:
  - development
  - reproducibility
  - volta
  - docker
  - environment
  - dependencies
created: 2025-12-28
when_to_use: Use when installing dependencies, wiring CI lockfile checks, or reviewing a PR that changes package-lock.json.
---

# Dependency Locking

## Package Lockfiles

**package-lock.json ensures deterministic installs**:

- Locks exact versions of all dependencies
- Locks exact versions of sub-dependencies
- Ensures identical dependency tree across machines
- Must be committed to git

## Using npm ci

**Prefer npm ci over npm install**:

```bash
# PASS: Development: Install from lockfile
npm ci

# FAIL: Avoid in automated environments
npm install  # May update lockfile
```

**Why npm ci**:

- Installs exactly what's in package-lock.json
- Deletes node_modules before install (clean slate)
- Fails if package.json and lockfile don't match
- Faster than npm install
- Deterministic (same result every time)

## CI/CD Configuration

**Enforce lockfile freshness**:

```yaml
# .github/workflows/ci.yml
- name: Install dependencies
  run: npm ci

- name: Check lockfile is up-to-date
  run: |
    npm install --package-lock-only
    git diff --exit-code package-lock.json
```

**What this does**:

- npm ci installs from lockfile
- npm install --package-lock-only regenerates lockfile
- git diff fails if lockfile changed (package.json and lockfile out of sync)

## Lockfile Best Practices

**Always commit lockfiles**:

```bash
git add package-lock.json
git commit -m "chore: update dependencies"
```

**Never gitignore lockfiles**:

```bash
# FAIL: DO NOT add to .gitignore
# package-lock.json
```

**Review lockfile changes in PRs**:

- Large lockfile changes may indicate major dependency updates
- Check for unexpected version bumps
- Verify sub-dependency changes don't introduce vulnerabilities

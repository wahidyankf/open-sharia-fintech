---
description: Shows reproducible patterns for Volta-based version pinning, lockfile-based dependency installs, and explicit dependency version ranges.
when_to_use: Use when pinning a runtime version or dependency and needing a concrete reproducible-versus-floating example.
---

# How It Applies

## Version Pinning with Volta

**Context**: Ensuring consistent Node.js and npm versions.

PASS: **Reproducible (Our Approach)**:

```json
// package.json
{
  "name": "open-sharia-enterprise",
  "volta": {
    "node": "24.13.1",
    "npm": "11.10.1"
  }
}
```

**Why this works**:

- Volta automatically uses specified versions when entering directory
- All developers get Node.js 24.13.1 and npm 11.10.1
- CI/CD uses same versions
- No manual version management needed

FAIL: **Non-reproducible (Avoid)**:

```bash
# FAIL: Just use whatever Node.js you have installed
node --version  # Developer A: v20.x
node --version  # Developer B: v22.x
node --version  # CI: v23.x

# Different behaviour across environments
```

**Why this fails**: Different Node.js versions have different APIs, bugs, performance characteristics. Code works differently on each system.

## Lockfiles for Deterministic Dependencies

**Context**: Ensuring identical dependency trees.

PASS: **Reproducible (Required)**:

```bash
# Install from lockfile - exact versions
npm ci

# Lockfile in git - committed
git add package-lock.json
git commit -m "chore: update dependencies"
```

**Why this works**: `package-lock.json` locks exact versions of all dependencies and sub-dependencies. `npm ci` installs exactly what's in lockfile.

FAIL: **Non-reproducible (Avoid)**:

```bash
# FAIL: Install from package.json - floating versions
npm install  # Gets latest within semver range

# FAIL: Lockfile gitignored
echo "package-lock.json" >> .gitignore
```

**Why this fails**:

- `npm install` may install different versions on different machines
- Without lockfile in git, each developer gets different dependency tree
- "Works on my machine" because you have different versions

## Explicit Version Ranges

**Context**: Specifying dependency versions in package.json.

PASS: **Reproducible (Recommended)**:

```json
{
  "dependencies": {
    "@nrwl/react": "19.0.0",
    "react": "18.2.0",
    "react-dom": "18.2.0"
  },
  "devDependencies": {
    "prettier": "3.1.0",
    "husky": "8.0.3"
  }
}
```

**Why this works**: Exact versions mean lockfile is more stable. Upgrades are deliberate, not accidental.

**Acceptable with lockfile**:

```json
{
  "dependencies": {
    "react": "^18.2.0"
  }
}
```

**Why this is acceptable**: With `package-lock.json` committed, everyone gets same version. `^` allows patch updates when you run `npm update`.

FAIL: **Non-reproducible (Avoid)**:

```json
{
  "dependencies": {
    "react": "*",
    "express": "latest"
  }
}
```

**Why this fails**: `*` and `latest` mean "any version". Completely non-deterministic.

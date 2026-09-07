---
description: How Volta pins and auto-switches Node.js/npm versions per project, plus installation and CI/CD integration.
when_to_use: Use when pinning, installing, updating, or wiring Volta-managed Node.js/npm versions into CI.
---

# Runtime Version Management with Volta

## Why Volta

**Volta automatically manages Node.js and npm versions** per project:

- Versions specified in package.json
- Auto-switches when entering directory
- No manual version switching (nvm, asdf)
- Works on macOS, Linux, Windows
- Team members get same versions automatically

## Configuration

**package.json volta field**:

```json
{
  "name": "open-sharia-enterprise",
  "volta": {
    "node": "24.13.1",
    "npm": "11.10.1"
  }
}
```

**What happens**:

```bash
cd open-sharia-enterprise
# Volta automatically activates Node.js 24.13.1 and npm 11.10.1

node --version  # v24.13.1 (same for everyone)
npm --version   # 11.10.1 (same for everyone)
```

## Installation

**One-time setup for contributors**:

```bash
# Install Volta
curl https://get.volta.sh | bash

# Clone repository
git clone https://github.com/wahidyankf/ose-public.git
cd open-sharia-enterprise

# Volta auto-installs pinned Node.js/npm versions
# No manual version management needed
```

## CI/CD Integration

**GitHub Actions example**:

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # Install Volta
      - uses: volta-cli/action@v4

      # Volta uses versions from package.json
      - run: node --version # v24.13.1
      - run: npm --version # 11.10.1

      # Install dependencies
      - run: npm ci

      # Run tests with exact same environment as local
      - run: npm test
```

## When to Update Versions

**Update Node.js/npm when**:

- Security vulnerabilities in current versions
- New LTS release available
- Features needed from newer version
- Dependency requires newer runtime

**Update process**:

```bash
# Test with new version locally
volta pin node@24.12.0
npm test

# If tests pass, commit updated package.json
git add package.json
git commit -m "chore: update Node.js to 24.12.0"
```

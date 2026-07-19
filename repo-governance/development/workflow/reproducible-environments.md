---
title: Reproducible Environments
description: Practices for creating consistent, reproducible development and build environments
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
---

# Reproducible Environments

Practices for creating consistent, reproducible development and build environments. This document defines HOW to implement reproducibility across runtime versions, dependencies, configuration, and infrastructure.

## Principles Implemented/Respected

This practice respects the following core principles:

- **[Reproducibility First](../../principles/software-engineering/reproducibility.md)**: All environment configuration is explicit, version-controlled, and reproducible. Eliminates "works on my machine" problems through deterministic setup.

- **[Automation Over Manual](../../principles/software-engineering/automation-over-manual.md)**: Environment setup automated through version managers (Volta), lockfiles, scripts, and containers. Manual setup steps eliminated or documented.

- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**: Runtime versions pinned explicitly (package.json volta field). Dependencies locked with exact versions (package-lock.json). No implicit system dependencies.

- **[Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md)**: Use simple, proven tools (Volta, npm lockfiles, Docker) instead of complex custom solutions. Minimum configuration for maximum reproducibility.

## Conventions Implemented/Respected

This practice implements/respects the following conventions:

- **[Code Quality Convention](../quality/code.md)**: Reproducible environments enable consistent automated quality checks. Same Node.js/npm versions mean same Prettier, ESLint, and test results across machines.

- **[Trunk Based Development](./trunk-based-development.md)**: Reproducible CI/CD environments ensure consistent validation of commits to main branch. No environment-specific failures.

- **[No Secrets in Git Convention](../../conventions/security/no-secrets-in-committed-files.md)**: The `.env.example` template carries placeholders only; real secret values stay in uncommitted `.env*` files, keeping secrets out of version control while configuration shape remains reproducible.

## Overview

Reproducible environments require:

1. **Runtime version management**: Volta for Node.js/npm pinning
2. **Dependency locking**: package-lock.json for deterministic installs
3. **Configuration management**: .env.example for required environment variables
4. **Container definitions**: Docker/docker-compose for complex setups
5. **Documentation**: Clear setup instructions for onboarding

## Runtime Version Management with Volta

### Why Volta

**Volta automatically manages Node.js and npm versions** per project:

- Versions specified in package.json
- Auto-switches when entering directory
- No manual version switching (nvm, asdf)
- Works on macOS, Linux, Windows
- Team members get same versions automatically

### Configuration

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

### Installation

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

### CI/CD Integration

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

### When to Update Versions

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

## Dependency Locking

### Package Lockfiles

**package-lock.json ensures deterministic installs**:

- Locks exact versions of all dependencies
- Locks exact versions of sub-dependencies
- Ensures identical dependency tree across machines
- Must be committed to git

### Using npm ci

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

### CI/CD Configuration

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

### Lockfile Best Practices

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

## Shared Cargo Target Directories

`npm run doctor -- --fix` provisions a shared cargo build-artifact cache for local development, in addition to the toolchain convergence described in [Worktree Toolchain Initialization](./worktree-setup.md). This mechanism targets build-artifact reuse across worktrees of the same repo — it does not change dependency resolution, which remains governed by `Cargo.lock`.

### Symlink Mechanism and Cache Root

For each Rust crate, `rhino-cli doctor --fix` creates a `target/` symlink that points into a shared cache instead of leaving `target/` as an ordinary crate-local directory. The symlink target follows this layout:

```text
<cache_root>/<repo_name>/<crate_leaf>
```

- **Cache root**: defaults to `$HOME/.cache/ose-cargo-target`, overridable with the `OSE_CARGO_TARGET_CACHE` environment variable.
- **`<repo_name>`**: derived from the git common directory, so every worktree of the same repository resolves to the same cache namespace and shares build artifacts across worktrees.
- **`<crate_leaf>`**: the crate's own path segment, so distinct crates in the same repo never collide in the shared cache.

This is a **local-development-only** mechanism, reducing redundant compilation when multiple worktrees of the same repo build the same crates.

### CI Guard

Under CI (detected via the `CI` or `GITHUB_ACTIONS` environment variable), the doctor target-share step is a no-op — it never creates a symlink on CI runners, and reports "CI detected — skipped." CI runners keep an ordinary, isolated `target/` directory per job.

### Worktree-Aware Pruning (`doctor --prune-cargo-cache`)

`rhino-cli doctor --prune-cargo-cache` is a worktree-aware garbage collector for the shared cache. It deletes shared-cache entries that no live worktree or checkout of the repo references any more. Use `--dry-run` to preview candidate deletions without deleting anything. Like the target-share step, pruning is a no-op under CI.

**Anti-pattern — no per-worktree delete hook.** Removing a git worktree (`git worktree remove`) deliberately does NOT delete that worktree's shared-cache entry. The shared cache is keyed by crate, not by worktree, so other worktrees may still reference the same entry after one worktree is removed. Reclaiming shared-cache space happens exclusively through the explicit, worktree-aware `doctor --prune-cargo-cache` GC — never as a side effect of worktree removal.

### Cleanup Path

Two complementary cleanup mechanisms apply:

- **`cargo clean`**: per-crate, standard Cargo cleanup, unaffected by the shared-cache mechanism.
- **`cargo-sweep`** (optional periodic stale-artifact reclamation): when `cargo-sweep` is installed on `PATH`, the doctor shells out to it with:

  ```bash
  cargo-sweep --time 30 --recursive <cache_root>
  ```

  When `cargo-sweep` is not installed, the doctor degrades gracefully and reports "cargo-sweep not installed — skipped." It is never a hard dependency.

## Environment Configuration

> **Stub.** The full env/secrets standards — naming convention, annotation format, `.env.example`
> layout, startup validation, `rhino-cli env` toolchain, and drift guard — live in
> [`secrets-and-env-standards.md`](../../conventions/security/secrets-and-env-standards.md).

### .env Files (summary)

**Pattern**: Committed template (`apps/<app>/.env.example`), gitignored real file (`.env.local`).

**Hard iron rule**: Real secret values never enter git. `.env.example` (committed template) contains
placeholders only. See:
[`secrets-and-env-standards.md` § 1](../../conventions/security/secrets-and-env-standards.md#1-hard-iron-rule--no-secrets-in-committed-files).

**Backup and restore**: Use `rhino-cli env backup / restore`. See:
[`secrets-and-env-standards.md` § 6](../../conventions/security/secrets-and-env-standards.md#6-rhino-cli-env-toolchain).

## Containerization for Complex Environments

### Docker Compose for Local Development

**docker-compose.yml** (committed to git):

```yaml
version: "3.8"

services:
  postgres:
    image: postgres:16.1
    environment:
      POSTGRES_DB: ose_dev
      POSTGRES_USER: developer
      POSTGRES_PASSWORD: dev_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7.2.4
    ports:
      - "6379:6379"

  app:
    build:
      context: .
      dockerfile: Dockerfile.be.dev
    volumes:
      - .:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgresql://developer:dev_password@postgres:5432/ose_dev
      REDIS_URL: redis://redis:6379
    depends_on:
      - postgres
      - redis

volumes:
  postgres_data:
```

**Starting local environment**:

```bash
docker-compose up
# All services start with exact same configuration
```

### Development Dockerfile

**Dockerfile.be.dev**:

```dockerfile
# Use specific version
FROM node:24.13.1-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies from lockfile
RUN npm ci

# Copy source code
COPY . .

# Expose port
EXPOSE 3000

# Start development server
CMD ["npm", "run", "dev"]
```

**Why this works**:

- Exact Node.js version (24.13.1)
- npm ci installs from lockfile (deterministic)
- Same environment for all developers
- Works identically on macOS, Linux, Windows

## Documentation

### README Setup Instructions

**Clear, step-by-step setup**:

````markdown
## Environment Setup

### Prerequisites

- [Volta](https://volta.sh/) - JavaScript tool manager (auto-installs Node.js/npm)
- [Docker](https://www.docker.com/) - For local services (PostgreSQL, Redis)
- Git - Version control

### Installation

1. **Install Volta**:

   ```bash
   curl https://get.volta.sh | bash
   ```
````

1. **Clone Repository**:

   ```bash
   git clone https://github.com/wahidyankf/ose-public.git
   cd open-sharia-enterprise
   ```

2. **Install Dependencies**:

   ```bash
   npm ci
   ```

   Volta automatically uses Node.js 24.13.1 and npm 11.10.1 (pinned in package.json).

3. **Configure Environment**:

   ```bash
   cp .env.example .env
   # Edit .env with your values
   ```

4. **Start Services**:

   ```bash
   docker-compose up -d
   ```

5. **Run Development Server**:

   ```bash
   npm run dev
   ```

6. **Verify Setup**:
   - Application: <http://localhost:3000>
   - API health: <http://localhost:3000/health>

### Troubleshooting

**Issue**: "node: command not found"

- **Solution**: Install Volta, then restart terminal

**Issue**: "Cannot connect to database"

- **Solution**: Ensure Docker is running and services started with `docker-compose up`

**Issue**: "Port 3000 already in use"

- **Solution**: Change API_PORT in .env file

````

### Development Workflow Documentation

**Document common tasks**:

```markdown
## Common Development Tasks

### Running Tests

```bash
npm test                    # All tests
npm run test:unit          # Unit tests only
npm run test:integration   # Integration tests only
````

### Database Migrations

```bash
npm run db:migrate         # Run migrations
npm run db:rollback        # Rollback last migration
npm run db:seed            # Seed test data
```

### Code Quality

```bash
npm run lint               # Check code style
npm run format             # Auto-format with Prettier
npm run type-check         # TypeScript type checking
```

````

## Automated Setup Scripts

### setup.sh

**Automate repetitive setup steps**:

```bash
#!/bin/bash
set -e

echo "Setting up Open Sharia Enterprise development environment..."

# Check Volta installed
if ! command -v volta &> /dev/null; then
    echo " Volta not found. Installing..."
    curl https://get.volta.sh | bash
    export VOLTA_HOME="$HOME/.volta"
    export PATH="$VOLTA_HOME/bin:$PATH"
fi

echo " Volta installed"

# Install dependencies
echo " Installing dependencies..."
npm ci

echo " Dependencies installed"

# Setup environment
if [ ! -f .env ]; then
    echo "️  Creating .env file..."
    cp .env.example .env
    echo " .env created (please update with your values)"
else
    echo " .env already exists"
fi

# Start Docker services
echo " Starting Docker services..."
docker-compose up -d

echo " Services started"

# Wait for database
echo " Waiting for database..."
sleep 5

# Run migrations
echo "️  Running database migrations..."
npm run db:migrate

echo " Migrations complete"

echo ""
echo "PASS: Setup complete!"
echo ""
echo "To start development server:"
echo "  npm run dev"
echo ""
echo "Application will be available at:"
echo "  http://localhost:3000"
````

**Usage**:

```bash
./scripts/setup.sh
```

## Testing Reproducibility

### Verification Script

**Verify environment matches expectations**:

```typescript
// scripts/verify-environment.ts
import { execSync } from "child_process";
import { existsSync } from "fs";
import pkg from "../package.json";

function getVersion(command: string): string {
  return execSync(command, { encoding: "utf-8" }).trim();
}

function verify() {
  console.log("Verifying environment...\n");

  // Check Node.js version
  const nodeVersion = getVersion("node --version");
  const expectedNode = `v${pkg.volta.node}`;
  if (nodeVersion === expectedNode) {
    console.log(`PASS: Node.js: ${nodeVersion}`);
  } else {
    console.error(`FAIL: Node.js: Expected ${expectedNode}, got ${nodeVersion}`);
    process.exit(1);
  }

  // Check npm version
  const npmVersion = getVersion("npm --version");
  const expectedNpm = pkg.volta.npm;
  if (npmVersion === expectedNpm) {
    console.log(`PASS: npm: ${npmVersion}`);
  } else {
    console.error(`FAIL: npm: Expected ${expectedNpm}, got ${npmVersion}`);
    process.exit(1);
  }

  // Check lockfile exists
  if (existsSync("package-lock.json")) {
    console.log("PASS: package-lock.json exists");
  } else {
    console.error("FAIL: package-lock.json missing");
    process.exit(1);
  }

  console.log("\nPASS: Environment verification passed!");
}

verify();
```

**Run in CI**:

```yaml
- name: Verify environment
  run: npx ts-node scripts/verify-environment.ts
```

## Monorepo Considerations

### Nx Cache Configuration

**nx.json** (committed to git):

```json
{
  "tasksRunnerOptions": {
    "default": {
      "runner": "nx/tasks-runners/default",
      "options": {
        "cacheableOperations": ["build", "test", "lint"]
      }
    }
  }
}
```

**Why this matters**:

- Nx caching is deterministic (same inputs = cache hit)
- Reproducible builds enable reliable caching
- Cache hits speed up CI/CD

### Workspace Dependencies

**Ensure consistent workspace configuration**:

```json
// tsconfig.base.json
{
  "compilerOptions": {
    "paths": {
      "@open-sharia-enterprise/ts-validation": ["libs/ts-validation/src/index.ts"],
      "@open-sharia-enterprise/ts-auth": ["libs/ts-auth/src/index.ts"]
    }
  }
}
```

**Reproducibility benefit**:

- Path mappings explicit in tsconfig
- All developers resolve imports identically
- TypeScript compilation deterministic

## Troubleshooting

### Common Issues

**"Different behavior locally vs CI"**:

- Check Node.js/npm versions match
- Verify using npm ci (not npm install)
- Check environment variables (.env vs CI secrets)
- Review lockfile is committed and up-to-date

**"Dependencies install differently on different machines"**:

- Ensure package-lock.json committed
- Use npm ci instead of npm install
- Check npm version matches (Volta should handle this)

**"Works on my machine but fails for others"**:

- Document system dependencies (OpenSSL, Python for node-gyp)
- Use Docker to eliminate system dependency variance
- Check for hardcoded paths (use relative paths)
- Review .env.example is up-to-date

## Migration Guide

### Adding Volta to Existing Project

1. **Install Volta** (team members):

   ```bash
   curl https://get.volta.sh | bash
   ```

2. **Pin versions** (project maintainer):

   ```bash
   volta pin node@24.13.1
   volta pin npm@11.10.1
   ```

   This updates package.json with volta field.

3. **Commit changes**:

   ```bash
   git add package.json
   git commit -m "chore: pin Node.js and npm versions with Volta"
   ```

4. **Update documentation** (README.md):
   - Add Volta to prerequisites
   - Update setup instructions
   - Document how Volta auto-manages versions

### Adding Docker to Existing Project

1. **Create docker-compose.yml**:

   ```yaml
   version: "3.8"
   services:
     postgres:
       image: postgres:16.1
       # ... configuration
   ```

2. **Create Dockerfile.be.dev**:

   ```dockerfile
   FROM node:24.13.1-alpine
   # ... configuration
   ```

3. **Update .gitignore**:

   ```
   # Docker volumes
   .docker/
   docker-volumes/
   ```

4. **Document Docker usage**:
   - Add Docker to prerequisites
   - Provide docker-compose up instructions
   - Document how to access services

## Git Identity Guardrail

No AI agent sets or modifies git identity at any scope. This behavioral guardrail replaces the
former `scripts/git-identity-check.sh` pre-commit script, which was removed because it
over-restricted human developers who legitimately maintain per-repository identities via
`includeIf`.

### Forbidden agent actions

All of the following are forbidden for AI agents:

- `git config --local user.name` / `git config --local user.email`
- `git config user.name` / `git config user.email` (bare form writes local scope by default)
- `git config --global user.*` (any identity key at global scope)
- `git config --system user.*` (any identity key at system scope)
- Direct edits to the `.git/config` `[user]` block

### Human rule

Developers set identity in `~/.gitconfig` (global default). For per-repository overrides, use
`includeIf`:

```gitconfig
[includeIf "gitdir:/path/to/repo/"]
  path = ~/.gitconfig-work
```

This keeps repository-specific identity local to the developer's machine without any script
intervention.

### CI exemption

CI service-account identity is configured in workflow YAML (e.g. setting `user.name` to
`github-actions[bot]` before a format-commit-back step). This is not an agent action and is the
one legitimate exemption. It is a CI platform concern, owned by the workflow YAML, not by any AI
agent.

## Related Documentation

- [Reproducibility First](../../principles/software-engineering/reproducibility.md) - WHY reproducibility matters
- [Worktree Toolchain Initialization](./worktree-setup.md) - The `npm run doctor -- --fix` invocation that provisions shared cargo target directories
- [Native-First Toolchain Management](./native-first-toolchain.md) - Architectural decision to use native package managers and `rhino-cli doctor` instead of IaC tools for dev environment setup
- [Code Quality Convention](../quality/code.md) - Automated quality in reproducible environments
- [No Machine-Specific Information in Commits](../quality/no-machine-specific-commits.md) - Preventing machine-specific paths and credentials from entering the repository
- [Trunk Based Development](./trunk-based-development.md) - Reproducible CI/CD for main branch

## References

**Version Management**:

- [Volta](https://volta.sh/) - Hassle-free JavaScript tool manager
- [volta-cli/action](https://github.com/volta-cli/action) - GitHub Action for Volta

**Dependency Management**:

- [npm ci](https://docs.npmjs.com/cli/v10/commands/npm-ci) - Clean install from lockfile
- [package-lock.json](https://docs.npmjs.com/cli/v10/configuring-npm/package-lock-json) - Lockfile format

**Containerization**:

- [Docker](https://www.docker.com/) - Container platform
- [Docker Compose](https://docs.docker.com/compose/) - Multi-container orchestration

**Build Reproducibility**:

- [Nx Caching](https://nx.dev/concepts/how-caching-works) - Deterministic build caching
- [Reproducible Builds](https://reproducible-builds.org/) - Best practices

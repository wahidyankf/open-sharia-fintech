# Common Development Workflow — Development Environment Setup

Before implementing any changes, ensure the development environment is ready. This prevents wasted time on toolchain issues mid-implementation.

## Quick Verification

```bash
# Verify all tools are installed and at correct versions
npm run doctor

# If tools are missing, auto-install them
npm run doctor -- --fix

# Preview what would be installed (dry run)
npm run doctor -- --fix --dry-run

# Check only core tools (git, volta, node, npm, go, docker, jq)
npm run doctor -- --scope minimal
```

## Environment File Management (rhino-cli)

The repository uses `rhino-cli` for environment file management:

```bash
# Initialize .env files from .env.example templates
apps/rhino-cli/scripts/rhino-bin.sh env init

# Backup current .env files
apps/rhino-cli/scripts/rhino-bin.sh env backup

# Restore .env files from backup
apps/rhino-cli/scripts/rhino-bin.sh env restore --force

# Restore including config files (AI tool settings, Docker overrides, etc.)
apps/rhino-cli/scripts/rhino-bin.sh env restore --force --include-config
```

## When to Run Environment Setup

- **Immediately after creating or entering a git worktree** — run BOTH `npm install` AND `npm run doctor -- --fix` in the root repository worktree, in that order. This is a mandatory two-step init; the `postinstall` hook's implicit `doctor || true` does NOT substitute for the explicit `doctor --fix` call. See [Worktree Toolchain Initialization](../../../../repo-governance/development/workflow/worktree-setup.md)
- **Before starting any implementation work** — verify tools and env files are ready
- **After pulling changes** that modify `package.json`, `go.mod`, `.tool-versions`, or other version config
- **After switching between projects** that use different toolchains
- **When any build/test/lint command fails with a "not found" or version error** — run `npm run doctor` first

## Full Setup Guide

For complete step-by-step environment setup (new machine, fresh OS, or broken toolchain), see:
[Development Environment Setup Workflow](../../../../repo-governance/workflows/infra/development-environment-setup.md)

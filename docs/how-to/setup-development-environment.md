---
title: How to Set Up Your Development Environment
description: Install and configure the tools needed to develop and test OSE Public locally
category: how-to
tags:
  - onboarding
  - toolchain
  - setup
  - development
  - docker
  - volta
created: 2026-04-04
---

# How to Set Up Your Development Environment

This guide walks you through installing the tools needed to work on an authorized OSE Public
project locally. After completing it, the repository can verify your toolchain, Git hooks, and the
tests relevant to the project you are changing.

> **Note**: The polyglot demo apps (`a-demo-be-*`, `a-demo-fe-*`) were removed from this repo on
> 2026-04-18. This guide covers only the toolchains this repository actually ships.

## Overview

The monorepo contains projects in TypeScript, Rust, and F#. Each language has its own runtime,
but they all share the same Nx build system and git hooks.

**Two setup paths**:

- **Minimal** — Node.js + Docker + jq. Covers git hooks, TypeScript projects, and
  basic E2E tests.
- **Full** — All tools checked by doctor. Required for working on F# backend apps
  (`organiclever-be`, `ose-be`) and Rust CLI tools.
- **Automated** — Run `npm run doctor -- --fix` to auto-install missing tools. Use
  `npm run doctor -- --fix --dry-run` to preview what would be installed.

## Prerequisites

- **macOS** (primary) or **Linux** (Debian/Ubuntu). Windows is not supported. WSL2 may work, but it
  is not supported or verified by this repository.
- **Admin access** to install system packages.
- **~5 GB disk space** for all runtimes, Docker images, and Playwright browsers.

## Quick Start (Minimal Setup)

If you only work on TypeScript projects, this is all you need:

```bash
# 1. Install Homebrew (macOS — skip if already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Install core tools
brew install jq
# Docker Desktop: download from https://docs.docker.com/desktop/setup/install/mac-install/

# 3. Install Volta (Node.js version manager)
curl https://get.volta.sh | bash
source ~/.zshrc

# 4. Clone and bootstrap
git clone https://github.com/wahidyankf/ose-public.git
cd ose-public
npm install          # Installs deps + git hooks
npx playwright install  # Installs test browsers

# 6. Verify
npm run doctor
```

If doctor shows all green, you are ready. Run
`npm exec nx -- affected -t typecheck,lint,test:quick,test:specs`
to verify the full pre-push pipeline.

## Full Setup

### Step 1: System Package Manager

**macOS**:

```bash
# Install or update Homebrew
brew --version || /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew update
```

**Linux (Debian/Ubuntu)**:

```bash
sudo apt-get update
sudo apt-get install -y build-essential curl git
```

### Step 2: Git and Docker

Git is usually pre-installed on macOS (via Xcode Command Line Tools):

```bash
git --version || xcode-select --install
```

Install Docker Desktop from <https://docs.docker.com/desktop/setup/install/mac-install/>
(macOS) or Docker Engine from <https://docs.docker.com/engine/install/> (Linux).

After installation, verify:

```bash
docker --version
docker compose version
docker info   # Confirms daemon is running
```

Install jq (needed for Claude Code hooks and shell scripts):

```bash
# macOS
brew install jq

# Linux
sudo apt-get install -y jq
```

### Step 3: Node.js via Volta

[Volta](https://volta.sh/) pins Node.js and npm versions per-project. The pinned versions
live in `package.json` under `volta.node` and `volta.npm`.

```bash
curl https://get.volta.sh | bash
source ~/.zshrc   # or source ~/.bashrc
```

After installation, entering the repo directory auto-installs the correct versions:

```bash
cd ose-public
node --version   # Expected: v24.16.0
npm --version    # Expected: 11.11.0
```

If the versions don't match, force install:

```bash
volta install node@24.16.0
volta install npm@11.11.0
```

### Step 4: Rust Toolchain

Required for `rhino-cli`. The toolchain version is pinned via `rust-toolchain.toml` in the project — `rustup` picks it up automatically.

`doctor` additionally checks that every `rust-toolchain.toml` (the workspace root and each
`apps/*`/`libs/*` project) declares the `rustfmt` and `clippy` components. A toolchain pinned
without them installs with rustup's `minimal` profile, and `cargo fmt`/`cargo clippy` then fail
intermittently under it — the failure races with whichever gate happens to run first against that
toolchain. A missing component is reported as a warning, not a blocking failure, matching how
`doctor` reports every other version mismatch.

```bash
# Install rustup (if not present)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install additional cargo tools used by test:quick and deps:audit
cargo install cargo-llvm-cov --locked
cargo install cargo-deny --locked

rustc --version
```

### Step 5: Clone and Bootstrap

```bash
git clone https://github.com/wahidyankf/ose-public.git
cd ose-public
npm install
```

`npm install` does three things:

1. Installs all npm dependencies
2. Runs `npm run doctor` automatically (postinstall script) to verify your toolchain
3. Sets up Husky git hooks (pre-commit, commit-msg, pre-push)

### Step 6: Keep local environment data out of onboarding

Do not restore, copy, or commit a real `.env` file as part of a first checkout. The public
onboarding path does not require private environment values. When an application eventually needs
configuration, read its README and its tracked `.env.example` only; keep real values local and
uncommitted.

### Step 7: Install Playwright Browsers

```bash
npx playwright install
```

This downloads Chromium, Firefox, and WebKit (~500 MB total). Required for all `*-e2e`
projects.

On Linux, also install system dependencies:

```bash
npx playwright install-deps
```

## Verification

### Check all tools

```bash
npm run doctor
```

Expected output: all tools show `ok` status. If any show `missing`, revisit the corresponding
step above.

### Test git hooks

**Pre-commit** (runs on every commit — Prettier, markdownlint, lint-staged):

```bash
# Run the staged-file gate without creating a throwaway commit
apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-commit
```

**Pre-push** (runs affected quality and specification checks):

```bash
# Dry-run: execute the same targets pre-push would
npm exec nx -- affected -t typecheck,lint,test:quick,test:specs
```

This also warms the Nx cache, making subsequent pushes fast.

### Test integration tests

```bash
# Run the OrganicLever backend's integration suite (uses Docker + PostgreSQL)
npm exec nx -- run organiclever-be:test:integration
```

If this passes, Docker and database integration work correctly.

## Troubleshooting

### Doctor reports a tool as "missing"

The doctor command shows exactly which tool is missing, its expected version, and where the
version requirement comes from (e.g., `package.json → volta.node`). Reinstall the tool using
the matching step above.

### Pre-push hook times out

The pre-push hook runs affected quality and specification checks, including `typecheck`, `lint`,
`test:quick`, and `test:specs`. On first run with a cold cache, this can take a while. Warm the
cache first:

```bash
npm exec nx -- affected -t typecheck,lint,test:quick,test:specs
```

Subsequent pushes reuse cached results and complete in seconds.

### Volta not switching Node.js version

Ensure Volta's shims are first in your PATH:

```bash
echo $PATH | tr ':' '\n' | head -5
# ~/.volta/bin should appear before /usr/local/bin
```

If not, add to your shell profile:

```bash
export VOLTA_HOME="$HOME/.volta"
export PATH="$VOLTA_HOME/bin:$PATH"
```

### Docker "permission denied" on Linux

Add your user to the docker group:

```bash
sudo usermod -aG docker $USER
# Log out and back in for changes to take effect
```

### Integration test fails with "port already in use"

Another Docker stack or service is using port 5432. Stop it:

```bash
docker compose -f infra/dev/<other-stack>/docker-compose.yml down
# Or find the process:
lsof -i :5432
```

### Playwright "browser not found"

Re-install browsers:

```bash
npx playwright install
```

On Linux, also run:

```bash
npx playwright install-deps
```

## Version Reference

All version requirements are auto-detected by `npm run doctor` from these config files:

| Tool                 | Version Source                                                                                         |
| -------------------- | ------------------------------------------------------------------------------------------------------ |
| Node.js              | `package.json` → `volta.node`                                                                          |
| npm                  | `package.json` → `volta.npm`                                                                           |
| Rust                 | `apps/rhino-cli/rust-toolchain.toml` → `channel`                                                       |
| Rust lint components | every `rust-toolchain.toml` (root + `apps/*`/`libs/*`) → `components` must include `rustfmt`, `clippy` |
| .NET                 | `repo-config.yml` → `doctor.dotnet-global-json` → `sdk.version` (currently `apps/ose-be/global.json`)  |
| Docker, jq           | Any (no pinned version)                                                                                |

Never hardcode version numbers in scripts — always read from these source-of-truth files.

## Related Documentation

- [Development Environment Setup Workflow](../../repo-governance/workflows/infra/development-environment-setup.md) —
  Granular workflow with phases and success criteria
- [Reproducible Environments](../../repo-governance/development/workflow/reproducible-environments.md) —
  Volta, npm, Docker reproducibility practices
- [Code Quality Convention](../../repo-governance/development/quality/code.md) — Git hooks and
  automated formatting

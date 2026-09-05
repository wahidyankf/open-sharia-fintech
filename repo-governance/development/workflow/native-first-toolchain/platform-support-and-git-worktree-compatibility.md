---
title: "Platform Support and Git Worktree Compatibility"
description: Which platforms doctor --fix supports and how, and why every command already works correctly from a git worktree.
category: explanation
subcategory: development
tags:
  - development
  - toolchain
  - doctor
  - environment
  - architecture-decision
created: 2026-04-04
when_to_use: Use when setting up doctor on Ubuntu/Linux, or when confirming toolchain commands are worktree-safe.
---

# Platform Support and Git Worktree Compatibility

## Platform Support

`doctor --fix` supports both **macOS** and **Ubuntu/Linux**. Platform detection uses `runtime.GOOS`.

Install commands differ per platform:

- **macOS**: Homebrew (`brew install`), Homebrew casks (`brew install --cask`)
- **Ubuntu**: apt (`sudo apt-get install`), curl scripts (Volta, rustup, dotnet-install)
- **Cross-platform**: Volta, rustup, dotnet-install, cargo — same install commands on both platforms

Ubuntu requires system build dependencies before compiling some toolchains:

```bash
sudo apt-get install -y build-essential autoconf curl git \
  libncurses-dev libssl-dev libreadline-dev libsqlite3-dev \
  libbz2-dev libffi-dev zlib1g-dev
```

The `Brewfile` is macOS-only (harmless on Linux — `brew` command not available).

## Git Worktree Compatibility

All commands work correctly from git worktrees. `findGitRoot()` uses `os.Stat` to detect `.git`, which succeeds for both directories (main repo) and files (worktrees). All config file paths are constructed relative to the repo root via `filepath.Join(repoRoot, ...)`, which resolves correctly in both contexts.

This is important because the repository uses git worktrees heavily for AI agent isolation (`.claude/worktrees/`).

Per the [Worktree Toolchain Initialization](../worktree-setup.md) practice,
the transactionally dispatched `npm run doctor -- --fix` is required as the second step of a
mandatory two-step init (after the checksum-pinned HIPPO-guarded `npm install`) whenever a worktree
is created. Doctor's idempotency (documented in the Rationale
section above) makes running it for every new worktree cheap enough to codify as a rule—when the
toolchain is healthy, `doctor --fix` is a no-op pass; when it has drifted, it actively converges.
Mere re-entry does not trigger setup.

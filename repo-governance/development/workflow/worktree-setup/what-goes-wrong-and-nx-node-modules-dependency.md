---
title: "What Goes Wrong Without Both Steps, and Nx's `node_modules` Dependency"
description: The concrete failure modes (build, test, lint, cache, cryptic errors) from skipping the two-step init, and why Nx's caching depends on consistent node_modules state.
category: explanation
subcategory: development
tags:
  - development
  - git
  - worktree
  - npm
  - nx
  - dependencies
  - toolchain
  - doctor
created: 2026-03-28
when_to_use: Use when diagnosing a build, test, lint, or Nx-cache failure that may trace back to a skipped worktree init step.
---

# What Goes Wrong Without Both Steps, and Nx's `node_modules` Dependency

## What Goes Wrong Without Both Steps

Without running both steps after worktree creation or entry, these failures can occur:

- **Build failures**: A dependency that a new worktree's code requires may be absent or at the wrong version, or a native compiler (`rustc`, `dotnet`) may be missing entirely.
- **Test failures**: Test runners (Vitest, Playwright, Cargo, `dotnet test`) may resolve the wrong module versions or fail to launch at all.
- **Lint failures**: Linters may behave differently when versions mismatch, or may not be installed at all for the language a new file uses.
- **Nx cache invalidation**: Nx computes cache keys based on inputs including resolved module versions. A stale `node_modules/` causes cache misses or incorrect cache hits.
- **Cryptic errors**: Dependency and toolchain mismatches often surface as obscure runtime errors rather than clear "missing module" or "missing tool" messages, making them harder to diagnose.

## Nx Workspace Dependency on `node_modules` State

Nx task caching, project graph resolution, and executor plugins all depend on a consistent `node_modules/` state in the workspace root. When `node_modules/` diverges from `package-lock.json`, the entire workspace behaves unpredictably — not just the files that changed.

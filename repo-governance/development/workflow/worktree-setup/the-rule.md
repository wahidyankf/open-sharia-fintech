---
title: "The Rule"
description: The mandatory two-step npm install / doctor --fix sequence, run order, the --fix flag, and the shared cargo target-directory symlink it provisions.
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
when_to_use: Use as the exact commands to run, in order, right after creating or entering a worktree.
---

# The Rule

**After every `git worktree add`, `EnterWorktree` invocation, or any other entry into a worktree session (human or agent), run BOTH of the following in the root repository worktree, in order:**

```bash
# Run these in the ROOT repository worktree path, not the new worktree.
cd /path/to/root/open-sharia-enterprise

# Step 1: Node/Nx workspace dependencies (node_modules/)
npm install

# Step 2: Toolchain convergence (Rust, .NET/F#, TypeScript/Node — all managed by rhino-cli)
npm run doctor -- --fix
```

The root worktree is the primary checkout of the repository — the directory that contains the canonical `node_modules/` used by Nx across all worktrees. Replace `/path/to/root/open-sharia-enterprise` with the actual absolute path to the root checkout on the current machine.

**Order matters.** Run `npm install` first, because `rhino-cli doctor` itself is a Rust binary built and invoked through the Node tooling; the doctor script may need a freshly synchronized `node_modules/` to run correctly. Run `npm run doctor -- --fix` second to actively converge the native toolchain.

**Use `--fix`, not plain `doctor`.** Plain `npm run doctor` only detects drift and requires a second human action. `npm run doctor -- --fix` actively converges to the declared toolchain state in a single step. If a human wants a preview of what would change first, use `npm run doctor -- --fix --dry-run`.

## Shared Cargo Target Directories (Local-Dev Only)

`npm run doctor -- --fix` also creates per-crate `target/` symlinks pointing into a shared cargo build-artifact cache, so multiple worktrees of the same repo reuse build artifacts instead of recompiling the same crates independently. This step is **local-dev only** — it is a no-op under CI. See [Reproducible Environments §Shared Cargo Target Directories](../reproducible-environments/shared-cargo-target-directories.md#shared-cargo-target-directories) for the full mechanism, including the cache root, the `OSE_CARGO_TARGET_CACHE` override, and the worktree-aware `doctor --prune-cargo-cache` garbage collector.

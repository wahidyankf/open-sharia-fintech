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

**After every `rtk git worktree add`, `EnterWorktree` invocation, or other worktree entry, run BOTH
commands from the root directory of that new or active worktree, in order:**

```bash
# Set the active worktree root as the command workdir.

# Step 1: Node/Nx workspace dependencies (node_modules/)
rtk npm install

# Step 2: Toolchain convergence (Rust, .NET/F#, TypeScript/Node — all managed by rhino-cli)
rtk npm run doctor -- --fix
```

Each worktree needs its own ignored `node_modules/`. Running `rtk npm install` there also runs the
repository's `prepare` script, which activates Husky's tracked hooks for Git operations from that
worktree. A successful install in the primary checkout does not initialize a new worktree.

**Order matters.** Run `rtk npm install` first, because `rhino-cli doctor` itself is a Rust binary built and invoked through the Node tooling; the doctor script may need a freshly synchronized `node_modules/` to run correctly. Run `rtk npm run doctor -- --fix` second to actively converge the native toolchain.

**Use `--fix`, not plain `doctor`.** Plain `rtk npm run doctor` only detects drift and requires a second human action. `rtk npm run doctor -- --fix` actively converges to the declared toolchain state in a single step. For a preview, use `rtk npm run doctor -- --fix --dry-run`.

## Shared Cargo Target Directories (Local-Dev Only)

`rtk npm run doctor -- --fix` also creates per-crate `target/` symlinks pointing into a shared cargo build-artifact cache, so multiple worktrees of the same repo reuse build artifacts instead of recompiling the same crates independently. This step is **local-dev only** — it is a no-op under CI. See [Reproducible Environments §Shared Cargo Target Directories](../reproducible-environments/shared-cargo-target-directories.md#shared-cargo-target-directories) for the full mechanism, including the cache root, the `OSE_CARGO_TARGET_CACHE` override, and the worktree-aware `doctor --prune-cargo-cache` garbage collector.

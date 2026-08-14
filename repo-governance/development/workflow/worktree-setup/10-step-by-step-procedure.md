---
title: "Step-by-Step Procedure"
description: The five numbered steps from creating a worktree through confirming both init commands completed.
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
when_to_use: Use as a walkthrough when creating a worktree and running its toolchain init for the first time.
---

# Step-by-Step Procedure

1. Create or enter the worktree using your preferred method:

   ```bash
   git worktree add worktrees/my-feature-branch my-feature-branch
   ```

   This repo overrides the upstream coding-agent default worktree path — worktrees land at repo-root `worktrees/<name>/`, not under the platform binding directory. See [worktree-path.md](../../../conventions/structure/worktree-path.md) for the convention and the `WorktreeCreate` hook that enforces it.

2. Identify the root repository worktree path. This is the directory containing the canonical checkout — typically the parent of `worktrees/`.

3. Run `npm install` in the root worktree:

   ```bash
   cd /path/to/root/open-sharia-enterprise
   npm install
   ```

4. Run `npm run doctor -- --fix` in the root worktree:

   ```bash
   npm run doctor -- --fix
   ```

   This command is idempotent — when the toolchain is already healthy it is a no-op pass; when drifted it actively converges. To preview changes without applying them, use `npm run doctor -- --fix --dry-run`.

5. Confirm both steps completed without errors before running any Nx commands in the new worktree.

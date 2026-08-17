---
title: "Independent Drift Layers and the `postinstall` Hook"
description: The two independent kinds of toolchain drift a worktree session can hit, and why the postinstall hook's error-swallowing means only the explicit doctor --fix call forces convergence.
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
when_to_use: Use when explaining why both npm install and npm run doctor -- --fix are independently required, not either alone.
---

# Independent Drift Layers and the `postinstall` Hook

## Two Independent Layers of Drift

A new or newly-entered worktree session can hit two independent kinds of toolchain drift, and a single command does not cover both:

1. **Node/Nx dependency drift** — handled by `npm install`. `node_modules/` is not tracked by git, so it is not automatically synchronized between worktrees.
2. **Polyglot native toolchain drift** — handled by `npm run doctor -- --fix`. The monorepo spans native toolchains beyond Node — Rust, .NET/F#, and the shell/Terraform/container linters (see [Native-First Toolchain Management](../native-first-toolchain.md)); a session needs any of them to be correct the moment the pre-push hook (`apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-push`) fans out its affected-projects gates, including `nx affected -t test:quick`.

Skipping either step leaves the other layer vulnerable. Doing only `npm install` handles `node_modules/` but leaves native toolchain drift undetected; doing only `npm run doctor -- --fix` converges the native toolchain but can leave the Nx workspace operating against a stale `node_modules/`.

## The `postinstall` Hook Silently Tolerates Drift

`package.json` defines a `postinstall` hook that runs `npm run doctor || true`. The `|| true` is deliberate — it prevents `npm install` from failing when the polyglot toolchain is drifted, which is the right default for `npm install` to remain usable as a dependency-sync command. But the consequence is that **`npm install` can complete "successfully" while the polyglot toolchain is actually broken**. A human developer or AI agent then tries to run a Rust, .NET, or TypeScript task in the new worktree and hits cryptic errors that aren't traceable to a missing or drifted toolchain.

The explicit `npm run doctor -- --fix` call is the only mechanism that forces active convergence at the moment the worktree session begins.

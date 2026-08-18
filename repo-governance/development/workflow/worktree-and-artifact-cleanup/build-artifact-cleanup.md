---
title: "Build-Artifact Cleanup"
description: Scope and exclusions for purging build output produced inside a plan's own worktrees.
category: explanation
subcategory: development
tags:
  - git
  - workflow
  - worktree
  - cleanup
  - parallelism
created: 2026-07-20
when_to_use: Use when deciding what build output to purge, and what to leave alone, during plan-end cleanup.
---

# Build-Artifact Cleanup

Purge only the build output produced **inside this plan's own worktrees** — `target/`, `dist/`,
`.next/`, and build caches — after verifying non-use.

Explicitly **skip** the shared cargo `target/` and every other shared cache, and run **no** `git gc`
or `git prune` on the object store. If build output is already gone when this gate runs, that is the
ambient sweeper, not a missed step — record it as swept and move on rather than rebuilding output
solely to delete it. History maintenance is a serialization point on a shared machine
and stays out of the cleanup gate entirely.

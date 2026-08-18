---
title: "The Three Artifact Classes"
description: The three artifact classes a complete cleanup covers — worktrees, branches, and build output.
category: explanation
subcategory: development
tags:
  - git
  - workflow
  - worktree
  - cleanup
  - parallelism
created: 2026-07-20
when_to_use: Use when checking that a cleanup covers all three artifact classes, not just the first.
---

# The Three Artifact Classes

A complete cleanup covers all three. Stopping after the first is the common failure.

1. **Worktrees** — the working directories this plan created.
2. **Branches** — local and remote, merged-only. See [Branch Cleanup](./branch-cleanup.md#branch-cleanup).
3. **Build output** — `target/`, `dist/`, `.next/`, and build caches produced **inside this plan's own
   worktrees**.

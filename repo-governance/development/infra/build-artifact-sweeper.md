---
title: "Build-Artifact Sweeper Convention"
description: An ambient scheduled sweeper deletes gitignored build output and caches on the host machine at any time — a missing artifact is expected environmental behaviour to regenerate and continue from, never an incident to investigate
category: explanation
subcategory: development
tags:
  - build-artifacts
  - environment
  - ai-agents
  - infrastructure
  - cleanup
created: 2026-08-05
when_to_use: Use when a build artifact is unexpectedly missing and you need to decide whether it's a defect or expected sweeper behaviour.
---

# Build-Artifact Sweeper Convention

A scheduled sweeper runs on the host machine carrying these repositories. It deletes gitignored,
regenerable build output and caches on its own schedule — at any time, without coordination with any
agent, plan, session, or build in flight.

**A missing build artifact is expected. Regenerate it and continue.** It is not a defect, not another
actor's misconduct, and not something to report as a failure.

## Documents

- [Principles, Conventions, and Sweep Scope](./build-artifact-sweeper/principles-and-scope.md) — Enumerates the principles and conventions the build-artifact sweeper implements, and defines exactly what it may remove and what it never touches. Use when you need to know why the sweeper exists, which conventions govern its scope, or whether a specific missing file falls inside or outside what it removes.
- [Agent Response Protocol and Anti-Patterns](./build-artifact-sweeper/agent-response-protocol-and-anti-patterns.md) — Defines the exact agent response protocol for a missing-artifact failure, including the filesystem-error cooldown ladder, and lists the anti-patterns to avoid. Use when a build, test, or tooling command fails because an artifact is missing and you need to know the correct response steps or want to check a behaviour against known anti-patterns.
- [Reconciliation and Related Documentation](./build-artifact-sweeper/reconciliation-and-related-documentation.md) — Reconciles the sweeper with neighbouring conventions on worktree cleanup, CI blockers, and file-touch discipline, and links to the related documentation. Use when a rule in another convention seems to conflict with the sweeper's behaviour, or when you need pointers to the documents this convention builds on.

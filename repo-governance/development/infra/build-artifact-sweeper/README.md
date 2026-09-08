---
description: "An ambient scheduled sweeper deletes gitignored build output and caches on the host machine at any time — a missing artifact is expected environmental behaviour to regenerate and continue from, never an incident to investigate"
when_to_use: "Read this index to find the right Build-Artifact Sweeper Convention child document."
---

# Build-Artifact Sweeper Convention

- [Principles, Conventions, and Sweep Scope](./principles-and-scope.md) — Enumerates the principles and conventions the build-artifact sweeper implements, and defines exactly what it may remove and what it never touches Use when you need to know why the sweeper exists, which conventions govern its scope, or whether a specific missing file falls inside or outside what it removes.
- [Agent Response Protocol and Anti-Patterns](./agent-response-protocol-and-anti-patterns.md) — Defines the exact agent response protocol for a missing-artifact failure, including the filesystem-error cooldown ladder, and lists the anti-patterns to avoid Use when a build, test, or tooling command fails because an artifact is missing and you need to know the correct response steps or want to check a behaviour against known anti-patterns.
- [Reconciliation and Related Documentation](./reconciliation-and-related-documentation.md) — Reconciles the sweeper with neighbouring conventions on worktree cleanup, CI blockers, and file-touch discipline, and links to the related documentation Use when a rule in another convention seems to conflict with the sweeper's behaviour, or when you need pointers to the documents this convention builds on.

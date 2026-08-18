---
title: "Anti-Patterns in Workflow Development"
description: "Common workflow anti-patterns and their corrected pattern."
when_to_use: "Read this index to find the right Anti-Patterns in Workflow Development child document."
---

# Anti-Patterns in Workflow Development

- [Overview and Purpose](./overview-and-purpose.md) — Why understanding workflow anti-patterns matters and what this document covers. Use when orienting to why the anti-patterns document exists and what it covers before reading individual entries.
- [Anti-Pattern: Long-Lived Feature Branches](./long-lived-feature-branches.md) — Feature branches lasting weeks cause merge conflicts and integration delays, and the fix that avoids them. Use when tempted to keep a feature branch open for more than a day or two instead of shipping in small integrated phases.
- [Anti-Pattern: Large, Infrequent Commits](./large-infrequent-commits.md) — Committing large batches of changes infrequently makes review and revert difficult. Use when about to commit a week's worth of changes in a single large commit instead of small incremental ones.
- [Anti-Pattern: Vague Commit Messages](./vague-commit-messages.md) — Commit messages that don't explain changes undermine searchable history and changelog automation. Use when writing a commit message that doesn't clearly state what changed and why.
- [Anti-Pattern: Skipping Feature Flags for Incomplete Work](./skipping-feature-flags-for-incomplete-work.md) — Hiding incomplete features in long-lived branches instead of using feature flags. Use when incomplete work would otherwise be held back in a branch instead of merged behind a flag.
- [Anti-Pattern: Premature Optimization](./premature-optimization.md) — Optimizing before the implementation works wastes effort and skips the make-it-work step. Use when planning to design caching or micro-optimizations before a basic working implementation exists.
- [Anti-Pattern: Unpinned Dependencies](./unpinned-dependencies.md) — Not locking dependency versions or committing the lockfile causes inconsistent builds. Use when adding a dependency or configuring version pinning and lockfile commits.
- [Anti-Pattern: Ignoring Broken CI](./ignoring-broken-ci.md) — Pushing code that breaks CI and deferring the fix blocks the whole team. Use when CI fails after a push and there's a temptation to defer the fix.
- [Anti-Pattern: Mixed Concerns in Single Commit](./mixed-concerns-in-single-commit.md) — Combining unrelated changes in one commit produces confusing, hard-to-revert history. Use when a single commit would otherwise bundle unrelated changes across different domains.
- [Anti-Pattern: Hardcoded Environment Configuration](./hardcoded-environment-configuration.md) — Hardcoding production values in code creates security issues and breaks local development. Use when about to hardcode a database URL, API key, or other environment-specific value in source code.
- [Anti-Pattern: Skipping Local Testing](./skipping-local-testing.md) — Relying on CI alone to discover test failures wastes time that local testing would have saved. Use when about to push changes without first running tests and lint locally.
- [Anti-Pattern: Pushing Without Pulling Latest Main](./pushing-without-pulling-latest-main.md) — Pushing without first pulling and rebasing on the latest main causes push rejections and messy merge commits. Use when about to push to main without first pulling with rebase, or when configuring the team's pull strategy.
- [Conclusion and Principles](./conclusion-and-principles.md) — Closing summary of anti-pattern outcomes and the principles/conventions this document implements. Use when checking which principles and conventions the anti-patterns document traces back to.

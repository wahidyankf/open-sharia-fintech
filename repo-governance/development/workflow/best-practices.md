---
title: "Best Practices for Workflow Development"
description: Twelve recommended workflow patterns covering branching, commits, feature flags, staged implementation, dependencies, CI, config, and push discipline.
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: Use when looking for the recommended pattern for a workflow decision — branching, commits, CI, config, or push strategy.
---

# Best Practices for Workflow Development

> **Companion Document**: For common mistakes to avoid, see [Anti-Patterns](../workflow/anti-patterns.md)

## Contents

- [Overview and Purpose](./best-practices/01-overview-and-purpose.md) — Why this document exists.
- [Practice 1: Integrate Continuously via Short-Lived Branches](./best-practices/02-practice-1-integrate-continuously-via-short-lived-branches.md) — Merge to main at least daily.
- [Practice 2: Make Small, Frequent Commits](./best-practices/03-practice-2-make-small-frequent-commits.md) — Atomic commits, multiple times per day.
- [Practice 3: Use Conventional Commits](./best-practices/04-practice-3-use-conventional-commits.md) — type(scope): description format.
- [Practice 4: Use Feature Flags Instead of Long-Lived Branches](./best-practices/05-practice-4-use-feature-flags-instead-of-long-lived-branches.md) — Merge behind a flag, toggle later.
- [Practice 5: Implement in Three Stages](./best-practices/06-practice-5-implement-in-three-stages.md) — Work, then right, then fast.
- [Practice 6: Pin Dependencies for Reproducibility](./best-practices/07-practice-6-pin-dependencies-for-reproducibility.md) — Exact versions, lockfiles committed.
- [Practice 7: Keep CI Green at All Times](./best-practices/08-practice-7-keep-ci-green-at-all-times.md) — Fix or revert immediately on red.
- [Practice 8: Use Environment-Specific Configuration](./best-practices/09-practice-8-use-environment-specific-configuration.md) — No hardcoded environment values.
- [Practice 9: Split Commits by Domain](./best-practices/10-practice-9-split-commits-by-domain.md) — One concern per commit.
- [Practice 10: Test Before Committing](./best-practices/11-practice-10-test-before-committing.md) — Run the suite locally first.
- [Practice 11: Pull with Rebase Before Pushing](./best-practices/12-practice-11-pull-with-rebase-before-pushing.md) — Keep history linear.
- [When to Use Merge vs Rebase](./best-practices/13-when-to-use-merge-vs-rebase.md) — Default rebase, and five conditions for merge instead.
- [Git Configuration for Rebase](./best-practices/14-git-configuration-for-rebase.md) — Branch-specific, global, or explicit-flag config.
- [Conflict Resolution Workflows](./best-practices/15-conflict-resolution-workflows.md) — Resolving conflicts under rebase vs merge.
- [Safety Considerations](./best-practices/16-safety-considerations.md) — Never rebase pushed commits; abort paths.
- [Best Practice in Daily Workflow](./best-practices/17-best-practice-in-daily-workflow.md) — A worked start-of-day-to-push walkthrough.
- [Practice 12: Default to worktree-to-pr; Select a Direct-Push Mode Deliberately](./best-practices/18-practice-12-default-to-worktree-to-pr.md) — Deliberate opt-in for direct-push modes.
- [Summary and Principles/Conventions Implemented](./best-practices/19-summary-and-principles-conventions-implemented.md) — Recap of all twelve practices.

## Related Documentation

- [Trunk Based Development Convention](../workflow/trunk-based-development.md) - Complete TBD workflow
- [Commit Message Convention](../workflow/commit-messages.md) - Conventional Commits guide
- [Implementation Workflow Convention](../workflow/implementation.md) - Three-stage methodology
- [Reproducible Environments Convention](../workflow/reproducible-environments.md) - Environment practices
- [Anti-Patterns](../workflow/anti-patterns.md) - Common mistakes to avoid
- [Git Push Default Convention](../workflow/git-push-default.md) - The PR-branch-as-default push target, and the direct-push modes as explicit selections

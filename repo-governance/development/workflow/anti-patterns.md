---
title: "Anti-Patterns in Workflow Development"
description: Common workflow anti-patterns and their corrected pattern.
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: Use when reviewing a workflow decision for a known anti-pattern.
---

# Anti-Patterns in Workflow Development

> **Companion Document**: For positive guidance on what to do, see [Best Practices](../workflow/best-practices.md)

Understanding common mistakes in development workflows helps teams build more efficient, collaborative, and predictable systems. These anti-patterns cause merge conflicts, integration delays, and development friction. Each entry below covers the problem, a bad example, the fix, and the rationale; see the last entry for the summary table, conclusion, and traced principles.

## Anti-Patterns

- [Overview and Purpose](./anti-patterns/overview-and-purpose.md) — Why this document exists and what it covers.
- [Anti-Pattern: Long-Lived Feature Branches](./anti-patterns/long-lived-feature-branches.md) — Long branches cause conflicts and delays. Use when tempted to keep a branch open more than a day or two.
- [Anti-Pattern: Large, Infrequent Commits](./anti-patterns/large-infrequent-commits.md) — Large batched commits are hard to review. Use when about to commit a week's changes as one lump.
- [Anti-Pattern: Vague Commit Messages](./anti-patterns/vague-commit-messages.md) — Vague messages undermine history and changelogs. Use when a commit message doesn't state what changed and why.
- [Anti-Pattern: Skipping Feature Flags for Incomplete Work](./anti-patterns/skipping-feature-flags-for-incomplete-work.md) — Keeping work on a long-lived branch instead of integrating an internally complete-and-inert increment behind a temporary production-disabled flag. Use when incomplete behaviour would otherwise sit unmerged.
- [Anti-Pattern: Premature Optimization](./anti-patterns/premature-optimization.md) — Optimizing before it works wastes effort. Use when planning optimization before a working implementation exists.
- [Anti-Pattern: Unpinned Dependencies](./anti-patterns/unpinned-dependencies.md) — Unlocked versions cause inconsistent builds. Use when adding a dependency or configuring pinning.
- [Anti-Pattern: Ignoring Broken CI](./anti-patterns/ignoring-broken-ci.md) — Deferring a CI fix blocks the team. Use when CI fails and there's a temptation to defer the fix.
- [Anti-Pattern: Mixed Concerns in Single Commit](./anti-patterns/mixed-concerns-in-single-commit.md) — Independent purposes bundled together or completion artifacts split apart. Use after authorization when applying the thematic boundary test.
- [Anti-Pattern: Hardcoded Environment Configuration](./anti-patterns/hardcoded-environment-configuration.md) — Hardcoded prod values create security and portability issues. Use when about to hardcode a URL, key, or env value.
- [Anti-Pattern: Skipping Local Testing](./anti-patterns/skipping-local-testing.md) — Relying on CI alone wastes time. Use when about to push without running tests and lint locally.
- [Anti-Pattern: Pushing Without Pulling Latest Main](./anti-patterns/pushing-without-pulling-latest-main.md) — Pushing without pulling first causes rejections and messy merges. Use when about to push without pulling with rebase first.
- [Conclusion and Principles](./anti-patterns/conclusion-and-principles.md) — Summary table, closing takeaways, and the principles/conventions this document implements.

## Related Documentation

- [Trunk Based Development Convention](../workflow/trunk-based-development.md) - Complete TBD workflow
- [Commit Message Convention](../workflow/commit-messages.md) - Conventional Commits guide
- [Implementation Workflow Convention](../workflow/implementation.md) - Three-stage methodology
- [Reproducible Environments Convention](../workflow/reproducible-environments.md) - Environment practices
- [Best Practices](../workflow/best-practices.md) - Recommended patterns
- [No Secrets in Git Convention](../../conventions/security/no-secrets-in-committed-files.md) - Hard iron rule
  governing Anti-Pattern 9 and all committed files: no system secret may ever enter git history

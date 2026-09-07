---
description: "A deferred merge-queue integration idea."
when_to_use: "Use when scoping a future merge-queue integration."
---

# Deferred Merge Queue (D7/D10)

A merge queue was researched during this convention's own drafting — GitHub-native versus
Graphite/Aviator — as a way to close a gap in
[PR Merge Protocol](../../workflow/pr-merge-protocol.md) precondition (c): a static, per-PR
branch-up-to-date check cannot guarantee the branch stays non-destructively current when two PRs
merge at overlapping times. **That adoption was researched but NOT delivered.** The repo's branch
settings expose no merge-queue toggle to enable, because GitHub merge queue requires organization
ownership and the repos in scope are personal-account-owned. Precondition (c) therefore remains the
manual branch-up-to-date check, unchanged. The deferred investigation, availability matrix, and
adoption path are tracked separately as future work, not by this convention.

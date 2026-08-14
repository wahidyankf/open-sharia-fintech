---
name: docs-managing-file-operations
description: Complete methodology for safely renaming, moving, and deleting files/directories in docs/ — file naming review, the four-phase systematic process, deletion safety, link updates, git operations, index updates, validation checklists, safety guidelines, edge cases, and integration with other agents. Backs the docs-file-manager agent.
---

# Documentation: Managing File Operations

Methodology for safely managing files and directories in `docs/` while maintaining kebab-case
conventions, fixing links, preserving git history, and avoiding orphaned references.

## Reference Modules

1. [When to Use and Naming Convention](reference/01-when-to-use-and-naming.md) — when to use this
   agent, what it's not for, and the file naming convention review.
2. [Systematic Process](reference/02-systematic-process.md) — the four-phase process: Discovery &
   Analysis, Planning, Execution, Validation.
3. [Deletion Operations](reference/03-deletion-operations.md) — safe deletion, deleting directories,
   the deletion safety checklist.
4. [Link Updates and Git Operations](reference/04-link-updates-and-git-ops.md) — calculating relative
   paths, removing links to deleted files, git best practices, batch ordering.
5. [Index Updates and Validation](reference/05-index-updates-and-validation.md) — when/how to update
   README.md indices, the full validation checklist.
6. [Safety Guidelines and Edge Cases](reference/06-safety-and-edge-cases.md) — read-before-edit,
   confirmation gates, README.md special-casing, circular updates, uncommitted files.
7. [Integration and Communication](reference/07-integration-communication-antipatterns.md) —
   coordinating with `docs-link-checker`/`repo-rules-checker`/`docs-maker`, summary format, and the
   anti-patterns table.

## Core Principles

- **`git mv`/`git rm` always, never `mv`/`rm`** — history preservation is non-negotiable.
- **Find every reference before deleting** — an unlinked file is an orphan; a deleted file with
  surviving links is a 404.
- **Plan, confirm, then execute** — large reorganizations get a presented plan and explicit user
  confirmation before Phase 3 touches anything.

## Related Skills

- `docs-validating-links`, `docs-applying-content-quality`, `docs-applying-diataxis-framework`,
  `repo-practicing-trunk-based-development`.

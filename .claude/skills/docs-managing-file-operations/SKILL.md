---
name: docs-managing-file-operations
description: Complete methodology for safely renaming, moving, and deleting files/directories in docs/ — file naming review, the four-phase systematic process, deletion safety, link updates, git operations, index updates, validation checklists, safety guidelines, edge cases, and integration with other agents. Backs the docs-file-manager agent.
---

# Documentation: Managing File Operations

Methodology for safely managing files and directories in `docs/` while maintaining kebab-case
conventions, fixing links, preserving git history, and avoiding orphaned references.

## Reference Modules

1. [When to Use and Naming Convention](reference/when-to-use-and-naming.md) — when to use this
   agent, what it's not for, and the file naming convention review.
2. [Discovery and Planning](reference/discovery-and-planning.md) — Phase 1-2 of the four-phase
   process: Discovery & Analysis, then Planning.
3. [Execution and Validation](reference/execution-and-validation.md) — Phase 3-4 of the
   four-phase process: Execution, then Validation.
4. [Deletion Operations](reference/deletion-operations.md) — safe deletion, deleting directories,
   the deletion safety checklist.
5. [Link Updates and Git Operations](reference/link-updates-and-git-ops.md) — calculating relative
   paths, removing links to deleted files, git best practices, batch ordering.
6. [Index Updates and Validation](reference/index-updates-and-validation.md) — when/how to update
   README.md indices, the full validation checklist.
7. [Safety Guidelines and Edge Cases](reference/safety-and-edge-cases.md) — read-before-edit,
   confirmation gates, README.md special-casing, circular updates, uncommitted files.
8. [Integration and Communication](reference/integration-communication-antipatterns.md) —
   coordinating with `docs-link-checker`/`rules-checker`/`docs-maker`, summary format, and the
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

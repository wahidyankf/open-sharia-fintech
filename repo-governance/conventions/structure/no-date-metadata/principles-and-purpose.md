---
title: "No Manual Date Metadata: Principles and Purpose"
description: The core principles this convention implements, and why manual updated fields, Last Updated footers, and inline date annotations were removed in favor of git history.
when_to_use: Read this to understand why the repository bans manual date metadata before you go looking for where to record a file's last-changed date.
category: explanation
subcategory: conventions
tags:
  - conventions
  - frontmatter
  - maintenance
  - git
created: 2026-04-25
---

# No Manual Date Metadata: Principles and Purpose

Why this convention exists. Part of the
[No Manual Date Metadata Convention](../no-date-metadata.md).

## Principles Implemented/Respected

This convention implements the following core principles:

- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: Removing manual date tracking eliminates a maintenance burden that grows with every file edit. Fewer fields to maintain means less surface area for drift and audit noise.

- **[Automation Over Manual](../../../principles/software-engineering/automation-over-manual.md)**: Git provides automatic, authoritative, tamper-evident change tracking. Manual date fields duplicate this information poorly — git does it better without any human effort.

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: By explicitly banning all forms of manual date metadata from non-website files, this convention makes the rule unambiguous. No exceptions to remember, no judgment calls about whether to update the date, no false signals to readers.

## Purpose

Manual `updated:` fields, `**Last Updated**` footers, and inline body annotations like `- **Created**: 2025-12-01` were intended to signal content age. In practice they:

- **Drift immediately**: Any edit to a file should update the date, but this is easy to forget and impossible to enforce automatically
- **Create audit noise**: Governance quality gate runs flag date mismatches and stale annotations as real findings, requiring multiple fix iterations that add no value
- **Duplicate git**: `git log --follow -- <file>` gives the same information with full commit message context and author attribution
- **Mislead readers**: A stale date signals "this content is old" when the file may simply not have needed updates
- **Pollute document bodies**: Inline `- **Created**: 2025-12-01` annotations in agent or convention files are visible to every reader but answer no question that git does not already answer

The `created:` frontmatter field is unaffected by this convention. It is set once at file creation, never updated, and does not drift.

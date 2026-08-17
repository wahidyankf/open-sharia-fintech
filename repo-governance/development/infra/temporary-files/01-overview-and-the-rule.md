---
title: "Overview and the Rule"
description: Why the convention exists and the mandatory directory rule itself.
category: explanation
subcategory: development
tags: [temporary-files, ai-agents, file-organization, best-practices]
created: 2025-12-01
when_to_use: Use before creating any temporary file, to confirm the mandatory directory rule.
---

# Overview and the Rule

## Principles Implemented/Respected

This practice respects the following core principles:

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: Designated directories (`generated-reports/`, `local-tmp/`) with explicit purposes. Report naming pattern clearly encodes agent family, timestamp, and type. No hidden temporary files scattered throughout the repository.

- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: Two directories for all temporary files - one for reports, one for scratch work. Simple, flat structure with clear naming conventions. No complex hierarchies or categorization schemes.

## Conventions Implemented/Respected

**REQUIRED SECTION**: All development practice documents MUST include this section to ensure traceability from practices to documentation standards.

This practice implements/respects the following conventions:

- **[AI Agents Convention](../../agents/ai-agents.md)**: All checker agents MUST have Write and Bash tools for report generation. Report-generating agents follow mandatory progressive writing requirement to survive context compaction.

- **[Timestamp Format Convention](../../../conventions/formatting/timestamp.md)**: Report filenames use UTC+7 timestamps in format YYYY-MM-DD--HH-MM (hyphen-separated for filesystem compatibility).

- **[File Naming Convention](../../../conventions/structure/file-naming.md)**: Report files follow 4-part pattern {agent-family}**{uuid-chain}**{timestamp}\_\_{type}.md with double-underscore separators. UUID chain enables parallel execution without file collisions.

## Overview

This convention establishes designated directories for temporary files created by AI agents during validation, auditing, checking, and other automated tasks. It prevents repository clutter and provides clear organization for ephemeral outputs.

## The Rule

**AI agents creating temporary uncommitted file(s) or folder(s) MUST use one of these directories:**

- `generated-reports/` - For validation, audit, and check reports
- `local-tmp/` - For miscellaneous temporary files and scratch work

**Exception**: Unless specified otherwise by other existing repo-governance/conventions in the repository.

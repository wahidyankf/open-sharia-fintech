---
title: "Report File Naming Standard — Repository Audit and Link Validation Reports"
description: Filename pattern and retention for rules-checker and docs-link-checker reports.
category: explanation
subcategory: development
tags: [temporary-files, ai-agents, file-organization, best-practices]
created: 2025-12-01
when_to_use: Use when naming a rules-checker or docs-link-checker report.
---

# Report File Naming Standard — Repository Audit and Link Validation Reports

Continues [Report File Naming Standard](./report-file-naming-standard.md).

## Repository Audit Reports

**Agent**: rules-checker
**Pattern**: `repo-rules__{uuid-chain}__{YYYY-MM-DD--HH-MM}__audit.md`
**Example**: `repo-rules__a1b2c3__2025-12-14--20-45__audit.md`

**Content**: Comprehensive consistency audit covering:

- AGENTS.md vs convention documents
- Agent definitions vs conventions
- Cross-references and links
- Duplication and contradictions
- Frontmatter consistency
- File naming compliance

**Timestamp**: Audit start time in UTC+7 (YYYY-MM-DD--HH-MM format)

**Retention**: Keep for historical tracking and comparison. Review/archive older reports periodically.

## Link Validation Reports

**Agent**: docs-link-checker
**Pattern**: `docs-link__{uuid-chain}__{YYYY-MM-DD--HH-MM}__audit.md`
**Example**: `docs-link__a1b2c3__2025-12-14--20-45__audit.md`

**Content**: External and internal link validation results, broken links, redirect chains, cache maintenance summary (pruned links, usedIn updates)

**Timestamp**: Audit start time in UTC+7 (YYYY-MM-DD--HH-MM format)

**Retention**: Keep for historical tracking and comparison. Review/archive older reports periodically.

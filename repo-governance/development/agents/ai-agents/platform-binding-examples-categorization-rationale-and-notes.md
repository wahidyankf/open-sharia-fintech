---
title: "Platform Binding Examples — Categorization Rationale and Link Checker Note"
description: "Explains why the color categorization system exists and gives a special note for link-checker agents."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - standards
created: 2025-11-23
when_to_use: Use when justifying a color choice or handling a link-checker agent's color assignment.
---

# Platform Binding Examples — Categorization Rationale and Link Checker Note

## Why This Categorization System

This role-based categorization was chosen because it:

1. **Aligns with naming conventions** - Role suffixes (-maker, -checker, -fixer, -dev, -deployer, -manager, -tester, -researcher) directly map to colors
2. **Maps to tool permissions** - Clear security boundaries between read-only, edit-only, write-capable, and full-access agents
3. **Provides clear user guidance** - Users can quickly identify which category of agent they need
4. **Extensible** - New agents naturally fit into one of the four role categories
5. **Semantic consistency** - Colored square emojis (🟦🟩🟨🟪) have no pre-existing meaning in Unicode, allowing flexible assignment

## Link Checker Agents Note

**NOTE**: Link checker agents are checker agents (`color: green`) that also manage persistent cache files. This is documented here to clarify their tool permissions.

**Link Checker Agents:**

- **docs-link-checker** - Validates documentation links + manages external-links-status.yaml cache
- **apps-ayokoding-www-link-checker** - Validates ayokoding-www content links + manages ayokoding-links-status.yaml cache

**Why green (not purple)?**

1. **Primary role**: Link validation (checker behaviour) with audit report generation
2. **Color follows primary role**: The `-checker` suffix and validation-first behaviour make green the correct color
3. **State management is secondary**: Cache file management supports the validation role, not the reverse
4. **Consistency**: Agent `Role` declarations and naming suffix both say "Checker (green)"

**Why they have Write + Edit tools (beyond standard green pattern):**

- Cache files (`external-links-status.yaml`, `ayokoding-links-status.yaml`) are operational metadata, NOT temporary reports
- Cache management is essential functionality, NOT general file writing capability
- Write tool is scoped specifically to designated cache file paths (explicit over implicit)
- This exception respects the Explicit Over Implicit principle by documenting the extended tool access

**Cache files are NOT temporary:**

- Location: `docs/metadata/` (docs-link-checker) and `apps/ayokoding-www/` (apps-ayokoding-www-link-checker)
- Purpose: Long-term link status tracking (6-month expiry), shared across team
- Committed to git: Yes (operational metadata)
- Updated every run: Yes (including lastFullScan timestamp)

This is intentionally documented here to maintain transparency and prevent confusion about tool permission patterns.

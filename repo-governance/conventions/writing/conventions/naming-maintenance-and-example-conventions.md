---
title: "Convention Writing Convention — Naming, Maintenance, and Example Conventions"
description: The file/title naming pattern for convention documents, the review and deprecation process, and a curated list of exemplary conventions to model.
when_to_use: Use when naming a new convention file, reviewing an existing one for staleness, or looking for a structural example to imitate.
category: explanation
subcategory: conventions
tags:
  - meta
  - conventions
  - standards
  - documentation
created: 2025-12-07
---

# Naming, Maintenance, and Example Conventions

## Naming Convention

Convention files follow the [File Naming Convention](../../structure/file-naming.md):

**Pattern:** Lowercase kebab-case basename under the appropriate `repo-governance/conventions/` subdirectory. The directory hierarchy encodes the category — no filename prefix is needed. A convention document is not a step, so it never carries a leading `NN-` ordinal; see [Ordinal Filename Prefixes](../../structure/ordinal-filename-prefixes.md).

**Examples:**

- `repo-governance/conventions/structure/file-naming.md`
- `repo-governance/conventions/formatting/diagrams.md`
- `repo-governance/conventions/writing/quality.md`
- `repo-governance/conventions/writing/conventions.md` (the parent document for this convention)

**Title vs Filename:**

- Filename: `conventions.md` (plain kebab-case)
- Frontmatter title: `"Convention Writing Convention"` (Title Case + "Convention")
- H1 heading: `# Convention Writing Convention` (matches title)

## Maintenance and Updates

### Regular Review

- Review conventions annually or when underlying tools/practices change
- Update examples if they become outdated
- Add new sections for emerging patterns

### Version Control

- Git history is the authoritative record of changes (no `updated:` field needed)
- Significant changes should update AGENTS.md if they affect agent behaviour
- Use `rules-maker` to propagate changes across related files

### Deprecation

If a convention becomes obsolete:

1. Add deprecation notice at top of document
2. Provide migration path to replacement convention
3. Keep file for 6 months before considering deletion
4. Update all references in other docs and AGENTS.md

## Example Conventions

Looking for inspiration? These conventions exemplify different structural approaches:

- **[Color Accessibility Convention](../../formatting/color-accessibility.md)** - Comprehensive reference convention with detailed palette specifications, contrast ratios, and tool-specific guidance
- **[Tutorial Naming Convention](../../tutorials/naming.md)** - Decision-tree convention with structured types, coverage percentages, and clear selection criteria
- **[Indentation Convention](../../formatting/indentation.md)** - Simple, focused convention addressing a single technical standard with clear examples

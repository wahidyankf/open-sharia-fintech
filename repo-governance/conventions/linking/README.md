---
description: Rules for durable, repository-internal Markdown links
when_to_use: Use when one repository document needs to link to another and you want the link to keep working in a fresh checkout, not just on a published site.
---

# Linking Conventions

Use these conventions when one repository document points to another. They keep links useful in a fresh checkout, not just on a published site.

## Purpose

Linking conventions ensure consistent, maintainable internal references across the repository. These standards govern how markdown files reference other files, ensuring links remain functional and follow repository conventions.

## Conventions

- [Internal AyoKoding Reference Links Convention](./internal-ayokoding-references.md) — Standards for linking from docs/ to apps/ayokoding-www/ content using relative paths instead of public web URLs. Use when linking from docs/ to educational content in apps/ayokoding-www/ and unsure whether to use a relative path or a public URL.

## Principles Implemented/Respected

- **[Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md)**: Direct markdown links, no complex indirection
- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**: Links are explicit paths, not computed references
- **[Documentation First](../../principles/content/documentation-first.md)**: Clear linking standards prevent broken references

## Related Conventions

- [File Naming Convention](../structure/file-naming.md) — Correct file names enable accurate linking
- [Diátaxis Framework](../structure/diataxis-framework.md) — Documentation organization affects link paths

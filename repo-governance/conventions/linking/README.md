---
title: "Linking Conventions"
description: Rules for durable, repository-internal Markdown links
category: explanation
subcategory: conventions
tags: []
created: 2026-05-12
---

# Linking Conventions

Use these conventions when one repository document points to another. They keep links useful in a fresh checkout, not just on a published site.

## Purpose

Linking conventions ensure consistent, maintainable internal references across the repository. These standards govern how markdown files reference other files, ensuring links remain functional and follow repository conventions.

## Conventions

### [Internal AyoKoding References](./internal-ayokoding-references.md)

Standards for linking between AyoKoding educational content and OSE Platform documentation, including language prefix requirements, absolute path conventions, and cross-repository reference patterns.

## Principles Implemented/Respected

- **[Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md)**: Direct markdown links, no complex indirection
- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**: Links are explicit paths, not computed references
- **[Documentation First](../../principles/content/documentation-first.md)**: Clear linking standards prevent broken references

## Related Conventions

- [File Naming Convention](../structure/file-naming.md) - Correct file names enable accurate linking
- [Diátaxis Framework](../structure/diataxis-framework.md) - Documentation organization affects link paths

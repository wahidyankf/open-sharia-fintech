---
title: "Purpose, Scope, and Why GitHub-Compatible Links"
description: Defines what the Linking Convention covers, the principles it implements, and why the repository standardizes on GitHub-compatible relative markdown links.
when_to_use: Use when you need to understand why this repository avoids wiki-style links or what the linking convention covers.
category: explanation
subcategory: conventions
tags:
  - linking
  - markdown
  - conventions
  - github-compatibility
created: 2025-11-22
---

# Purpose, Scope, and Why GitHub-Compatible Links

## Principles Implemented/Respected

This convention implements the following core principles:

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: Uses explicit relative paths (`./path/to/file.md`) instead of implicit wiki-style links (`[[filename]]`). File extensions are always included, making it clear what type of file is being referenced. No magic linking behavior - every path is stated clearly.

- **[Accessibility First](../../../principles/content/accessibility-first.md)**: Descriptive link text (not filenames) improves screen reader experience. Users hear meaningful context like "File Naming Convention" instead of cryptic identifiers like "ex-co\_\_file-naming-convention".

## Purpose

This convention establishes the standard linking format for all markdown files in the repository. It ensures links are GitHub-compatible, use relative paths with `.md` extensions, and follow consistent patterns across all documentation. This prevents broken links and maintains portability.

## Scope

### What This Convention Covers

- **Markdown link syntax** - `Display Text` format
- **Relative vs. absolute paths** - When to use each
- **Extension requirements** - `.md` extension for all markdown files
- **Cross-directory linking** - How to link between different documentation areas
- **External link formatting** - How to format links to external resources

### What This Convention Does NOT Cover

- **Link validation** - Covered by docs-link-checker and apps-ayokoding-www-link-checker agents
- **Link text quality** - Descriptive link text is covered in [Content Quality Principles](../../writing/quality.md)
- **Anchor links** - Deep linking to specific sections (implementation detail)

## Why GitHub-Compatible Links?

We use standard markdown link syntax with explicit relative paths to ensure:

1. **GitHub Rendering** - GitHub does not render wiki-style `[[...]]` links; standard markdown links render correctly on GitHub web and anywhere else
2. **Universal Compatibility** - Links work in any standard markdown viewer, VS Code, and CI link checkers
3. **Explicit Paths** - Relative paths make it clear where files are located
4. **Version Control** - Easier to track changes and validate links in CI/CD
5. **No Ambiguity** - Full paths prevent confusion when files have similar names

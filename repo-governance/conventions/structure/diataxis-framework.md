---
title: "Diátaxis Framework"
description: Understanding the Diátaxis documentation framework used in open-sharia-enterprise
when_to_use: Use when deciding where new documentation belongs or organizing content by Diátaxis category.
category: explanation
subcategory: conventions
tags:
  - diataxis
  - documentation-framework
  - organization
  - conventions
created: 2025-11-22
---

# Diátaxis Framework

The open-sharia-enterprise project uses the [Diátaxis framework](https://diataxis.fr/) to organize all documentation. This document explains what Diátaxis is, why we use it, and how it's implemented in our project.

## Principles Implemented/Respected

This convention implements the following core principles:

- **[Progressive Disclosure](../../principles/content/progressive-disclosure.md)**: Diátaxis separates learning-oriented content (tutorials) from problem-solving (how-to) and reference material. Beginners start with tutorials, experienced users jump to how-to guides or reference. Complexity is layered, not overwhelming.

- **[Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md)**: Four clear categories (Tutorials, How-To, Reference, Explanation) instead of complex, nested documentation hierarchies. Each category serves a single, well-defined purpose.

## Children

- [What is Diátaxis, and Why We Use It](./diataxis-framework/what-is-diataxis-and-why-we-use-it.md) — the 2x2 model and the concrete benefits for writers, users, and the project.
- [The Four Categories](./diataxis-framework/the-four-categories.md) — purpose, characteristics, and in-project location for Tutorials, How-To, Reference, and Explanation.
- [How Diátaxis is Implemented](./diataxis-framework/how-diataxis-is-implemented.md) — the docs/ directory structure, naming rationale, and required frontmatter.
- [Choosing the Right Category, and Common Mistakes to Avoid](./diataxis-framework/choosing-the-right-category-and-common-mistakes.md) — a decision tree plus category-mixing and miscategorization examples.
- [Examples from Our Project, Related Documentation, and External Resources](./diataxis-framework/examples-related-and-external-resources.md) — worked before/after examples and further reading.

## Purpose and Scope

### Purpose

This convention establishes the Diátaxis framework as the organizational structure for all documentation in the repository. It provides a systematic approach to categorizing content into four distinct types (Tutorials, How-To, Reference, Explanation), ensuring documentation serves different user needs effectively. This framework guides where new content belongs and maintains clear boundaries between documentation types.

### Scope

#### What This Convention Covers

- **Documentation categorization** - The four Diátaxis categories (Tutorials, How-To, Reference, Explanation)
- **Category characteristics** - Purpose, audience, and appropriate content for each category
- **Category boundaries** - What belongs in each category vs. what doesn't
- **Navigation and discovery** - How categories help users find information
- **Content creation guidance** - When to create content in each category

#### What This Convention Does NOT Cover

- **How to write content within categories** - Covered in category-specific conventions (e.g., [Tutorial Naming Convention](../tutorials/naming.md), [README Quality Convention](../writing/readme-quality.md))
- **File naming within categories** - Covered in [File Naming Convention](./file-naming.md)
- **App-specific content structure** - Covered in [Programming Language Content Standard](../tutorials/programming-language-content.md)
- **Content quality standards** - Covered in [Content Quality Principles](../writing/quality.md)

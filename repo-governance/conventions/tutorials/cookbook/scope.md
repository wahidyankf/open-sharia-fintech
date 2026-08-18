---
title: "Scope"
description: "Defines what the Cookbook convention covers and explicitly does not cover, and where it applies across the repository."
when_to_use: "Read when determining whether a question about Cookbook tutorials is answered by this convention or a different one."
category: explanation
subcategory: conventions
tags:
  - convention
  - tutorial
  - cookbook
  - education
  - problem-solving
  - recipes
created: 2026-01-30
---

# Scope

**Universal Application**: This convention applies to **all cookbook tutorial content** across the repository:

- **apps/ayokoding-www/content/** - Canonical location for programming language cookbooks (Java, Golang, Python, etc.)
- **apps/ose-www/content/** - Platform cookbooks using recipe approach
- **Any other location** - Cookbook tutorials regardless of directory

**Implementation Notes**: While these standards apply universally, platform-specific details (frontmatter, weights, navigation) are covered in site-specific skills.

## What This Convention Covers

- **Cookbook tutorial structure** - Problem-focused recipes organized by category
- **Target audience** - Developers at any level seeking practical solutions
- **Recipe format** - Problem → Solution → Explanation → Pitfalls → Related
- **Recipe organization** - By problem type (not difficulty level)
- **Recipe count** - 30+ recipes across problem domains
- **Code quality** - Copy-paste ready, annotated at 0.5-1.5 density
- **Independence** - Each recipe self-contained and usable in any order

## What This Convention Does NOT Cover

- **General tutorial standards** - Covered in [Tutorials Convention](../general.md)
- **Tutorial naming** - Covered in [Tutorial Naming Convention](../naming.md)
- **How-to guides** - Goal-oriented guides in how-to/ directory (different from cookbook)
- **By-example tutorials** - Sequential learning examples (different structure)
- **By-concept tutorials** - Comprehensive concept coverage (different organization)

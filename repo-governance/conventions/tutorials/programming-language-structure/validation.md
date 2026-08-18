---
title: "Validation"
description: Automated checker coverage and the manual pre-publish verification checklist for tutorial structure.
when_to_use: Use when running or interpreting automated tutorial-structure checks, or before publishing new language tutorials.
category: explanation
subcategory: conventions
tags:
  - programming-languages
  - tutorials
  - ayokoding-www
  - education
  - structure
created: 2025-12-27
---

# Validation

## Automated Validation

**apps-ayokoding-www-general-checker** validates:

- PASS: By-concept directory structure exists
- PASS: All mandatory files present (\_index.md, overview.md, beginner/intermediate/advanced.md)
- PASS: Weight values follow level-based system
- PASS: Internal links use absolute paths
- PASS: Frontmatter completeness
- PASS: No H1 headings in content

**apps-ayokoding-www-by-example-checker** validates:

- PASS: By-example directory structure (when exists)
- PASS: 75-90 examples across three files
- PASS: Five-part example structure
- PASS: Self-containment rules
- PASS: Educational comment standards
- PASS: Coverage progression

## Manual Verification Checklist

Before publishing new language tutorials:

- [ ] By-concept directory with all required files
- [ ] Overview files explain learning approach
- [ ] Beginner/intermediate/advanced tutorials exist
- [ ] Initial Setup and Quick Start at root level
- [ ] Navigation lists paths in correct order (by-concept/by-example first)
- [ ] Weight values follow level-based system
- [ ] All links use absolute paths with language prefix
- [ ] Frontmatter complete and correct
- [ ] No categories field in frontmatter
- [ ] Tags use JSON array format
- [ ] If by-example exists: 75-90 examples across three files
- [ ] If by-example exists: Five-part structure per example
- [ ] Cross-references to Programming Language Content Standard

---
title: "Disabled Rules"
description: "The markdownlint rules intentionally disabled, and why each is off."
category: explanation
subcategory: development
tags:
  - markdown
  - linting
  - formatting
  - prettier
  - markdownlint
  - quality
created: 2026-01-17
when_to_use: "Use when confirming whether a markdownlint rule was deliberately disabled."
---

# Disabled Rules

These rules are intentionally disabled to align with repository conventions:

- **MD001**: Heading increment (false positives with code blocks)
- **MD003**: Heading style (allow mixed atx/atx_closed)
- **MD013**: Line length (allow long links)
- **MD024**: Duplicate headings (common in long docs)
- **MD025**: Multiple H1s (some files intentionally have multiple)
- **MD033**: Inline HTML (allowed for frontmatter)
- **MD036**: Emphasis as heading (intentional styling pattern)
- **MD040**: Code language (many code blocks are plain text)
- **MD041**: First line H1 (conflicts with frontmatter)
- **MD051**: Link fragments (false positives with auto-generated anchors)
- **MD056**: Table column count (intentional table formatting)
- **MD059**: Descriptive link text (contextually clear links)
- **MD060**: Table column style (intentional styling)

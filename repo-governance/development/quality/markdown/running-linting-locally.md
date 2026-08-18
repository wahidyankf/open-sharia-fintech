---
title: "Running Linting Locally"
description: "npm commands to check and auto-fix markdown lint/format violations locally."
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
when_to_use: "Use when you need to check or fix markdown violations before committing."
---

# Running Linting Locally

## Check markdown files

```bash
# Lint all markdown files
npm run lint:md

# Auto-fix violations
npm run lint:md:fix
```

## Format markdown files

```bash
# Format all markdown files
npm run format:md

# Check if files need formatting (no changes)
npm run format:md:check
```

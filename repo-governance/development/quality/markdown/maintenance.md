---
title: "Maintenance"
description: "How to update markdownlint rules and the Prettier/markdownlint-cli2 dependencies."
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
when_to_use: "Use when changing a rule or bumping a markdown-tooling dependency."
---

# Maintenance

## Updating Rules

To modify linting rules:

1. Edit `.markdownlint-cli2.jsonc`
2. Test changes: `npm run lint:md`
3. Verify zero violations: `npm run lint:md:fix && npm run lint:md`
4. Commit configuration changes

## Updating Dependencies

```bash
# Update markdownlint-cli2
npm update markdownlint-cli2

# Update Prettier
npm update prettier
```

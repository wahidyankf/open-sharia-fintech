---
title: "Prettier - Code Formatting"
description: "How Prettier formats code in this repository."
category: explanation
subcategory: development
tags:
  - development
  - code-quality
  - prettier
  - husky
  - lint-staged
  - git-hooks
  - automation
created: 2026-05-12
when_to_use: "Use when configuring or debugging Prettier formatting."
---

# Prettier - Code Formatting

**Purpose**: Automatically format code to maintain consistent style across the codebase.

**Supported File Types**:

- JavaScript/TypeScript: `*.{js,jsx,ts,tsx,mjs,cjs}`
- JSON: `*.json`
- Markdown: `*.md`
- YAML: `*.{yml,yaml}`
- CSS/SCSS: `*.{css,scss}`

**When It Runs**: Automatically on staged files before each commit via the pre-commit hook.

**Configuration**: Prettier uses default settings (no custom configuration file). This ensures maximum compatibility and reduces configuration overhead.

**Manual Formatting**: You can manually format files with:

```bash
npx prettier --write [file-path]
```

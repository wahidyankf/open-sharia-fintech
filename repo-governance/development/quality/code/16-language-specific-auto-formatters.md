---
title: "Language-Specific Auto-Formatters"
description: "Auto-formatters used per language across the repository."
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
when_to_use: "Use when checking which formatter applies to a given language."
---

# Language-Specific Auto-Formatters

The following language-specific formatters run automatically as part of the pre-commit hook or CI pipeline:

| Language  | Tool            | Trigger                  |
| --------- | --------------- | ------------------------ |
| Rust      | `rustfmt`       | Pre-commit (lint-staged) |
| F\# / C\# | `dotnet format` | Pre-commit hook step     |

Each formatter uses its language's standard style conventions. No custom configuration is applied
unless a project-specific config file exists (e.g., `rustfmt.toml`, `.editorconfig`).

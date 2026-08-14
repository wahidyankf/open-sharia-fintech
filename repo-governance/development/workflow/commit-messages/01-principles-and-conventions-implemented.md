---
title: "Principles and Conventions Implemented"
description: The principles and companion conventions the commit message format respects.
category: explanation
subcategory: development
tags:
  - conventional-commits
  - git
  - development
  - code-quality
created: 2025-11-24
when_to_use: Use when tracing why the commit message convention exists back to the principles and conventions it respects.
---

# Principles and Conventions Implemented

## Principles Implemented/Respected

This practice respects the following core principles:

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: Commit format (`type(scope): description`) explicitly states the nature of change. No guessing from cryptic messages like "fix stuff" or "updates". Commit type, scope, and description are all explicit.

- **[Automation Over Manual](../../../principles/software-engineering/automation-over-manual.md)**: Commitlint automatically validates message format via git hooks. Commits rejected if format is invalid. No manual review of commit messages needed - automation enforces the standard.

## Conventions Implemented/Respected

**REQUIRED SECTION**: All development practice documents MUST include this section to ensure traceability from practices to documentation standards.

This practice implements/respects the following conventions:

- **[Code Quality Convention](../../quality/code.md)**: Commit message validation is enforced through git hooks (Husky + Commitlint) as part of the automated code quality workflow.

- **[Content Quality Principles](../../../conventions/writing/quality.md)**: Commit messages use active voice (imperative mood) and clear, concise descriptions - aligning with content quality standards for communication.

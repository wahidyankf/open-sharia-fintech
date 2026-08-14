---
title: "Overview"
description: "Overview of the automated code-quality tooling."
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
when_to_use: "Use when orienting to the code-quality toolchain."
---

# Overview

This project enforces code quality through automated tools that run during the development workflow:

- **Prettier** - Automatic code formatting
- **Husky** - Git hooks management
- **Lint-staged** - Run tools on staged files only
- **Commitlint** - Commit message validation (see [Commit Message Convention](../../workflow/commit-messages.md))

These tools work together to ensure code consistency and quality without manual intervention.

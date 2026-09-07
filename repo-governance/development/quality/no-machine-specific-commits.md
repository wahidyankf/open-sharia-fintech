---
title: "No Machine-Specific Information in Commits"
description: Practice prohibiting absolute local paths, usernames, IP addresses, and environment-specific configuration from committed code
category: explanation
subcategory: development
tags:
  - git
  - commits
  - security
  - portability
  - environment
  - quality
created: 2026-03-24
when_to_use: "Use when writing, reviewing, or fixing a commit that might contain a machine-specific path, username, IP, or config value."
---

# No Machine-Specific Information in Commits

**Purpose**: Prevent committed code from containing information specific to one developer's machine, ensuring the repository remains portable, reproducible, and free of accidental credential exposure.

## Documents

- [Principles and Conventions Implemented/Respected](./no-machine-specific-commits/principles-and-conventions-implemented-respected.md) — The reproducibility, explicit-config, and root-cause principles, and the file-naming and no-secrets conventions this practice implements. Use when tracing this practice to the principles/conventions it implements.
- [Overview](./no-machine-specific-commits/overview.md) — The two classes of harm from machine-specific values entering git history: portability failures and information disclosure. Use when orienting to why machine-specific commits are prohibited.
- [What Counts as Machine-Specific Information](./no-machine-specific-commits/what-counts-as-machine-specific-information.md) — The prohibited categories: absolute local paths, embedded usernames, local IPs/hostnames, and environment-specific literals. Use when deciding whether a specific value is machine-specific and must not be committed.
- [Acceptable Test Data](./no-machine-specific-commits/acceptable-test-data.md) — The distinction between realistic test data that verifies parsing logic and actual machine identity. Use when a test fixture resembles machine-specific data and you need to confirm it is acceptable.
- [What Belongs in Source Files vs. Environment Configuration](./no-machine-specific-commits/what-belongs-in-source-files-vs-environment-configuration.md) — A table mapping information types to their correct location, plus the .env.example template pattern. Use when deciding whether a value belongs in source code or in .env configuration.
- [Verifying a Commit Before Pushing](./no-machine-specific-commits/verifying-a-commit-before-pushing.md) — The grep command to scan staged changes for common machine-specific patterns before committing. Use before pushing a commit that adds test fixtures, configuration, or script output containing paths.
- [Examples](./no-machine-specific-commits/examples.md) — Worked prohibited-vs-correct examples for hardcoded paths, test fixtures, and committed credentials. Use when you need a concrete before/after example of fixing a machine-specific value.
- [Scope](./no-machine-specific-commits/scope.md) — What file types this rule applies to, and the two exclusions (.env files and .gitignore entries). Use when checking whether this rule applies to a specific file type.
- [Remediation](./no-machine-specific-commits/remediation.md) — The steps to fix an already-committed machine-specific value, including credential rotation for sensitive leaks. Use when machine-specific information has already been committed and needs remediation.

## Related Documentation

- [Code Quality Convention](./code.md) - Git hooks and pre-commit automation that help catch violations before they reach the remote
- [Reproducible Environments](../workflow/reproducible-environments.md) - Volta pinning, package-lock.json, and `.env.example` templates for consistent developer environments
- [Commit Message Convention](../workflow/commit-messages.md) - Conventional Commits format for the corrective commit

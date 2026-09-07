---
title: "No Machine-Specific Information in Commits"
description: "Practice prohibiting absolute local paths, usernames, IP addresses, and environment-specific configuration from committed code"
when_to_use: "Read this index to find the right No Machine-Specific Information in Commits child document."
---

# No Machine-Specific Information in Commits

- [Principles and Conventions Implemented/Respected](./principles-and-conventions-implemented-respected.md) — The reproducibility, explicit-config, and root-cause principles, and the file-naming and no-secrets conventions this practice implements. Use when tracing this practice to the principles/conventions it implements.
- [Overview](./overview.md) — The two classes of harm from machine-specific values entering git history: portability failures and information disclosure. Use when orienting to why machine-specific commits are prohibited.
- [What Counts as Machine-Specific Information](./what-counts-as-machine-specific-information.md) — The prohibited categories: absolute local paths, embedded usernames, local IPs/hostnames, and environment-specific literals. Use when deciding whether a specific value is machine-specific and must not be committed.
- [Acceptable Test Data](./acceptable-test-data.md) — The distinction between realistic test data that verifies parsing logic and actual machine identity. Use when a test fixture resembles machine-specific data and you need to confirm it is acceptable.
- [What Belongs in Source Files vs. Environment Configuration](./what-belongs-in-source-files-vs-environment-configuration.md) — A table mapping information types to their correct location, plus the .env.example template pattern. Use when deciding whether a value belongs in source code or in .env configuration.
- [Verifying a Commit Before Pushing](./verifying-a-commit-before-pushing.md) — The grep command to scan staged changes for common machine-specific patterns before committing. Use before pushing a commit that adds test fixtures, configuration, or script output containing paths.
- [Examples](./examples.md) — Worked prohibited-vs-correct examples for hardcoded paths, test fixtures, and committed credentials. Use when you need a concrete before/after example of fixing a machine-specific value.
- [Scope](./scope.md) — What file types this rule applies to, and the two exclusions (.env files and .gitignore entries). Use when checking whether this rule applies to a specific file type.
- [Remediation](./remediation.md) — The steps to fix an already-committed machine-specific value, including credential rotation for sensitive leaks. Use when machine-specific information has already been committed and needs remediation.

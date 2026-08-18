---
title: "Timestamp Format Convention"
description: Standard timestamp format using UTC+7 (Indonesian WIB Time)
when_to_use: Use when writing, generating, or validating any timestamp in this repository.
category: explanation
subcategory: conventions
tags:
  - conventions
  - timestamps
  - timezone
  - formatting
created: 2025-11-30
---

# Timestamp Format Convention

This convention establishes UTC+7 timezone with ISO 8601 format as the standard for all timestamps in the repository, ensuring consistent time representation across cache files, metadata, logs, and frontmatter.

## In This Convention

- [Purpose, Scope, and Standard Format](./timestamp/purpose-scope-and-standard-format.md) — Principles, scope, overview, the baseline format, and why UTC+7
- [Applicability, Format Specification, and Validation](./timestamp/applicability-format-specification-and-validation.md) — Where to use and not use UTC+7, implementation examples, format components, UTC conversion, and valid/invalid examples
- [Generating Current Timestamps](./timestamp/generating-current-timestamps.md) — Bash commands for AI agents and scripts to generate real timestamps, and anti-patterns to avoid

## Related Conventions

- [File Naming Convention](../structure/file-naming.md) — Date format in filenames

## See Also

- **ISO 8601**: International standard for date and time representation
- **RFC 3339**: Internet timestamp format specification
- **WIB**: Western Indonesian Time (Waktu Indonesia Barat)

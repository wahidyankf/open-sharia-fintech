---
title: "Best Practices for Infrastructure Development"
description: Index of best practices for managing development infrastructure — temporary files, report generation, execution tracking, acceptance criteria, and audit trails — split across focused child documents.
category: explanation
subcategory: development
tags: [infrastructure, best-practices]
created: 2026-05-12
when_to_use: Use when looking for best-practice guidance on temporary file handling, report naming/generation, execution tracking, Gherkin acceptance criteria, or audit-trail hygiene in development infrastructure, and need to find the right child document.
---

# Best Practices for Infrastructure Development

> **Companion Document**: For common mistakes to avoid, see [Anti-Patterns](../infra/anti-patterns.md)

This document indexes best practices for managing development infrastructure, including temporary files, report generation, execution tracking, Gherkin acceptance criteria, and audit trails. Each linked document below covers a focused group of practices with concrete good/bad examples and rationale.

## Best Practices Documents

- [Overview and Purpose](./best-practices/overview-and-purpose.md) — Explains what infrastructure development best practices this document covers and why they matter for organized, traceable, testable development processes. Use when orienting to what this best-practices document covers before diving into the individual practices.
- [Best Practices: File Organization and Progressive Reporting](./best-practices/file-organization-and-progressive-reporting.md) — Covers best practices for organizing temporary files, naming reports consistently, writing reports progressively during execution, and generating real UUIDs and timestamps instead of placeholders. Use when setting up temporary file locations, naming a new report file, deciding when to write report content, or generating UUIDs/timestamps for a report.
- [Best Practices: Execution Tracking, Acceptance Criteria, and Tooling](./best-practices/execution-tracking-acceptance-criteria-and-tooling.md) — Covers best practices for scope-based execution tracking in concurrent workflows, writing Gherkin acceptance criteria, and required tools for report-generating checker agents. Use when tracking concurrent workflow executions, writing Given-When-Then acceptance criteria, or configuring tools for a checker agent that generates reports.
- [Best Practices: Audit Trails and Temporary File Hygiene](./best-practices/audit-trails-and-temporary-file-hygiene.md) — Covers best practices for pairing audit and fix reports with matching identifiers, periodically cleaning up temporary files, and documenting the purpose of long-lived temporary files. Use when generating a fix report that follows an audit, scheduling cleanup of temporary files, or documenting why a temporary file or directory exists.
- [Related Documentation, Summary, and Principles](./best-practices/related-documentation-summary-and-principles.md) — Lists related documentation, summarizes the ten infrastructure best practices, and states the principles and conventions this guidance implements. Use when looking for related documentation links, a quick recap of all ten best practices, or the principles/conventions this document implements.

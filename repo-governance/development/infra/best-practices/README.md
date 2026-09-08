---
description: "Index of best practices for managing development infrastructure — temporary files, report generation, execution tracking, acceptance criteria, and audit trails — split across focused child documents."
when_to_use: "Read this index to find the right Best Practices for Infrastructure Development child document."
---

# Best Practices for Infrastructure Development

- [Best Practices: File Organization and Progressive Reporting](./file-organization-and-progressive-reporting.md) — Covers best practices for organizing temporary files, naming reports consistently, writing reports progressively during execution, and generating real UUIDs and timestamps instead of placeholders. Use when setting up temporary file locations, naming a new report file, deciding when to write report content, or generating UUIDs/timestamps for a report.
- [Best Practices: Execution Tracking, Acceptance Criteria, and Tooling](./execution-tracking-acceptance-criteria-and-tooling.md) — Covers best practices for scope-based execution tracking in concurrent workflows, writing Gherkin acceptance criteria, and required tools for report-generating checker agents. Use when tracking concurrent workflow executions, writing Given-When-Then acceptance criteria, or configuring tools for a checker agent that generates reports.
- [Best Practices: Audit Trails and Temporary File Hygiene](./audit-trails-and-temporary-file-hygiene.md) — Covers best practices for pairing audit and fix reports with matching identifiers, periodically cleaning up temporary files, and documenting the purpose of long-lived temporary files. Use when generating a fix report that follows an audit, scheduling cleanup of temporary files, or documenting why a temporary file or directory exists.
- [Related Documentation, Summary, and Principles](./related-documentation-summary-and-principles.md) — Lists related documentation, summarizes the ten infrastructure best practices, and states the principles and conventions this guidance implements. Use when looking for related documentation links, a quick recap of all ten best practices, or the principles/conventions this document implements.

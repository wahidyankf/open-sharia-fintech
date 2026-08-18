---
title: "Anti-Patterns in Infrastructure Development"
description: "Common anti-patterns in infrastructure development — scattered files, placeholder values, missing tools, vague criteria — with problems, examples, and solutions for each."
when_to_use: "Read this index to find the right Anti-Patterns in Infrastructure Development child document."
---

# Anti-Patterns in Infrastructure Development

- [Anti-Patterns in Temporary Files, Placeholder Values, and Buffered Reports](./scattered-files-placeholders-and-buffered-reports.md) — Covers the scattered-temp-files, placeholder-UUID, and in-memory-report-buffering anti-patterns, with bad/good examples for each. Use when a script is about to write a temporary file, generate a UUID/timestamp, or buffer audit findings before writing a report.
- [Anti-Patterns in Checker Tooling, Execution Tracking, and Report Pairing](./missing-tools-global-tracking-and-mismatched-reports.md) — Covers the missing-tools, global-execution-tracking, and mismatched-audit/fix-report anti-patterns for checker and fixer agents. Use when defining a checker agent's tool list, an execution-tracking file, or pairing a fixer report with its source audit.
- [Anti-Patterns in Gherkin Keyword Cardinality and Acceptance Criteria](./keyword-cardinality-and-vague-acceptance-criteria.md) — Covers the Gherkin multiple-primary-keyword and vague-acceptance-criteria anti-patterns, with the cardinality rule and testable-criteria examples. Use when writing or reviewing a Gherkin Scenario block or drafting acceptance criteria for a plan or spec.
- [Anti-Patterns in Temp File Cleanup, Checker Output, and Documentation](./cleanup-conversation-output-and-undocumented-files.md) — Covers the never-cleaning-temp-files, conversation-only-output, and undocumented-long-lived-temp-file anti-patterns. Use when a checker agent is about to report findings only in conversation, or when temporary files are piling up without cleanup or documentation.
- [Anti-Patterns Summary, Related Documentation, and Conclusion](./summary-related-docs-and-conclusion.md) — Summary table of all anti-patterns, related documentation links, the closing anti-pattern checklist, and the principles/conventions this document implements. Use for a quick-reference table of every anti-pattern and solution, or to find related conventions and principles documents.

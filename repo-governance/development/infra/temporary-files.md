---
title: "Temporary Files Convention"
description: Guidelines for AI agents creating temporary uncommitted files and folders
category: explanation
subcategory: development
tags:
  - temporary-files
  - ai-agents
  - file-organization
  - best-practices
created: 2025-12-01
when_to_use: Use when an AI agent needs to create a temporary uncommitted file or folder — a report, a scratch file, or anything not meant for git.
---

# Temporary Files Convention

The rule is simple — `generated-reports/` for reports, `local-tmp/` for everything else — with the details linked below.

## Rules and Report Generation

- [Overview and the Rule](./temporary-files/overview-and-the-rule.md) — Why the convention exists and the mandatory directory rule itself. Use before creating any temporary file, to confirm the mandatory directory rule.
- [Mandatory Report Generation for Checker Agents](./temporary-files/mandatory-report-generation.md) — The requirement that \*-checker agents write reports to generated-reports/ with required tools. Use when building or reviewing a \*-checker agent.

## UUID Chain Generation

- [UUID Chain Generation](./temporary-files/uuid-chain-generation.md) — How agents generate the 6-character UUID chain, plus scope-based tracking and scope passing. Use when generating a report filename's UUID chain.
- [UUID Chain Generation — Startup and Tracking](./temporary-files/uuid-chain-startup-and-tracking.md) — The startup logic that builds the UUID chain, the write-tracking rule, and concurrency isolation. Use when implementing a checker/fixer agent's startup logic.
- [UUID Chain Generation — Limitations, Compatibility, and Rationale](./temporary-files/uuid-chain-limitations-and-rationale.md) — The concurrency limitation, backward compatibility for old filenames, and why the scheme is mandatory. Use when parsing an old-format report filename.

## Directory Purposes and Report Naming

- [Directory Purposes — generated-reports/ and Progressive Writing Requirement](./temporary-files/generated-reports-and-progressive-writing.md) — What generated-reports/ is for, and why checker agents must write progressively. Use when deciding what belongs in generated-reports/.
- [Progressive Writing Requirement — Requirements and Implementation Pattern](./temporary-files/progressive-writing-requirements-and-implementation.md) — The five progressive-writing requirements and the checker-agent list subject to the rule. Use when writing a checker agent's progressive-writing instructions.
- [Report File Naming Standard](./temporary-files/report-file-naming-standard.md) — The 4-part `{agent-family}__{uuid-chain}__{timestamp}__{suffix}.md` pattern, its separators, and why UUIDs/timestamps must be real. Use when constructing a checker or fixer report filename.
- [Report File Naming Standard — Repository Audit and Link Validation Reports](./temporary-files/report-file-naming-early-report-types.md) — Filename pattern and retention for repo-rules-checker and docs-link-checker reports. Use when naming a repo-rules-checker or docs-link-checker report.
- [Report File Naming Standard — Fixer Reports (Universal Pattern)](./temporary-files/fixer-reports-universal-pattern.md) — The shared fixer-report naming, audit-fix pairing, and content structure fixers follow. Use when a fixer agent generates its fix report.
- [Report File Naming Standard — Content, Documentation, and Plan Validation Reports](./temporary-files/report-file-naming-content-and-plan-reports.md) — Filename patterns for the content, docs, plan, and plan-execution families. Use when naming a content, docs, or plan report.
- [`local-tmp/`](./temporary-files/local-tmp-directory.md) — What local-tmp/ is for and the predicates for reclaiming anything inside it. Use when deciding if a file belongs in local-tmp/.

## Usage and Reference

- [Usage and Implementation for AI Agents](./temporary-files/usage-and-implementation.md) — When these directories apply and don't, plus implementation steps for both agent types. Use when deciding if a file belongs here.
- [Directory Status, Exceptions, and Related Conventions](./temporary-files/status-exceptions-and-related.md) — Confirms both directories are gitignored and when another convention overrides this default. Use when confirming gitignore status.

---
name: docs-converting-pdf-to-markdown
description: PDF-to-Markdown conversion fidelity — the crane CLI, criticality levels, and workflow steps shared by the pdf-to-md maker/checker/fixer family
---

# Converting PDF to Markdown

A Markdown file converted from a PDF must be a verbatim, complete representation of its source:
every passage, table, heading level, list-nesting depth, figure, and diagram preserved.

## When This Skill Loads

Auto-loads for `pdf-to-md-maker`, `pdf-to-md-checker`, and `pdf-to-md-fixer`.

## Reference Modules

- [reference/01-checking-fidelity.md](./reference/01-checking-fidelity.md) — the checker's
  seven-dimension validation workflow, `crane check-*` commands, criticality table, and audit
  report format.

## Tools Usage

- **Bash**: `crane` (pdf/text/heading/nesting/table/figure/mermaid/ocr/report/skiplist commands),
  `diff` for comparison
- **Read**: source Markdown and temporary extracted text files
- **Glob**: locate the MD file when path not specified
- **Grep**: search MD for text segments, count figures, find Mermaid blocks
- **Write**: progressive audit/fix reports to `generated-reports/`

## Reference Documentation

- [pdf-to-md-quality-gate workflow](../../../repo-governance/workflows/content/pdf-to-md-quality-gate.md)

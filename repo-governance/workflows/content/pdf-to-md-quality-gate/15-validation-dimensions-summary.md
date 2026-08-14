---
title: "Validation Dimensions Summary"
description: "Table mapping each validation dimension to its responsible agent, crane command, and auto-fixability."
when_to_use: "Use as a quick reference for which crane command backs a given validation dimension."
---

# Validation Dimensions Summary

| Dimension                                       | Agent   | crane Command                          | Auto-Fixable                                                               |
| ----------------------------------------------- | ------- | -------------------------------------- | -------------------------------------------------------------------------- |
| Text completeness (missing sections/paragraphs) | checker | `crane text --check "$PDF" "$MD"`      | Yes (re-extract from PDF)                                                  |
| Text accuracy (wrong words)                     | checker | `crane text --search "$MD" "$SEGMENT"` | Yes (re-extract from PDF)                                                  |
| Heading level accuracy (`#` depth vs PDF)       | checker | `crane heading --check "$PDF" "$MD"`   | Yes (re-derive from layout heuristic)                                      |
| Content nesting accuracy (list/block depth)     | checker | `crane nesting --check "$PDF" "$MD"`   | Yes (re-extract with layout output)                                        |
| Table integrity (missing/wrong data)            | checker | `crane table --check "$PDF" "$MD"`     | Yes (re-extract from PDF)                                                  |
| Figure coverage (Mermaid or placeholder)        | checker | `crane figure --check "$PDF" "$MD"`    | Yes (add placeholder)                                                      |
| Mermaid syntax validity                         | checker | `crane mermaid --validate "$MD"`       | Yes (fix syntax)                                                           |
| OCR quality (gibberish rate)                    | checker | `crane ocr --quality "$MD"`            | No (manual review)                                                         |
| Structural order (section sequence)             | checker | (heuristic from text+heading checks)   | Partial (re-ordering risky)                                                |
| **All-in-one aggregator**                       | checker | `crane check-all "$PDF" "$MD"`         | Mixed (per-dimension; may time out on large PDFs — see Large-PDF fallback) |

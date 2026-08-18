---
title: "The Split — Deterministic vs AI Validation Categories"
description: The table mapping each governance validation category to its owning layer (deterministic preflight or AI checker) and the rationale.
when_to_use: Use when deciding, or looking up, which layer (deterministic preflight or AI checker) owns a given validation category.
category: explanation
subcategory: conventions
tags:
  - conventions
  - governance
  - validation
  - quality-gate
  - automation
created: 2026-08-13
---

# The Split

| Category                          | Owner         | Rationale                                                                                  |
| --------------------------------- | ------------- | ------------------------------------------------------------------------------------------ |
| `governance-word-budget`          | Deterministic | Whole-file word count against a per-surface threshold                                      |
| `frontmatter-audit`               | Deterministic | YAML parse + regex against frontmatter and body                                            |
| `traceability-audit`              | Deterministic | Walk + regex for required H2 sections                                                      |
| `license-audit`                   | Deterministic | File existence + SPDX line comparison against notice table                                 |
| `readme-index-audit`              | Deterministic | Diff README link list vs actual `*.md` siblings                                            |
| `emoji-audit`                     | Deterministic | Rune scan for codepoint ranges                                                             |
| `layer-coherence`                 | Deterministic | Regex extraction + cross-doc set comparison                                                |
| `docs-validate-naming`            | Deterministic | Basename regex                                                                             |
| `docs-validate-frontmatter`       | Deterministic | Per-area required-field schema                                                             |
| `docs-validate-heading-hierarchy` | Deterministic | Tokenize headings + level-skip check                                                       |
| `agents-detect-duplication`       | Deterministic | Sliding-window SHA-256 verbatim match                                                      |
| Paraphrased duplication           | AI checker    | Requires semantic judgement — same meaning, different words                                |
| Terminology alignment             | AI checker    | Cross-doc concept naming consistency requires judgement                                    |
| Contradictions                    | AI checker    | Identifying two passages that disagree requires reading both                               |
| Inaccuracies                      | AI checker    | Comparing a passage against ground truth requires the judgement that the truth is known    |
| Principle-appropriateness         | AI checker    | "Does this convention follow Simplicity Over Complexity?" is a value judgement, not a fact |
| Content quality (alt text, voice) | AI checker    | Judging a passage as "active voice" or alt text as "useful" requires reading the content   |

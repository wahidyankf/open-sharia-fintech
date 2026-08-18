---
name: readme-fixing-quality
description: How readme-fixer re-validates readme-checker findings, assesses HIGH/MEDIUM/FALSE_POSITIVE confidence for README-specific issues, and applies fixes only for objective/verifiable problems. Use when re-validating or applying README quality fixes.
when_to_use: When acting as readme-fixer — re-validating a readme-checker finding, deciding whether a README issue is objective enough to auto-fix, or applying a paragraph-length/jargon/acronym/passive-voice fix.
---

# README Fixing Quality

## Overview

`readme-fixer` never trusts checker findings blindly — every finding is re-validated before a
fix is applied, and fixes apply only to objective, verifiable issues. Subjective quality
assessments (tone, engagement, emoji placement) are always flagged for manual review, never
auto-fixed.

## Reference Modules

- [01-domain-confidence-examples.md](./reference/domain-confidence-examples.md) — README-specific
  HIGH / MEDIUM / FALSE_POSITIVE examples
- [02-high-confidence-validation-checks.md](./reference/high-confidence-validation-checks.md) —
  the four objective checks (paragraph length, jargon pattern, acronym context, passive voice)
  with exact bash re-validation patterns
- [03-medium-confidence-and-safeguards.md](./reference/medium-confidence-and-safeguards.md) —
  the four subjective categories that always get flagged, plus refusal conditions, required
  output, and convergence safeguards

## Core Principles

1. **Re-validation is mandatory** — never skip it, a file may have changed since the audit.
2. **Objective issues only auto-fix** — line counts and pattern matches are objective; tone and
   engagement are not.
3. **Use the EXACT SAME patterns as `readme-checker`** — consistency between checker and fixer
   is critical; a mismatch indicates a checker issue, not a fixer judgment call.
4. **Report everything** — fixed, skipped, and flagged decisions all belong in the fix report for
   audit trail and checker-improvement feedback.

## Related Skills

`repo-assessing-criticality-confidence` (universal confidence system this specializes),
`repo-applying-maker-checker-fixer` (the fixer workflow shape), `readme-writing-readme-files`
(the quality standard being fixed toward).

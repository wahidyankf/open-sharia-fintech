---
title: "Termination Criteria"
description: "Defines the pass, partial, and fail termination criteria for each quality mode (lax/normal/strict/ocd)."
when_to_use: "Use when determining what condition ends the workflow, or when choosing a quality mode."
---

# Termination Criteria

**Success** (`pass`):

- **lax**: Zero CRITICAL findings on 2 consecutive checks (HIGH/MEDIUM/LOW may exist)
- **normal**: Zero CRITICAL/HIGH findings on 2 consecutive checks (MEDIUM/LOW may exist)
- **strict**: Zero CRITICAL/HIGH/MEDIUM findings on 2 consecutive checks (LOW may exist)
- **ocd**: Zero findings at all levels on 2 consecutive checks

**Partial** (`partial`):

- Threshold-level findings remain after max-iterations
- Some findings require manual intervention (OCR quality, ambiguous diagram type)
- Some fixer operations failed

**Failure** (`fail`):

- Required CLI tool not found (`pdftotext`, `tesseract`)
- Source PDF unreadable or corrupt
- Output MD file could not be written

**Note**: Below-threshold findings are reported in final audit but don't prevent success status.
Success requires two consecutive zero-finding validations (consecutive pass requirement).

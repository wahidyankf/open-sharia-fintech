---
title: "Safety Features"
description: "Documents infinite-loop prevention, convergence safeguards, false-positive protection, and graceful degradation behavior."
when_to_use: "Use when verifying the workflow's safety guarantees or diagnosing a stuck/non-converging run."
---

# Safety Features

**Infinite Loop Prevention**:

- max-iterations defaults to 7
- Escalation warning at iteration 5

**Convergence Safeguards**:

- Checker loads `local-tmp/.known-false-positives.md` at each iteration start
- Fixer persists new FALSE_POSITIVEs to that same file in `local-tmp/pdf-to-md/`
- Step 5 (Re-validate) uses changed-sections-only scan when called after Step 4 (Apply Fixes)

**False Positive Protection**:

- Fixer re-validates each finding before applying
- FALSE_POSITIVE findings skipped and logged
- Stable key format prevents duplicate skip list entries

**Graceful Degradation**:

- Missing `tesseract` → fail early with install instructions (image-only PDFs)
- Missing `pdftotext` → fail early with install instructions (all PDFs)
- Missing `mmdc` → Mermaid validation falls back to syntax-only inspection

**Manual Intervention Flags**:

- OCR quality disputes: flagged in fix report, not auto-applied
- Ambiguous diagram types: kept as `[FIGURE N: ...]` placeholder

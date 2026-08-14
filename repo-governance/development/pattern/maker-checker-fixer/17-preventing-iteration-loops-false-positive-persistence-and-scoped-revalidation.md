---
title: "Preventing Iteration Loops — False-Positive Persistence and Scoped Re-validation"
description: "The first two safeguards against iteration loops."
category: explanation
subcategory: development
tags:
  - maker-checker-fixer
  - workflow
  - content-quality
  - agent-patterns
  - validation
  - automation
created: 2025-12-14
when_to_use: "Use when a checker re-flags a false positive."
---

# Preventing Iteration Loops — False-Positive Persistence and Scoped Re-validation

Without explicit mechanisms to track accepted decisions, checker-fixer workflows can enter infinite or very long iteration loops. This section defines the three structural safeguards that prevent runaway iterations.

## 1. FALSE_POSITIVE Persistence (`.known-false-positives.md`)

**Problem**: Checker re-flags the same accepted FALSE_POSITIVE findings on every iteration because it has no memory of previous decisions.

**Solution**: Fixer writes all accepted FALSE_POSITIVE findings to `generated-reports/.known-false-positives.md`. Checker reads this file at the start of every run and skips any matching entries.

**Key format**: `[category] | [file] | [brief-description]` — stable across runs.

**Checker behavior**: When a finding matches the skip list, log as `[PREVIOUSLY ACCEPTED FALSE_POSITIVE — skipped]` in the informational section. Do NOT count in findings total.

**Fixer behavior**: At end of every fix report, append each FALSE_POSITIVE to `.known-false-positives.md` and include an `## Accepted FALSE_POSITIVE Findings` section in the fix report.

## 2. Scoped Re-validation (Changed Files Only)

**Problem**: Full-repo scan on every iteration re-validates all ~265 software documentation files even when the fixer only changed 3-4 agent files.

**Solution**: Fixer captures `git diff --name-only HEAD` after applying fixes and includes the list in the fix report under `## Changed Files (for Scoped Re-validation)`. Checker in re-validation mode (identified by multi-part UUID chain like `abc123_def456`) focuses Step 8 validation only on the listed changed files.

**Result**: Subsequent iterations are 10-50x faster, reducing unnecessary work on unchanged content.

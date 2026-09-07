---
description: "Overview of the fixer confidence-level system."
when_to_use: "Use to orient to the fixer confidence-level system."
---

# Overview

## What This Convention Defines

This convention establishes:

- **Three confidence levels** - HIGH, MEDIUM, FALSE_POSITIVE
- **When to apply fixes automatically** - HIGH confidence only
- **When to skip fixes** - MEDIUM (manual review) and FALSE_POSITIVE (report to user)
- **Universal criteria** - Applicable across all fixer agents regardless of domain
- **Domain-specific examples** - How each fixer agent applies the system

## Why Confidence Levels Matter

Without a standardized confidence assessment system, automated fixers can:

- **Over-apply fixes** - Modify content that shouldn't be changed (subjective quality improvements, ambiguous cases)
- **Create false changes** - Apply fixes based on incorrect checker findings (false positives)
- **Break functionality** - Make changes in contexts where checker's fix suggestion was wrong
- **Erode trust** - Users lose confidence when automated fixes produce unexpected results

With confidence levels:

- PASS: **Safety** - Only high-confidence, objective fixes applied automatically
- PASS: **Transparency** - Users know why fixes were applied or skipped
- PASS: **Efficiency** - Obvious objective issues fixed without manual intervention
- PASS: **Quality** - Subjective improvements flagged for human judgment
- PASS: **Feedback loop** - False positives reported to improve checker accuracy

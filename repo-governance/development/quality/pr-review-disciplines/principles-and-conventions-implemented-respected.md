---
description: "Principles/conventions implemented."
when_to_use: "Use to trace rationale."
---

# Principles and Conventions Implemented/Respected

## Principles Implemented/Respected

This convention implements/respects the following core principles:

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**:
  the boundary tie-breaker rule and each specialist's `SUPPRESS` block turn "which discipline
  should catch this?" and "what should a reviewer never raise?" from an implicit, ad-hoc judgment
  call into a documented lookup every specialist and the coordinator apply the same way.
- **[Root Cause Orientation](../../../principles/general/root-cause-orientation.md)**: separating the
  CI-gaming/test-integrity discipline from correctness lets a reviewer trace a defect to its real
  root cause (a weakened test versus a genuinely wrong behaviour) instead of one generalist
  conflating the two into a single vague finding.
- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: the
  risk-tier fan-out keeps a trivial PR's review as simple as a single coordinator pass, reserving
  the full nine-specialist fan-out for diffs that actually need that much scrutiny.
- **[Automation Over Manual](../../../principles/software-engineering/automation-over-manual.md)**:
  the coordinator's dedup, re-categorize, reasonableness-filter, and tool-verify functions
  automate a second read of every raw finding that would otherwise require manual triage before a
  human ever sees it.

## Conventions Implemented/Respected

This convention implements/respects the following conventions:

- **[Criticality Levels Convention](.././criticality-levels.md)**: every specialist inherits the
  CRITICAL/HIGH/MEDIUM/LOW severity scale unchanged. This convention decides which discipline
  assigns a finding to which class, not how severity itself is defined.
- **[Maker-Checker-Fixer Pattern](../../pattern/maker-checker-fixer.md)**: extends that pattern's
  three-role idea into a fan-out variant — nine discipline-scoped makers plus one coordinator
  (a checker-like consolidation role) feed the unchanged `pr-review-fixer`.
- **[CI Blocker Resolution Convention](.././ci-blocker-resolution.md)**: the CI-gaming/test-integrity
  discipline's root-cause-first stance on weakened or skipped checks is this convention applied at
  review time, not just at author time.
- **[Regression Test Mandate](.././regression-test-mandate.md)**: the missing-regression-test check
  lives inside the CI-gaming/test-integrity discipline's owned scope, not correctness — a fix that
  lacks a pinning test is a test-integrity defect, not a behavioural one.
- **[Feature Change Completeness Convention](.././feature-change-completeness.md)**: the
  spec-file-presence-versus-scenario-completeness grey zone (ruling (d) below) exists precisely
  because that convention requires both a companion artifact to exist AND to be substantively
  adequate — two different disciplines check each half.

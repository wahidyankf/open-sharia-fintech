---
name: repo-harness-compatibility-protocol
description: The five deterministic cross-vendor parity invariants and seven external-drift dimensions shared by repo-harness-compatibility-checker (detection) and repo-harness-compatibility-fixer (remediation), plus each agent's own workflow and report format. Use when checking or fixing multi-harness binding drift.
when_to_use: When acting as repo-harness-compatibility-checker or repo-harness-compatibility-fixer — running/interpreting a Phase 0 invariant or Phase 1 drift dimension, or writing an audit/fix report.
---

# Repository Harness Compatibility Protocol

## Overview

Two agents share one taxonomy: five deterministic Phase 0 parity invariants (offline,
Bash-based) and seven Phase 1 external-drift dimensions (web-research-backed). The checker
detects; the fixer remediates what's safely mechanical and flags the rest for human judgment.

## Reference Modules

- [phase0-parity-invariants.md](./reference/phase0-parity-invariants.md) — the five
  invariants, each with detection tool/pass/fail/criticality AND fix scope (auto-fixable vs.
  human-required)
- [phase1-drift-dimensions-d1-d3.md](./reference/phase1-drift-dimensions-d1-d3.md) and
  [phase1-drift-dimensions-d4-d7.md](./reference/phase1-drift-dimensions-d4-d7.md) — the
  seven dimensions (D1–D7), each with drift indicator/criticality AND fix target/action
- [checker-workflow.md](./reference/checker-workflow.md) and
  [checker-finding-format.md](./reference/checker-finding-format.md) — the checker's own
  workflow steps, research delegation pattern, and finding format
- [fixer-confidence-and-scope.md](./reference/fixer-confidence-and-scope.md),
  [fixer-patterns-and-process.md](./reference/fixer-patterns-and-process.md), and
  [fixer-report-format.md](./reference/fixer-report-format.md) — the fixer's own confidence
  re-validation, fix patterns, process summary, fix report format, and FALSE_POSITIVE
  carry-forward

## Core Principles

1. **Phase 0 always runs in full**, even when Phase 1 is scoped to one harness.
2. **Only Invariant 3 (binding sync) and most Phase 1 dimensions auto-fix** — anything touching
   governance prose, root-instruction files, agent-set divergence, or a new color/tier mapping
   requires human judgment.
3. **Confidence propagates from the checker's cited source**: `[Verified]` → HIGH,
   `[Needs Verification]`/`[Unverified]` → MEDIUM (fixer downgrades and skips),
   `[Outdated]` → FALSE_POSITIVE.
4. **Conservative drift threshold** — flag substantive changes only (a different filename, a
   renamed directory, a removed required field), never minor wording differences.

## Related Agents

`repo-harness-compatibility-checker`, `repo-harness-compatibility-fixer`, `web-researcher`
(delegated Phase 1 research), `repo-rules-checker`/`repo-rules-fixer` (different scope).

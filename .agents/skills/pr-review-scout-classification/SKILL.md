---
name: pr-review-scout-classification
description: How pr-review-scout-maker classifies a PR's risk tier, selects the specialist fan-out set, assembles the shared-context brief once per cycle, and reads prior-cycle human-dismissal state. Use when acting as the PR-review pipeline's stage-0 scout.
when_to_use: When acting as pr-review-scout-maker at the start of a PR-review cycle — deciding risk tier, selecting specialists, assembling the shared-context brief, or reading prior-cycle thread-resolution status.
---

# PR Review Scout Classification

## Overview

`pr-review-scout-maker` is the PR-review pipeline's stage-0 scout: it never reviews code for a
defect and never posts a finding. Its entire job is deciding what the rest of the cycle sees —
risk tier, specialist set, shared context, and prior-cycle human decisions nobody should
re-litigate.

## Reference Modules

- [risk-tier-and-specialist-selection.md](./reference/risk-tier-and-specialist-selection.md) —
  the trivial/lite/full thresholds, the security-sensitive-path override, and the Content-Type
  Applicability Filter (DD-10)
- [shared-context-and-prior-cycle-read.md](./reference/shared-context-and-prior-cycle-read.md) —
  assembling the once-per-cycle shared-context brief (no-exclusion posture, large-diff slicing),
  and reading prior-cycle thread-resolution/human-dismissal state
- [correction-record-freeze.md](./reference/correction-record-freeze.md) — omitting the loop's own
  `plans/**` prose from cycle 2, and the plans-only and security carve-outs that survive it
- [untrusted-input-and-output-contract.md](./reference/untrusted-input-and-output-contract.md) —
  this agent's first-ingestion-point untrusted-input handling, the trivial-tier handoff, and the
  three-part output contract

## Core Principles

1. **Classification and assembly only — never reviewing.** This agent never originates a finding
   and never calls the GitHub Reviews API.
2. **Re-evaluate every cycle, never cache.** Tier, specialist set, and the content-type filter are
   freshly re-derived each cycle since the fixer's own commits can change the diff.
3. **Security-sensitive paths force `full` regardless of size** — non-negotiable.
4. **First and only ingestion point for raw PR text** — every downstream consumer reads only this
   agent's derived outputs, never the raw text itself.

## Related Agents

`pr-review-synthesis-maker` (receives this agent's tier/set/brief every cycle), the nine
`pr-review-*-maker` discipline specialists (selected from, per cycle), `pr-review-fixer`.

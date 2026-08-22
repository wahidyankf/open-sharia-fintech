---
title: "PR-Review Quality Gate — Convergence Measurement"
description: "How the loop distinguishes genuine convergence from its own exhaust: the three cause tags carried on every disposition, the two series they produce, and the every-third-cycle checkpoint that reads them."
when_to_use: "Use at every third cycle, and whenever deciding to continue, change fix strategy, block, or extend a ceiling."
---

# Convergence Measurement

A raw finding count does not measure convergence. It sums two unrelated quantities: defects in the
change under review, and defects the loop's own fixes created. On PR #249 the second was 63% of the
63 findings posted in cycles two through six, so the count stayed high while the change was
nearly clean.

## Every Disposition Carries a Cause

The `ose-pr-review-disposition:v2` block on each fixer reply names exactly one:

- `original` — a defect in the change as first written.
- `class-escape` — the same class re-escaping after a fix closed only the instance named.
- `fix-induced` — created by a previous cycle's fix.

The fixer tags it: only the fixer knows which commit introduced the line.

A finding can satisfy two of them — a class re-escaping through a line a previous fix wrote is both
`class-escape` and `fix-induced`. **The latest applicable cause governs**: `fix-induced` over
`class-escape` over `original`. Tagging by the earliest would bill the loop's own exhaust to the
change under review — the confusion these tags exist to remove.

## The Two Series

- **Original-defect series** — `original` per cycle. It falls as review does its job, and it is the
  series the exit and block decisions read.
- **Induced rate** — (`class-escape` + `fix-induced`) ÷ total, per cycle. It rises as the loop
  starts reviewing itself.

A cycle whose findings are all `fix-induced` says the change is clean and the fixing is the problem
— a different remedy from another review pass.

## The Checkpoint, Every Third Cycle

**The orchestrator** stops after cycles three, six, nine …, reads both series, and records the verdict in [the cycle's audit record](../../../../.claude/skills/pr-review-synthesis-coordination/reference/machine-readable-audit-record.md):

- **Continue** — original defects are falling and the induced rate is not rising.
- **Change fix strategy** — the induced rate is high. Attack the mechanism, not the surface — most
  often [restatement by value](./restatement-by-value.md).
- **Block** — original defects persist and are not falling.

Extending a ceiling when the checkpoint shows a falling original-defect series is a per-PR override,
recorded on the PR and citing both series. It funds attempts and
[never waives a finding](./notes.md).

## Vary the Probe

A cycle repeating the previous cycle's question converges on that question, not on correctness,
and one clean cycle is evidence about one probe. Both rules, the probe-class register, and the
exit condition they define live in
[probe variation and what makes a cycle clean](./probe-variation-and-exit.md).

## Enforcement

None automated. A violation is visible as a fixer reply carrying no cause tag, or a checkpoint
cycle whose audit record has no `checkpoint` block.

---
title: "PR-Review Quality Gate — Convergence Measurement"
description: "How the loop distinguishes genuine convergence from its own exhaust: the three cause tags carried on every disposition, the two series they produce, the every-third-cycle checkpoint, and the probe-variation rule."
when_to_use: "Use at every third cycle, and whenever deciding to continue, change fix strategy, block, or extend a ceiling."
---

# Convergence Measurement

A raw finding count does not measure convergence. It sums two unrelated quantities: defects in the
change under review, and defects the loop's own fixes created. On PR #249 the second was 63% of 63
findings, so the count stayed high while the change itself was nearly clean.

## Every Disposition Carries a Cause

The `ose-pr-review-disposition:v2` block on each fixer reply names exactly one:

- `original` — a defect in the change as first written.
- `class-escape` — the same class re-escaping after a fix closed only the instance named.
- `fix-induced` — created by a previous cycle's fix.

The fixer tags it, because only the fixer knows which commit introduced the line. Three tags and no
more: a taxonomy nobody applies consistently measures nothing.

## The Two Series

- **Original-defect series** — `original` per cycle. It falls as review does its job, and it is the
  series the exit and block decisions read.
- **Induced rate** — (`class-escape` + `fix-induced`) ÷ total, per cycle. It rises as the loop
  starts reviewing itself.

A cycle whose findings are all `fix-induced` says the change is clean and the fixing is the problem.
That calls for a different remedy than another review pass.

## The Checkpoint, Every Third Cycle

Stop after cycles three, six, nine … read both series, and record one of:

- **Continue** — original defects are falling and the induced rate is not rising.
- **Change fix strategy** — the induced rate is high. Attack the mechanism making surface rather
  than the surface, most often [restatement by value](./restatement-by-value.md).
- **Block** — original defects persist and are not falling.

Extending a ceiling to avoid resolving a finding stays forbidden. Extending one when the checkpoint
shows a falling original-defect series is a per-PR override, recorded on the PR, citing both series.

## Vary the Probe

A cycle repeating the previous cycle's question converges on that question, not on correctness. Six
cycles on PR #249 walked past a catastrophic-backtracking hole in an allowed command shape; the
seventh found it because the brief asked something different. Each cycle's scout states how this
cycle's probe differs — a different failure mode, a different reader, a different level. A clean
cycle counts as clean only under a probe unlike the one before it.

---
title: "PR-Review Quality Gate — Probe Variation and What Makes a Cycle Clean"
description: "The probe-class register, and the two-clean-cycle exit rule."
when_to_use: "Use when a scout plans a cycle's probe, and whenever deciding that a clean cycle ends the loop."
---

# Probe Variation and What Makes a Cycle Clean

A cycle repeating the previous cycle's question converges on that question, not on correctness. Each
cycle's scout states how the probe differs — a different failure mode, reader, or level.

## Measured on PR #249

Cycles five through ten each returned zero or one original defect and read as converged. Cycle
eleven asked three questions no earlier cycle had asked and found six; cycle twelve asked three more
and found five. All eleven had been in the diff since cycle one. The flat stretch measured **probe
exhaustion, not correctness** — a loop cannot find what it never asks about.

## The Probe-Class Register

Each PR's review record names the probe class every cycle used, so "a new probe" is checkable rather
than asserted. Classes used on PR #249: rule consistency, security shape, restatement, cross-repo
divergence, adversarial dismissal, inert-rule deletion, clause durability, PR-body drift, and
enforcement-disposition completeness.

Naming the class is what makes the register useful. "A different question" describes every cycle;
"the same class as cycle nine" is falsifiable.

## What Ends the Loop

_Clean_ keeps its single definition — a cycle leaving zero unresolved code-related
MEDIUM/HIGH/CRITICAL findings, stated once in
[loop-exit and block rules](./loop-exit-and-block-rules.md). This file adds the second
condition, not a second definition.

**A loop exits when two consecutive clean cycles each run a probe class not previously used on
that PR.** One clean cycle is evidence about one question. Two clean cycles under two unused
classes is the weakest available evidence that the questions have run out, and it is still weak —
a stopping rule, not a proof of correctness.

It does not change the cycle ceiling, which bounds effort rather than measuring convergence, and
which is [extended only per-PR](./convergence-measurement.md).

A ceiling reached before the exit condition holds is a `blocked` PR, not a clean one. Reaching the
ceiling never converts an unmet exit condition into a met one.

## Enforcement

None automated. A violation is visible as two cycles whose scouts named the same probe class, or as
an exit declared on a single clean cycle.

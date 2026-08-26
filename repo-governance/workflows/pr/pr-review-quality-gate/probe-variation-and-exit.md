---
title: "PR-Review Quality Gate — Probe Variation and What Makes a Cycle Clean"
description: "The probe-class register, and the two-clean-cycle exit rule."
when_to_use: "Use when a scout plans a cycle's probe, and whenever deciding that a clean cycle ends the loop."
---

# Probe Variation and What Makes a Cycle Clean

A cycle repeating the previous cycle's question converges on that question, not on correctness. Each
cycle's scout states how the probe differs — a different failure mode, reader, or level.

## The Probe-Class Register

Each PR's review record names the probe class every cycle used, so "a new probe" is checkable rather
than asserted. That record is the register; this file does not carry a second copy, which would go
stale within a cycle and make the exit rule return the wrong answer.

Naming the class is what makes the register useful. "A different question" describes every cycle;
"the same class as cycle nine" is falsifiable.

The changed probe also respects the frozen delivery outcome. It may test a different failure mode,
reader, or level of the shipped seam, but it does not introduce an unrelated improvement merely to
make a later cycle look productive. Record an unrelated observation as a reasoned reject or linked
follow-up instead.

## What Ends the Loop

_Clean_ keeps its single definition — a cycle leaving zero unresolved code-related
MEDIUM/HIGH/CRITICAL findings, stated once in
[loop-exit and block rules](./loop-exit-and-block-rules.md). This file adds the second
condition, not a second definition.

**A loop exits when two consecutive clean cycles each run a probe class not previously used on
that PR.** One clean cycle is evidence about one question. Two clean cycles under two unused
classes is the weakest available evidence that the questions have run out, and it is still weak —
a stopping rule, not a proof of correctness.

Each clean result exists only when its authenticated positive post-CI
[Cycle Credit Record](./cycle-non-credit-record.md) exists. Restart hydration never infers either
member of the pair from review prose, resolved threads, or a green check observed later.

It does not change the cycle ceiling, which bounds effort rather than measuring convergence, and
which is [extended only per-PR](./convergence-measurement.md).

A ceiling reached before the exit condition holds is a `blocked` PR, not a clean one. Reaching the
ceiling never converts an unmet exit condition into a met one.

That includes the case where **nothing is outstanding**: five cycles run, the last two are clean,
but one repeats an earlier class. The condition is unmet, so the PR is `blocked` with zero findings.
Its only lawful resolution is a recorded per-PR ceiling extension — which is permitted here, because
there is no finding for the extension to avoid resolving.

## Enforcement

None automated. A violation is visible as two cycles whose scouts named the same probe class, or as
an exit declared on a single clean cycle.

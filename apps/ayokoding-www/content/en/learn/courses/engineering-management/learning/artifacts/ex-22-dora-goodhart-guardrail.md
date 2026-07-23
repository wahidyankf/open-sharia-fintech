---
title: "Artifact: DORA-Goodhart Guardrail — Deployment Frequency"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 62
---

> A design that uses DORA metrics for team-level diagnosis without turning them into an individual
> scorecard -- exercises co-11. Everline and every name here are fictional; every detail is an
> illustrative, constructed example.

**The gaming risk being guarded against**: deployment frequency, treated as an individual or team
target rather than a diagnostic, can be inflated by splitting one meaningful change into several
trivial deploys (a whitespace commit, then the real change, then a comment fix) -- the number goes
up, the underlying delivery capability doesn't.

**The guardrail**: DORA numbers stay reported at the team level only, reviewed quarterly as a
diagnostic input to the next prioritization pass, never reported per-engineer and never referenced
in any individual's performance calibration. Alongside deployment frequency, the team also tracks a
simple qualitative check each quarter: "did anything ship this quarter that felt trivially split
just to move the number?" -- asked directly in the retro, so gaming would have to survive being
named out loud by a teammate.

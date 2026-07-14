---
title: "Artifact: Memo — Why Velocity-Linked Bonuses Backfire"
date: 2026-07-14T00:00:00+07:00
draft: false
weight: 59
---

> Comet team -- velocity-as-target memo -- exercises co-14, co-05.

Story points are relative-size estimates a team produces about its own future work -- they are not an
externally measured unit like lines of code or a stopwatch. The instant a team's average velocity
affects its own bonus, the team gains a direct, rational incentive to inflate its estimates: the same
story that used to be called a 5 gets called an 8, with zero change to the actual work. This is
Goodhart's Law in its purest form -- the measure becomes the target, and stops being a good measure
the moment it does.

The damage is not limited to unfairness between teams. It also destroys the number's original,
legitimate use: once a team's own historical velocity is inflated, that team's own future sprint
forecasts become meaningless too, because they are built on an average that no longer means what it
used to.

**Proposed alternative**: reward outcome metrics the team does not control the raw units of --
cycle-time trend (computed independently of any self-report; a team cannot "estimate" its way to a
shorter cycle time) and defect-escape rate. Neither can be inflated by a team simply agreeing to call
things bigger.

---
title: "Artifact: Shape Up Pitch — Kestrel Swap-Approval Redesign"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 69
---

> A Shape Up pitch for the fast-path swap-approval feature -- exercises co-25. Kestrel is a
> fictional product; every quoted number, question, or finding here is an illustrative,
> constructed example, not real data or a real transcript.

**Appetite**: 6 weeks, fixed. Not an estimate -- if the shaped solution below can't be built to a
demoable state in 6 weeks, the scope shrinks; the appetite does not extend.

**Problem**: routine shift-swap requests sit unapproved for hours because manual review, buried in
notifications, gets missed.

**Solution outline** (breadboard level): an approval queue screen for unusual swaps; a fast-path
SMS one-tap reply for routine swaps meeting the FAQ's eligibility rule; a per-team toggle to
disable fast-path entirely.

**Rabbit holes** (explicitly named, to avoid): do not build a general-purpose, configurable
approval-workflow engine -- the eligibility rule is fixed logic, not a rules builder. Do not
support swap chains involving more than two people (A swaps with B who swaps with C) -- single
pairwise swaps only, this cycle.

**No-gos**: cross-location shift swaps (a shift moving between two different store locations) --
explicitly out of scope for this cycle, revisit later.

**Circuit-breaker**: if the fast-path SMS flow and the per-team toggle aren't both demoable by the
end of week 5, cut the approval-queue screen redesign from this cycle's scope and ship
fast-path-only against the existing review screen, rather than extending the appetite past 6
weeks.

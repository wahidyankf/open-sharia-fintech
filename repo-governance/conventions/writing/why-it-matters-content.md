---
title: "Why It Matters Content Convention"
description: Rule prohibiting corporate case studies and fabricated platform scenarios in Why It Matters sections of ayokoding-www tutorials; requires theoretical explanations only
category: explanation
subcategory: conventions
tags:
  - ayokoding-www
  - tutorial-content
  - factual-accuracy
  - why-it-matters
  - hallucination-prevention
created: 2026-05-09
when_to_use: Read this before writing or reviewing a Why It Matters section in an ayokoding-www tutorial.
---

# Why It Matters Content Convention

This convention defines the content rules for `**Why It Matters**:` sections in
ayokoding-www tutorials. These sections must use theoretical explanations only.
Corporate case studies, anecdotal company events, and fabricated platform scenarios
are prohibited regardless of how plausible they appear.

## Contents

- [Purpose and Scope](./why-it-matters-content/purpose-and-scope.md) — the principles behind the rule, the problem it solves, and which files it covers.
- [Standards](./why-it-matters-content/standards.md) — the four content standards: theoretical explanations only, prohibited patterns, the suspension test, and permitted reference patterns.
- [Examples: Fabricated Anecdotes](./why-it-matters-content/examples-fabricated-anecdotes.md) — before/after rewrites of a fabricated corporate case study and a fabricated platform scenario.
- [Tools, Automation, and References](./why-it-matters-content/tools-and-references.md) — the checker/fixer agents that enforce this convention and its related conventions and principles.

## Example: Verifiable Fact Used Correctly

**PASS: Permitted (citable event with named source)**

```markdown
**Why It Matters**: Unit mismatches between subsystems can have catastrophic
consequences even in mission-critical engineering. NASA's Mars Climate Orbiter
($327M total mission cost) was lost in 1999 because one engineering team used
pound-force seconds while another used newton-seconds — a mismatch that went
undetected until the spacecraft entered the wrong orbit. Strong typing that
encodes units at the type level makes this class of error a compile-time
failure rather than a runtime disaster.
```

This is permitted because the NASA event is documented in the official accident
investigation report, and the fact is citable.

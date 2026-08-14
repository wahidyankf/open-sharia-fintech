---
title: "Example: Verifiable Fact Used Correctly"
description: A worked example of a Why It Matters section that cites a real, sourced historical event correctly
category: explanation
subcategory: conventions
tags:
  - ayokoding-www
  - tutorial-content
  - factual-accuracy
  - why-it-matters
  - hallucination-prevention
created: 2026-05-09
when_to_use: Read this when deciding whether a citable historical fact may be used in a Why It Matters section.
---

# Example: Verifiable Fact Used Correctly

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

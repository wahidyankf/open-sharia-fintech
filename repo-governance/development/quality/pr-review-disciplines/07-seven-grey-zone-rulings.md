---
title: "Seven Grey-Zone Rulings"
description: "The tie-breaker pre-resolved for seven recurring cases."
category: explanation
subcategory: development
tags:
  - pr-review
  - governance
  - agents
  - quality-gates
  - boundary-rules
created: 2026-07-23
when_to_use: "Use for a recurring grey-zone finding-ownership question."
---

# Seven Grey-Zone Rulings

The nine-discipline split creates recurring boundary questions between adjacent disciplines. The
following seven are pre-decided so the coordinator applies a lookup instead of re-deriving the
tie-breaker every cycle. Four are core to the original discipline set; two were added when
performance and documentation-quality became their own disciplines (D1); one more was added when
type-soundness became its own discipline.

- **(a) New cross-module dependency.** A violation of an existing layering rule → governance; a
  genuinely novel boundary judgment → architecture. (This is the tie-breaker's own worked example:
  reviewing a new cross-module dependency, an already-documented layering violation is governance's
  finding, while a boundary question no existing rule answers is architecture's.)
- **(b) Naming format vs. should-this-boundary-exist.** Mechanical naming/structure conformance
  (does this follow the documented naming pattern?) → governance; whether the module boundary
  itself should exist at all → architecture.
- **(c) Error-handling shape vs. domain error scenarios.** The _shape_ of error handling (does it
  follow the documented error-handling convention?) → governance; whether the domain's actual error
  scenarios are correctly covered (Gherkin edge/error-case conformance) → correctness (logic).
- **(d) Spec-file presence vs. scenario completeness.** Whether a required spec file exists at all
  → governance; whether the scenarios inside it are complete for the domain → correctness (logic).
- **(e) Performance ↔ architecture.** A quality-attribute tradeoff decision (accept a performance
  cost for a design benefit) → architecture; a concrete or likely measured regression on a hot path
  → performance.
- **(f) Docs ↔ governance.** Mechanical doc-convention conformance (heading hierarchy, linking,
  naming, alt-text as a rule) → governance; substantive doc completeness/clarity/drift →
  documentation-quality (docs).
- **(g) Compiles vs. is sound vs. should the boundary exist.** This boundary is three-way, not two-way.
  Code that compiles cleanly can still defeat type soundness via an escape hatch (unsafe cast, `any`,
  `unsafe` block, `!` suppression); a clean compile is NOT evidence against a type-soundness
  finding — the type-soundness discipline owns escape-hatch _usage_ regardless of whether the build
  succeeds. The third leg is a type/module-boundary tradeoff, not an escape-hatch-usage question:
  whether a new type or module boundary should exist at all → architecture (the same
  should-this-boundary-exist judgment as ruling (b), applied to types).

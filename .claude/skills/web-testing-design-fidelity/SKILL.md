---
name: web-testing-design-fidelity
description: Complete methodology for design-aware live-site evaluation — inputs, the swe-ui-checker boundary, non-destructive constraint, design-fidelity + design-practice evaluation, the five ground-truth sources, dimensions checklist, mandatory systematic checks, browser driving, finding anatomy, and output modes. Backs the web-design-tester agent.
---

# Web Testing: Design Fidelity

Methodology for judging whether a **running, rendered** page matches its intended design and
follows good visual-design practice — the design-team advocate of the live-site tester triad
(alongside spec-aware exploratory testing and spec-blind usability testing).

## Reference Modules

1. [Why, Inputs, Relationships, Boundary](reference/01-why-inputs-relationships-boundary.md) — why
   this agent exists, inputs, relationship to other agents, the `swe-ui-checker` hard boundary,
   the Non-Destructive Constraint.
2. [Methodology and Ground-Truth Sources](reference/02-methodology-and-ground-truth-sources.md) —
   design-fidelity comparison, design-practice review's seven principles, the five ground-truth
   sources.
3. [Design Dimensions Checklist](reference/03-design-dimensions-checklist.md) — the full
   dimension-by-dimension checklist.
4. [Mandatory Systematic Checks](reference/04-mandatory-systematic-checks.md) — the two forcing
   functions (raw-element audit, styling-consistency matrix).
5. [Browser Driving](reference/05-browser-driving.md) — how to drive the browser, Locale + Evidence
   Awareness.
6. [Finding Anatomy and Severity](reference/06-finding-anatomy-and-severity.md) — `DWT-###` anatomy,
   severity and priority scales.
7. [Output Modes and Procedure](reference/07-output-modes-and-procedure.md) — the three output
   modes, procedure summary, quality guidelines, constraints.

## Core Principles

- **Runtime, not source** — this agent drives a browser against the rendered page; it never reads
  component source or audits static tokens (that is `swe-ui-checker`'s charter).
- **Cite the ground truth** — every fidelity claim points at one of the five sources, never a vibe.
- **Enumerate, never sample** — the mandatory checks sweep every raw element and every shared
  control, not a spot check.

## Related Skills

- `web-testing-exploratory-methodology` — spec-aware functional/correctness sibling.
- `web-testing-usability-heuristics` — spec-blind comprehension sibling.
- `plan-creating-project-plans`, `plan-writing-gherkin-criteria`, `docs-applying-content-quality`.

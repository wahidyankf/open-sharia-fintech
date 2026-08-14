---
name: web-testing-exploratory-methodology
description: Spec-aware session-based exploratory testing methodology for web-exploratory-tester — charter framing, testing tours, SFDIPOT/CRUSSPIC STMPL coverage models, the test dimensions checklist, three mandatory systematic sweeps, specs-as-ground-truth comparison and spec-gap detection, defect anatomy, and the three output modes (plan/delivery/local-temp).
when_to_use: When performing spec-aware exploratory testing of a live website for functional/correctness defects, or extending/auditing the web-exploratory-tester agent's methodology.
---

# Web Exploratory Testing — Session-Based Methodology

Full methodology for `web-exploratory-tester`: how to hunt functional, edge-case, and consistency
defects on a live site using Session-Based Test Management, comparing against `specs/**` as ground
truth.

## Reference Modules

- `reference/01-inputs-relationships-nondestructive.md` — why this agent exists, invocation inputs,
  relationship to `web-usability-tester`/`web-design-tester`/`swe-ui-checker`, the Non-Destructive
  Constraint.
- `reference/02-session-based-methodology.md` — charter framing (Hendrickson template), testing
  tours (Whittaker taxonomy), SFDIPOT coverage, CRUSSPIC STMPL quality criteria.
- `reference/03-test-dimensions-checklist.md` — the full dimensions checklist (functional flows,
  edge cases, behavioural consistency, forms, navigation, URL/IA, responsive, accessibility,
  performance, cross-browser, safe security surface).
- `reference/04-mandatory-sweeps.md` — the three Mandatory Systematic Sweeps (shared-control ×
  surface matrix, per-control URL/state round-trip, declared-invariant conformance) and the
  self-completeness check.
- `reference/05-browser-driving-and-specs-ground-truth.md` — how to drive the browser
  (WebFetch/curl/Playwright/Lighthouse), comparing live behaviour against `specs/**`, and
  spec-gap detection.
- `reference/06-defect-anatomy-and-severity.md` — the full `EWT-###` defect anatomy and the
  severity/priority scales.
- `reference/07-output-modes-and-procedure.md` — the three output modes (`plan`/`delivery`/
  `local-temp`), the 10-step procedure summary, quality guidelines, and constraints.

## Core Principles

**Enumerate, never sample** — the three Mandatory Systematic Sweeps exist because charter-and-tour
testing reliably finds representative defects yet misses the "assert one property for every element"
class. **Cite the ground truth** — every "expected" points to a mockup, spec, contract, or
independent computation, never a guess. **Spec gaps are proposals, not verdicts** — a live behaviour
that contradicts an existing scenario is a defect for `findings.md`; only correct-but-unprotected
behaviour becomes a `spec-gaps.md` proposal.

## Related

`web-usability-tester` (the spec-blind first-time-comprehension sibling), `web-design-tester` (the
design-aware third lens of the live-site advocate triad), `plan-creating-project-plans` (backlog plan
structure), `plan-writing-gherkin-criteria` (Gherkin ACs and `spec-gaps.md` scenarios),
`docs-applying-content-quality`.

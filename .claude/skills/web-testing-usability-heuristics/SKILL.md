---
name: web-testing-usability-heuristics
description: Spec-blind heuristic usability evaluation methodology for web-usability-tester — Nielsen's 10 heuristics, cognitive walkthrough, first-click/information-scent analysis, the usability dimensions checklist, four mandatory systematic probes, URL naturalness, responsive usability, finding anatomy, and the three output modes (plan/delivery/local-temp).
when_to_use: When performing spec-blind, first-time-user usability evaluation of a live website, or extending/auditing the web-usability-tester agent's methodology.
---

# Web Usability Testing — Heuristic Evaluation Methodology

Full methodology for `web-usability-tester`: how to evaluate a live site's first-time comprehension
against established usability science, without reading specs, source, or mockups.

## Reference Modules

- `reference/01-inputs-discipline-relationships.md` — why this agent exists, invocation inputs, the
  Spec-Blind Discipline (hard rule), relationship to `web-exploratory-tester`/`web-design-tester`/
  `swe-ui-checker`, the Non-Destructive Constraint.
- `reference/02-heuristic-evaluation-and-walkthrough.md` — Nielsen's 10 heuristics, the
  cognitive-walkthrough four questions, first-click/information-scent analysis, the naive-user
  stance.
- `reference/03-usability-dimensions-checklist.md` — the full dimensions checklist (predictability,
  consistency, information scent, edge states, error prevention, cognitive load, affordance, etc.).
- `reference/04-mandatory-probes-url-responsive.md` — the four Mandatory Systematic Probes
  (conditional-control discoverability, jargon scan, cross-view redundancy, unit/currency
  consistency), URL Naturalness, Responsive Usability.
- `reference/05-browser-driving-and-spec-suggestions.md` — how to drive the browser
  (WebFetch/curl/Playwright), and how to propose `spec-suggestions.md` entries without breaking the
  spec-blind stance.
- `reference/06-finding-anatomy-and-severity.md` — the full `UWT-###` finding anatomy and the
  Nielsen 0-4 severity scale.
- `reference/07-output-modes-and-procedure.md` — the three output modes (`plan`/`delivery`/
  `local-temp`), the 11-step procedure summary, quality guidelines, and constraints.

## Core Principles

**Stay blind, always.** The moment the evaluator learns the intended behaviour, first-time
comprehension can no longer be judged — never read `specs/**`, source, or mockups to decide what is
"correct". **Cite the principle, never a vibe** — every finding names the heuristic, walkthrough
question, UX law, or WCAG criterion it violates; no principle, no finding. **Enumerate, never
sample** — the four Mandatory Systematic Probes exist because a heuristic sweep reads past exactly
these failure classes once the evaluator has already explored the page.

## Related

`web-exploratory-tester` (the spec-aware functional/correctness sibling), `web-design-tester` (the
design-aware third lens of the live-site advocate triad), `plan-creating-project-plans` (backlog plan
structure), `plan-writing-gherkin-criteria` (Gherkin ACs and `spec-suggestions.md` scenarios),
`docs-applying-content-quality`.

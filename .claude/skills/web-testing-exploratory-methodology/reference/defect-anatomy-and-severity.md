# Defect Report Anatomy and Severity/Priority Scales

Every finding in `findings.md` carries the ISTQB-aligned fields:

- **ID** — `EWT-001`, `EWT-002`, … (stable within the plan).
- **Title** — observed symptom, specific, not the suspected cause (e.g. "City filter ignored:
  selecting Jakarta still shows all cities").
- **Severity** (technical impact — set here) and **Priority** (business urgency — proposed, owner
  confirms). See scales below.
- **Area / Component** — page, flow, or component.
- **Environment** — URL, build/commit if visible, browser+version, viewport, locale, date observed.
- **Steps to Reproduce** — numbered, minimal, deterministic; include preconditions.
- **Expected Result** — per spec/design/mockup (cite the ground truth).
- **Actual Result** — what happened; quote exact error text verbatim.
- **Evidence** — screenshot path in the plan's `evidence/` subfolder
  (`./evidence/phase-N-<description>-<locale>-<breakpoint>px.png`), console excerpt, network entry,
  response header — never secrets/PII. Screenshots a finding cites are committed to `evidence/`, not
  left in `local-tmp/`, per the
  [Evidence Capture Convention](../../../../repo-governance/development/quality/evidence-capture.md).
- **Reproducibility** — Always / Intermittent (N/M) / Once.
- **Defect type** — Functional / UI / Responsive / Accessibility / Performance / Security / Content /
  Consistency.
- **Suggested fix locus** — best-guess file/area to orient the dev (clearly marked as a hypothesis).

## Severity scale (technical impact — tester sets)

| Severity | Meaning                                        | Web example                                      |
| -------- | ---------------------------------------------- | ------------------------------------------------ |
| Blocker  | Core flow completely unusable; no workaround   | Login returns 500 for all users                  |
| Critical | Core feature broken; painful workaround exists | Checkout fails for saved cards                   |
| Major    | Important feature wrong/inconsistent           | Search returns nothing for valid query on mobile |
| Minor    | UX degraded, functionality intact              | Wrong month label in date picker                 |
| Trivial  | Cosmetic; no functional/UX impact              | 1px footer-logo misalignment                     |

## Priority scale (business urgency — proposed; owner confirms)

| Priority | Meaning                                   |
| -------- | ----------------------------------------- |
| High     | Fix this release; blocks launch/SLA/brand |
| Medium   | Fix soon; next planned sprint             |
| Low      | Fix when time allows                      |

Severity ≠ priority — a trivial homepage typo before launch can be High priority; a critical crash in
a zero-user admin screen can be Low. Record both independently.

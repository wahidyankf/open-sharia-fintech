# Finding Anatomy and Severity/Priority Scales

Every finding in `findings.md` carries:

- **ID** — `DWT-001`, `DWT-002`, … (Design — Web Tester; stable within the plan).
- **Title** — the design defect, specific and observed (e.g. "Primary CTA renders #14B8A6 raw teal
  instead of the `--color-primary` token at 1280 px / en").
- **Violated ground truth or principle** — the mockup file, the token name, the `libs/web-ui`
  primitive, the external source, or the named design principle. **Mandatory** — this is what makes a
  design finding auditable rather than opinion.
- **Severity** (design impact — set here) and **Priority** (business urgency — proposed; owner
  confirms).
- **Area / Component** — page, region, or component.
- **Environment** — URL, build/commit if visible, browser+version, viewport, locale, date observed.
- **Steps to Reproduce** — numbered, minimal, deterministic; include the breakpoint/locale.
- **Expected (designed) result** — what the design ground truth specifies (cite the mockup/token/
  primitive/external source/principle).
- **Actual result** — what the rendered page shows; quote the computed value verbatim (e.g. the
  rendered hex, the px spacing).
- **Evidence** — screenshot path in the resolved destination's `evidence/` subfolder
  (`./evidence/phase-N-<description>-<locale>-<breakpoint>px.png`), a computed-style excerpt, or a
  mockup-vs-render comparison — never secrets/PII. The evidence root is local findings by default,
  host plan in `delivery` mode, or new plan only in explicitly authorized `plan` mode, per the
  [Evidence Capture Convention](../../../../repo-governance/development/quality/evidence-capture.md).
- **Reproducibility** — Always / Intermittent (N/M) / Once.
- **Defect type** — Mockup-fidelity / Token / Primitive-reuse / Hierarchy / Alignment /
  Spacing-density / Typography / Colour / Consistency / Responsive.
- **Suggested fix locus** — best-guess file/area to orient the dev (clearly a hypothesis).

## Severity scale (design impact — tester sets)

| Severity | Meaning                                                      | Web example                                             |
| -------- | ------------------------------------------------------------ | ------------------------------------------------------- |
| Blocker  | Page is unrecognisable vs the design; brand integrity broken | Entire layout ignores the mockup; wrong template ships  |
| Critical | A primary surface drifts hard from mockup or palette         | Hero uses off-brand colours and wrong type scale        |
| Major    | A clear, visible divergence on an important element          | CTA reinvents a button instead of the `libs/web-ui` one |
| Minor    | Noticeable but contained design drift                        | Card padding off the spacing scale at one breakpoint    |
| Trivial  | Cosmetic nuance; minimal design impact                       | 1px icon misalignment in the footer                     |

## Priority scale (business urgency — proposed; owner confirms)

| Priority | Meaning                                   |
| -------- | ----------------------------------------- |
| High     | Fix this release; blocks launch/SLA/brand |
| Medium   | Fix soon; next planned sprint             |
| Low      | Fix when time allows                      |

Severity ≠ priority — a trivial homepage colour drift before launch can be High priority; a critical
drift in a zero-traffic admin screen can be Low. Record both independently.

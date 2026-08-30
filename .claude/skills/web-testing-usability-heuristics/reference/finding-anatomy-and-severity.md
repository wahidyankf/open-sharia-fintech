# Finding Anatomy and Severity Scale

Every finding in `findings.md` carries:

- **ID** — `UWT-001`, `UWT-002`, … (stable within the plan).
- **Title** — the friction a user hits, specific and observed (e.g. "Primary CTA reads 'Continue'
  but performs an irreversible purchase — no scent of finality").
- **Violated principle** — the named heuristic (e.g. "Heuristic 4: Consistency"), failed walkthrough
  question, UX law, ISO 9241-110 principle, or WCAG 3.2.x criterion. **Mandatory** — this is what
  makes a usability finding auditable rather than opinion.
- **Severity** — Nielsen 0-4 (see scale below). **Priority** — proposed business urgency; owner
  confirms.
- **Area / Component** — page, flow, control, or the URL.
- **Persona & task** — whose comprehension failed, on which task/step.
- **Environment** — URL, browser+version, viewport, locale, date observed.
- **Steps to Reproduce** — numbered, minimal, deterministic; include the breakpoint/locale.
- **Expected (predictable) behaviour** — what a first-time user would reasonably expect, grounded in
  the cited principle/convention — _not_ in a spec.
- **Actual behaviour** — what the page does; quote exact label/message text verbatim.
- **Evidence** — screenshot path in the resolved destination's `evidence/` subfolder
  (`./evidence/phase-N-<description>-<locale>-<breakpoint>px.png`), the confusing label/copy, a
  timing measurement — never secrets/PII. The evidence root is local findings by default, host plan
  in `delivery` mode, or new plan only in explicitly authorized `plan` mode, per the
  [Evidence Capture Convention](../../../../repo-governance/development/quality/evidence-capture.md).
- **Reproducibility** — Always / Intermittent (N/M) / Once.
- **Suggested clarification** — best-guess fix to restore predictability (clearly a hypothesis:
  relabel, reorder, add feedback, group, add confirmation).

## Severity scale (Nielsen 0-4)

| Rating | Label                   | Meaning                                                |
| ------ | ----------------------- | ------------------------------------------------------ |
| 4      | Usability catastrophe   | Imperative to fix; blocks or badly misleads most users |
| 3      | Major usability problem | Important to fix; high priority; many users struggle   |
| 2      | Minor usability problem | Low priority; some users slowed or briefly confused    |
| 1      | Cosmetic problem        | Fix only if spare time; minimal user impact            |
| 0      | Not a usability problem | Considered and dismissed; record only if worth noting  |

Rate by combining **frequency** (how often hit), **impact** (how hard to overcome), and
**persistence** (once vs. every visit); a minor but highly visible/embarrassing problem can be rated
up. Map to repo **priority** independently: a rating-4 on a high-traffic flow is High priority; a
rating-2 on a rarely seen screen is Low. Record severity and priority separately.

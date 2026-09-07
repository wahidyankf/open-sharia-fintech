# Design-Funnel Grilling Questions and Learning-Bearing Plans

## Design-funnel grilling questions (UI-bearing plans)

For a UI-bearing plan, the specialist's envelope and the root-owned pre-write grill MUST cover the
UI-design-funnel decisions (see [ui-design-funnel.md](ui-design-funnel.md)) as structured
multiple-choice questions (each with 2-4 concrete options plus the two standing options — a
free-form blank-state type and "chat about this"):

- **Which alternatives?** Present 2-4 candidate low-fi layouts for the screen (e.g. Ranked Table /
  Card Grid / Split Layout), each option stating its trade-off in one sentence, one marked
  `(Recommended)`. The author must produce ≥2 genuinely different named alternatives.
- **What prior art?** Present 2-4 ways to ground the alternatives (e.g. delegate a
  `web-researcher` survey of comparable tools / reuse a named sibling screen pattern / blend the
  web-ui kit only), so the diverge stage is informed rather than invented.
- **Which selection, and why?** Present the finalists as options (e.g. Option A / Option B) and
  capture the winning design plus one-sentence rationale, so Select + Justify are explicit.
- **What responsive strategy?** Present 2-4 ways the selected layout reflows from **mobile** to
  **desktop** (e.g. table collapses to stacked cards / side rail moves into a top sheet / two-pane
  split becomes a single column), so the **responsive** behaviour across mobile/tablet/desktop is
  decided mobile-first rather than designed desktop-only.

See [Grilling-With-Options Convention](../../../../repo-governance/development/workflow/grilling-with-options.md)
for the authoritative multiple-choice format.

## Learning-Bearing Plans — the Syllabus Record (HARD RULE)

A plan is **learning-bearing** when its delivery checklist authors or restructures course, tutorial,
or curriculum content — the direct learning-side analogue of "UI-bearing." Plans that only cite,
link to, or lightly correct an existing corpus are exempt — exactly as with the specs/Gherkin and
UI-design-funnel bindings above.

Every learning-bearing plan MUST document its corpus through the required
`syllabus/README.md` + `syllabus/courses/` + `syllabus/paths/` folder layout, the template-derived
per-course shape, a `## Corpus Disposition` declaration in the selected technical form, and a
Custodian line in `syllabus/README.md`. In directory form, `tech-docs/README.md` maps the companion
that owns the declaration. Author these per the
[Learning-Plan `syllabus/` Folder Convention](../../../../repo-governance/conventions/structure/learning-plan-syllabus.md).

`plan-maker` requires these artefacts and emits delivery steps that produce them; `plan-checker`
flags any missing artefact at HIGH criticality (its Learning-Bearing Syllabus Completeness step,
Step 5n, sibling to the UI-design-funnel Step 5k); the gate's repair pass scaffolds the missing syllabus-record
sections.

# Rule 20: Learning-Bearing Syllabus Completeness (Step 5n — CONDITIONAL)

Enforces the
[Learning-Plan `syllabus/` Folder Convention](../../../../repo-governance/conventions/structure/learning-plan-syllabus.md)
— the learning-side sibling of the UI-design-funnel Step 5k. A plan is learning-bearing when its
delivery checklist authors or restructures course, tutorial, or curriculum content; merely citing,
linking to, or lightly correcting an existing corpus does not trigger it.

**What to validate**:

1. **Scope detection** — determine learning-bearing status from Scope, file-impact, and delivery
   steps; if not learning-bearing, skip (confirm the exemption is recorded explicitly).
2. **Required folder layout** — `syllabus/README.md`, `syllabus/courses/` (with its own `README.md`
   for a new corpus), `syllabus/paths/` (with its own `README.md` for a new corpus). Missing
   `syllabus/README.md`: **HIGH**. Missing a required subfolder README for a new corpus: **HIGH**
   (grandfathered pre-existing corpus lacking it is exempt — see the convention's Grandfathered Format
   Cohort section).
3. **Template-derived per-course shape** — every new course file carries the REQUIRED skeleton
   (`**Course ID**`, `## Why this exists`, `## Prerequisites`, `## Accuracy notes`, `**Scope note**`,
   `## Concepts`, `## In which paths`), with the capstone carve-out honored. Missing a REQUIRED
   section: **HIGH**.
4. **`## Corpus Disposition` declaration (owning plan only)** — the owning plan's chosen technical
   form carries a `## Corpus Disposition` section with exactly one of `archive-with-plan` or
   `promote-to:<path>`. In a directory form, its README maps the companion containing the section. A
   pure consumer plan never carries it. Missing or invalid: **HIGH**.
5. **Custodian line and consumer echo** — the corpus's `syllabus/README.md` carries a
   `**Custodian**: <plan-id>` line, echoed in every consumer plan's chosen technical form under its
   own `## Corpus Custody` heading as `custodied-by:<plan-id>` (distinct from item 4). Missing either:
   **HIGH**.
6. **Delivery steps produce the artefacts** — `delivery.md` carries explicit steps scaffolding the
   layout, authoring the course files, and declaring disposition/custodian — not merely assuming they
   appear. Declared artefact with no corresponding step: **HIGH**.
7. **Exemption** — plans that only read/link/lightly correct an existing corpus are EXEMPT. Verify
   legitimacy; illegitimate exemption on a genuinely learning-bearing plan: **HIGH**.

**Finding severity**: missing `syllabus/README.md`/`courses/`/`paths/` (or a new corpus's subfolder
README): **HIGH**. New course file missing a REQUIRED section: **HIGH**. Missing/invalid `## Corpus
Disposition`: **HIGH**. Missing Custodian line or `## Corpus Custody` echo: **HIGH**. Declared
artefact with no delivery step: **HIGH**. Illegitimate "not learning-bearing" exemption: **HIGH**.
Non-learning-bearing plan: not flagged (record the exemption explicitly).

# Content-Placement and File-Impact Fixes

## BRD/PRD Content-Placement Fixes

When the audit reports misplaced content per the
[Content-Placement Rules](../../../../repo-governance/conventions/structure/plans/content-placement-rules.md#content-placement-rules-brdmd-vs-prdmd),
apply (HIGH confidence — mechanical, unambiguous):

- **Business framing in `prd.md`** (sign-off language, sponsors, stakeholders, KPIs, ceremony
  language) → move to `brd.md` (typically Business Impact or Affected Roles). If sign-off/
  approval-gate language is present at all, strip it — this repo is single-maintainer with
  code-review as the only gate.
- **User stories or Gherkin in `brd.md`** → move to `prd.md` (User Stories or Acceptance Criteria).
- **Personas in `brd.md`** → move to `prd.md`.
- **Affected Roles in `prd.md`** → move to `brd.md`.
- **Fabricated numeric targets in BRD** (presented as measured, no baseline) → rewrite as one of:
  observable fact (grep/git/agent round-trip), cited measurement (inline excerpt + URL + access
  date), qualitative reasoning (drop the number), or explicitly labeled `_Judgment call:_ …`. Never
  invent a plausible-sounding number.
- **URL-only citation** → fetch and quote the specific figure/table/excerpt, include it alongside the
  URL and access date. If unable to fetch, classify MEDIUM and flag for manual authoring rather than
  a half-fix.

After moving content, update cross-references pointing at the old location and verify both files
still satisfy their per-file required-sections list.

## File-Impact Tree Repairs

Per
[Plans Organization Convention §File-Impact Analysis Format](../../../../repo-governance/conventions/structure/plans/file-impact-analysis-format.md#file-impact-analysis-format-hard-rule):
when a missing/malformed file-impact tree is flagged, reconstruct `## File-Impact Analysis` as a
root-relative fenced `text` tree before editing supporting prose. Preserve every repo-grounded target
already named, give each `[E]`/`[N]`/`[D]`/`[G]`, retain a bounded pattern only when the plan states
how its members are discovered. Non-obvious mechanics go in `### More Detail` immediately below the
tree — never a prose-bullet primary view, invented paths, or delivery checkboxes moved out of
`delivery.md`.

HIGH confidence only when existing targets are repo-grounded and mechanically mappable. If the
footprint is genuinely ambiguous, preserve the finding as MEDIUM for author clarification.

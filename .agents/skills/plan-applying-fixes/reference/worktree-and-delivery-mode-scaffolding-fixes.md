# Worktree and Delivery Mode Scaffolding Fixes

## Worktree Specification Fixes (Step 5d Findings)

**Confidence**: **HIGH** — section completely missing or inconsistent with the resolved mode. For a
worktree mode, derive `<plan-identifier>` and insert the path/provisioning template. For a main mode,
insert the primary-checkout `not applicable` template. **FALSE_POSITIVE** — a `## Worktree`
section already exists under non-standard heading text (e.g. `## Git Worktree`) — rename rather than
duplicate.

**How to fix missing `## Worktree` section**: for a current formal plan, insert it into
`delivery.md` before the first phase heading. For an existing pre-contract single-file plan,
retain or restore it in `README.md` before `## Delivery Checklist`; this compatibility repair
never authorizes a new single-file plan. Insert the mode-appropriate verbatim `## Worktree`
template from the Worktree
Specification section of `.claude/skills/plan-creating-project-plans/SKILL.md` — that section is the
single source of truth for the exact wording; do not paraphrase it.

Deriving `<plan-identifier>`: strip the date prefix. Example: folder `2026-05-15__auth-rewrite/` →
identifier `auth-rewrite`.

**How to fix wrong worktree-mode path format**: `.claude/worktrees/<name>/` → rewrite as `worktrees/<name>/`; path
missing the `worktrees/` prefix → prepend it; identifier mismatches the plan-folder → rewrite to
match.

**How to fix a machine-specific identity path**: replace an absolute, home, tool-prefix, drive, or
UNC path in a Provisioned Worktree Identity with the canonical repository-relative route
`worktrees/<plan-identifier>/`. Preserve the initial branch, creator, and UTC timestamp; move any
resolved host path to ignored runtime evidence and never retain it in `delivery.md`.

**How to fix missing worktree-mode provisioning command**: insert the canonical fenced bash block immediately
under the path declaration: ` ```bash\nclaude --worktree <plan-identifier>\n``` `.

**How to fix missing archival cleanup steps**: insert the three checkboxes verbatim from the Plan
Archival template in
[plan-archival.md](../../plan-creating-project-plans/reference/plan-archival.md) — inventory
classification, worktree removal, branch cleanup — immediately before the completion-date step of
the plan's `### Plan Archival` section. **HIGH**: the wording is fixed and the placement is
mechanical. **FALSE_POSITIVE** — the plan declares a main mode, which provisions no worktree, or it is a
pre-contract single-file plan with no `delivery.md` for the check to read. Never
weaken a merge step's `[HUMAN]` gate while editing this section.

## Delivery Mode Fixes (Step 5m Findings)

Sibling scaffold to Worktree Specification Fixes above — see
[Plans Organization Convention §Delivery Mode](../../../../repo-governance/conventions/structure/plans/delivery-mode-the-four-modes.md#delivery-mode).

**Confidence**: **HIGH** — section entirely missing on a freshly-authored plan, or a `*-to-pr` plan
is missing exact-current-head/base PR-CI steps (mechanical once the intended mode is known — a
`[HUMAN]`-tagged merge step is never itself a finding, so never in scope for this fix, nor is any
other merge-step tag value). **MEDIUM → grill first** — the declared mode value is invalid/
unrecognized, or the merge step carries a tag other than `[AI]`/`[HUMAN]`/`[AI+HUMAN]`. Do NOT guess
which mode or tag was intended — follow the Grilling Interaction Contract with the valid options
(four modes, `worktree-to-pr` marked `(Recommended)`; or the three tags) before writing a value. When
a native tool's option limit requires staging, the root uses the
[staged decision procedure](../../../../repo-governance/development/workflow/grilling-with-options/staged-native-rendering.md#staged-native-rendering),
preserving chat and the client-provided custom answer at every node. A merge step's tag is never
mechanically retagged, at any confidence level — see How to Fix a Merge-Tag Mismatch below.

### How to Fix a Missing `## Delivery Mode` Section

Insert `## Delivery Mode: worktree-to-pr` immediately after `## Worktree` (default mode, absent any
signal otherwise) in `delivery.md` before the first phase heading. An existing pre-contract
single-file plan may retain it in `README.md` before `## Delivery Checklist`; this does not
authorize that shape for new plans. If the plan's existing checklist already shows
direct-push-only steps (no PR step, no worktree at all), resolve via the Grilling Interaction
Contract rather than silently defaulting.

### How to Fix an Invalid Non-Empty Value

Never silently coerce to the default. Follow the Grilling Interaction Contract with all four modes
(`worktree-to-pr` marked `(Recommended)`), then write the resolved mode.

# Worktree and Delivery Mode Scaffolding Fixes

## Worktree Specification Fixes (Step 5d Findings)

**Confidence**: **HIGH** — section completely missing, path format wrong, or provisioning command
missing — mechanical fix: derive `<plan-identifier>` from the plan-folder name (strip the
`YYYY-MM-DD__` prefix) and insert the canonical template. **FALSE_POSITIVE** — a `## Worktree`
section already exists under non-standard heading text (e.g. `## Git Worktree`) — rename rather than
duplicate.

**How to fix missing `## Worktree` section**: multi-file plans — insert into `delivery.md` before
the first phase heading; single-file plans — insert into `README.md` before `## Delivery Checklist`.
In both cases, insert the verbatim `## Worktree` template (path declaration, optional
`claude --worktree <plan-identifier>` pre-provisioning block, Step-0-gate note) from the Worktree
Specification section of `.claude/skills/plan-creating-project-plans/SKILL.md` — that section is the
single source of truth for the exact wording; do not paraphrase it.

Deriving `<plan-identifier>`: strip the date prefix. Example: folder `2026-05-15__auth-rewrite/` →
identifier `auth-rewrite`.

**How to fix wrong path format**: `.claude/worktrees/<name>/` → rewrite as `worktrees/<name>/`; path
missing the `worktrees/` prefix → prepend it; identifier mismatches the plan-folder → rewrite to
match.

**How to fix missing provisioning command**: insert the canonical fenced bash block immediately
under the path declaration: ` ```bash\nclaude --worktree <plan-identifier>\n``` `.

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
signal otherwise) — multi-file: `delivery.md` before the first phase heading; single-file:
`README.md` before `## Delivery Checklist`. If the plan's existing checklist already shows
direct-push-only steps (no PR step, no worktree at all), resolve via the Grilling Interaction
Contract rather than silently defaulting.

### How to Fix an Invalid Non-Empty Value

Never silently coerce to the default. Follow the Grilling Interaction Contract with all four modes
(`worktree-to-pr` marked `(Recommended)`), then write the resolved mode.

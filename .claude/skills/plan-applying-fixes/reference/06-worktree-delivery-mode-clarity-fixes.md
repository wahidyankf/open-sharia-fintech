# Worktree, Delivery Mode, and Execution-Grade Clarity Fixes

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
[Plans Organization Convention §Delivery Mode](../../../../repo-governance/conventions/structure/plans/32-delivery-mode-the-four-modes.md#delivery-mode).

**Confidence**: **HIGH** — section entirely missing on a freshly-authored plan, or a `*-to-pr` plan
is missing its PR-Review Maker→Fixer Cycle steps (mechanical once the intended mode is known — a
`[HUMAN]`-tagged merge step is never itself a finding, so never in scope for this fix, nor is any
other merge-step tag value). **MEDIUM → grill first** — the declared mode value is invalid/
unrecognized, or the merge step carries a tag other than `[AI]`/`[HUMAN]`/`[AI+HUMAN]`. Do NOT guess
which mode or tag was intended — follow the Grilling Interaction Contract with the valid options
(four modes, `worktree-to-pr` marked `(Recommended)`; or the three tags) before writing a value. When
a native tool's option limit requires staging, the root uses the
[staged decision procedure](../../../../repo-governance/development/workflow/grilling-with-options/08-staged-native-rendering.md#staged-native-rendering),
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

### How to Fix a `*-to-pr` Plan Missing the PR-Review Maker→Fixer Cycle

Insert the cycle steps (strictly sequential maker→fixer, default N=3 — a hard ceiling never extended
and never exited early, each cycle CI-green-gated) immediately before the PR-merge step, sourced
verbatim in structure from the
[PR Review Quality Gate workflow](../../../../repo-governance/workflows/pr/pr-review-quality-gate.md):
one `- [ ] [AI] Invoke pr-review-synthesis-maker on $PR` / `- [ ] [AI] Invoke pr-review-fixer on $PR`
pair per cycle, the loop-exit condition (N cycles complete regardless of per-cycle finding count),
and — where the plan folder is tracked in this repo — an archival-in-PR step (`git mv` to
`plans/done/` + README updates) committed inside the same PR, before the final merge step — whatever
tag it already carries. Never retag it while scaffolding.

### How to Fix a Merge-Tag Mismatch

**This recipe is bound by the merge-step structural guard in
`01-merge-step-guard-and-confidence.md` — read that guard before applying anything here.**
Concretely:

- `*-to-pr` mode with the merge step carrying a tag other than `[AI]`/`[HUMAN]`/`[AI+HUMAN]` → do
  NOT retag it. Follow the Grilling Interaction Contract with all three valid tags and apply only the
  resolved tag. An unrecognized tag may carry human-actor semantics this agent must not silently
  strip — never assume it is safe to overwrite.
- **Never retag, delete, or otherwise remove a `[HUMAN]`- or `[AI+HUMAN]`-tagged merge step, in any
  Delivery Mode.** The tag on the merge step IS the plan's opt-in — there is no separate "explicit
  opt-in" declaration to check for. This is not limited to `*-to-pr` mode: a direct-push mode plan
  with a `[HUMAN]`-tagged merge step (or any recipe that would delete a merge step as a side effect
  of an unrelated fix) is exactly as unsafe as retagging one under `*-to-pr` — the observable
  outcome, the gate is gone, is identical either way. There is no fix action for a `[HUMAN]`- or
  `[AI+HUMAN]`-tagged merge step — leave it alone unconditionally.
- `*-to-origin-main` mode with the final push gated behind an unrequested `[HUMAN]` approval step →
  retag `[AI]` and remove the approval-gate framing (the push itself needs no sign-off under a
  direct-push mode). This is the push, not the merge, so the merge-step guard does not apply here.

## Execution-Grade Clarity Fixes (Step 5e Findings — HARD RULE)

When a delivery checkbox lacks explicit file paths, verbatim commands, or a concrete acceptance
criterion, rewrite with maximum detail.

**Confidence**: **HIGH** — the missing element can be derived from plan context (`tech-docs.md`
names the file, the project list implies the Nx command, the Gherkin criterion implies the test
command) — apply automatically. **MEDIUM** — genuinely ambiguous even on careful read — skip and
flag, invent nothing. **FALSE_POSITIVE** — the checkbox describes a non-mechanical decision (e.g.
"Decide whether to keep dual-write enabled") that legitimately has no path/command/criterion — rare;
convert to a `> Decision:` blockquote if appropriate, otherwise classify FALSE_POSITIVE.

**Rewrite recipe**: (1) file path — search `tech-docs.md` for the named subsystem, check "Files to
modify"/"Files to create", for new files give parent directory + naming pattern + sibling reference;
(2) shell command — match the project's Nx target conventions, quote verbatim in backticks; (3)
acceptance criterion — express as the observable change (passing test, typecheck exit 0, a grep
returning a specific count, a file containing a specific string).

**Rewrite examples**: see the Bad/Good Examples section of
`.claude/skills/plan-creating-project-plans/SKILL.md` for the three canonical before/after pairs
(caching, middleware, lint) — apply the same transformation shape.

After rewriting, re-read the checkbox and confirm a sonnet-tier agent could execute it without
consulting any other section. Repeat until self-contained.

**Never apply this rewrite to a merge step.** A merge step missing a verbatim command or acceptance
criterion is out of scope here and stays governed by How to Fix a Merge-Tag Mismatch above —
supplying a scripted `gh pr merge` command must never become the mechanism that converts a `[HUMAN]`
gate to `[AI]`.

# Knowledge Capture Log — Parallel-Orchestration & Shared-Machine Governance

<!-- Knowledge Capture running log — append entries during execution. -->
<!-- Triage every entry (or record the explicit "none" escape) before archival. -->

<!--
Entry shape:

## Learning: <one-line summary>

- **Context**: what was being done when this surfaced
- **Observation**: what was noticed (sanitized — see the secret/sensitivity gate)
- **Why it might generalize**: the litmus reasoning
-->

## Phase 0 baseline — old cap phrasing ("surfaces to update")

Captured 2026-07-20 in the plan worktree at `a207b66e7`, via the Phase 0 baseline command:

```bash
grep -rn "cap at 2\|3 total\|Cap at Three\|stricter cap of 2\|2 concurrent background\|capped at \*\*3 concurrent\*\*" \
  AGENTS.md CLAUDE.md repo-governance/
```

**15 hits across 8 files** (`CLAUDE.md` carries none — it inherits the model via `@AGENTS.md`):

| File                                                           | Lines                          | Hits |
| -------------------------------------------------------------- | ------------------------------ | ---: |
| `AGENTS.md`                                                    | 266, 267                       |    2 |
| `repo-governance/development/agents/subagent-orchestration.md` | 27, 79, 83, 170, 172, 194, 196 |    7 |
| `repo-governance/development/agents/README.md`                 | 38                             |    1 |
| `repo-governance/development/README.md`                        | 154                            |    1 |
| `repo-governance/development/practice/parallel-by-default.md`  | 74, 82, 86, 139                |    4 |
| `repo-governance/workflows/plan/multi-plans-execution.md`      | 118                            |    1 |

This is the "surfaces to update" set for Phase 1 and the Phase 4 Gate's repo-wide superseded-cap
proof. Note the Phase 4 Gate uses a **wider** pattern than this baseline (it adds `cap of 2`,
`cap 3 concurrent`, `2 background`, `never more`), so its expected post-change hit count is not
simply "15 → 0" against this same command — the two greps are deliberately different instruments.

## Learning: a plan's surface inventory can miss an index that describes the file being changed

- **Context**: Phase 1's closing grep sweep, after rewriting the four concurrency surfaces.
- **Observation**: Two index READMEs carried one-line descriptions of the conventions I had just
  rewritten, and both became factually wrong the instant those rewrites landed —
  `development/agents/README.md` ("≤2 concurrent background agents") and `development/README.md`
  ("default 2 simultaneous background Agent-tool spawns; … 3 total"). The plan's Phase 4 §4a checkbox
  names `development/agents/README.md` and `development/practice/README.md`, but **not**
  `development/README.md`. That third file was in no checkbox's stated scope; without an unscoped
  sweep it would have survived to the Phase 4 Gate's repo-wide proof, or past it.
- **Why it might generalize**: when a plan enumerates "surfaces to change", the enumeration is
  naturally built from files that _state_ the rule. Files that merely _summarize_ the rule — parent
  index READMEs, catalog tables, "Related Documentation" blurbs — describe it too, and go stale in
  exactly the same way. Candidate durable fix: have `plan-maker`/`plan-checker` expand any surface
  inventory entry `X` with "every index or README that links to and characterizes `X`", derived
  mechanically by grepping for inbound links, rather than relying on the author to recall them.
- **Related**: this is the same class as the existing memory note that bulk version-string replaces
  must be followed by a grep of **all** doc files, not just the ones edited.

## Learning: appending implementation notes is not the same edit as ticking the checkbox

- **Context**: Discovered at the Phase 2 Gate, 18 items into execution.
- **Observation**: The Atomic Sync Ritual has three steps — tick the checkbox, persist the notes,
  close the task. When the tick and the notes are written as **one** `Edit` whose `old_string` is the
  tail of a multi-line checkbox (the acceptance clause), it is easy to land only the notes: the
  `old_string` anchors on text _below_ the `- [ ]` marker, so the marker is never in the replaced
  span. The edit succeeds, the notes appear, the task gets closed — and disk still says `- [ ]`.
  Nothing errors. It accumulated silently across 18 items in Phases 0-2 before a gate check happened
  to `grep -n "^- \[ \]"` and exposed it.
- **Why it might generalize**: this failure is **invisible to every signal the executor watches**.
  The Edit tool reports success, the task list looks correct, and the notes are genuinely on disk. It
  is caught only by an independent count of `- [x]` versus closed tasks. Candidate durable fixes:
  (a) make the tick its own `Edit` whose `old_string` includes the literal `- [ ]` marker, so a
  mis-anchored edit _fails loudly_ instead of silently no-op'ing; (b) have the executor assert
  `count('- [x]') == count(completed tasks)` at every phase gate rather than only at plan end.
- **Repair applied**: verified all 18 carried a `**Date**` evidence block bounded by the next
  checkbox, then flipped exactly those 18 lines and diffed to confirm the change was purely
  `[ ]` → `[x]` (18 `<` / 18 `>`, no prose touched). Ticking without that evidence check would itself
  have been a corner-cut — asserting completion from memory rather than from the record.
- **Related**: the existing memory note that the PostToolUse markdown formatter rewrites files after
  every Edit is the reason `old_string` anchors drift in this repo in the first place.

## Learning: this plan structurally worsens a preexisting instruction-size warning

- **Context**: Phase 4a, after adding the same-machine assumption and two convention cross-links to
  `AGENTS.md`.
- **Observation**: `nx run rhino-cli:instruction-size:validation` exits **0** but emits
  `[WARN] AGENTS.md is 29049 bytes (over 27000-byte warn threshold)` and
  `[WARN] resolved-tree (CLAUDE.md) is 36422 bytes (over 34000-byte warn threshold)`. Measured
  against `origin/main`, `AGENTS.md` was **already 28333 bytes** — over threshold before this plan
  touched it. This phase added 716 bytes, and Phase 4 mandates further `AGENTS.md` additions (DAG
  rule, 3-5 min cadence, PR-as-merge-point, hardened merge preconditions, and the Delta 12 merge
  default rewrite).
- **Why it might generalize**: the plan and the budget are in **structural tension** — the plan's
  whole purpose is to thread new rules through the most-loaded instruction surface in the repo, while
  the budget convention's sole sanctioned remediation is progressive disclosure. Neither is wrong;
  they were authored independently and nothing forces a plan author to notice the collision. The
  budget was not surfaced as a constraint anywhere in this plan's surface inventory or acceptance
  criteria, so an executor only encounters it by running a gate the plan does not require.
- **Not fixed here, deliberately**: remediating means restructuring `AGENTS.md` into progressive
  disclosure — a substantial refactor of the canonical instruction file, well outside this plan's
  declared scope, and directly at odds with the phases still to run. Recording it rather than
  silently absorbing it (which would hide a real trend) or scope-creeping into it (which would be a
  different, unreviewed change). Candidate follow-up: a backlog plan to move `AGENTS.md` detail
  behind progressive disclosure, sequenced **after** this plan lands so the two do not conflict.
- **Mitigation applied in-plan**: keep every remaining `AGENTS.md` addition as tight as the
  acceptance criteria allow, and prefer linking to the convention over restating it inline.

## Learning: a whole convention can be the stale surface, and a grep-count sweep will not reveal it

- **Context**: Phase 4b's sweep of hardcoded `[HUMAN]`-merge references (46 pre-edit → 20 post-edit).
- **Observation**: `repo-governance/development/workflow/pr-merge-protocol.md` contributed only a
  couple of matching lines, so by hit-count it looked like a minor sweep target. It is in fact an
  entire convention built on the rule Delta 12 inverts: "AI agents and automation MUST NOT merge a
  pull request without explicit user approval", "No AI agent, automation script, or workflow may
  auto-merge", "Prior approval does not carry forward", a `### The Approval Prompt` section, and a
  `FAIL: … auto-merging` worked example. Most of that text never contains the literal `[HUMAN]`, so
  the sweep's own pattern could not see it. The plan names the file in **no** checkbox.
- **Why it matters**: the sweep's acceptance ("every surviving hit is an explicit per-plan opt-in")
  was technically satisfiable while the repo still shipped a convention asserting the exact opposite
  rule in different words. A count-based sweep measures the phrasing, not the position.
- **Why it might generalize**: a governance delta that inverts a default should search for
  **documents whose thesis is the old default**, not merely lines matching the old default's
  phrasing. Candidate durable fix: when a plan declares a delta that inverts an existing rule, have
  `plan-maker`/`plan-checker` require an explicit inventory entry for every convention whose title
  or `description:` frontmatter names that rule — those files need reading, not grepping.
- **Related**: same family as the index-staleness learning above (both are surfaces the enumeration
  missed), but a strictly harder case: an index at least _links_ to the file it describes, so an
  inbound-link sweep would catch it. A competing convention has no such mechanical trace.

## Plan-start baseline SHAs

Recorded 2026-07-20 via `git -C <repo> rev-parse origin/main` after `git fetch origin main` in each
repo. Every later "commits this plan authored" check anchors to these (`<baseline-sha>..origin/main`),
never to reflog-relative syntax such as `origin/main@{1}`.

- ose-public: a207b66e7e59bc6fafd1f650480718fcae02f7e5
- ose-primer: 1728a6e751980289753bf93934d446b998161741
- ose-infra: edbb604e49a1c84f00bd01ea547bbd126b87b29c

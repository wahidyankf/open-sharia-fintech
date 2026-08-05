# Delivery Checklist: PR Review Cycle Scout + Cycle-Number + Type-Soundness

**Delivery Mode**: `worktree-to-pr` — Phases 0-4 happen in a dedicated worktree with no PR yet (Phase
0 opens no PR per the hard rule; Phases 1-4 are one contiguous delivery unit that is not yet
independently shippable until the mirrors validate). The PR opens at the delivery boundary, at the
start of Phase 5, per [Plans Organization Convention §PRs Open at Delivery
Boundaries](../../../repo-governance/conventions/structure/plans.md#prs-open-at-delivery-boundaries-not-every-phase-hard-rule).

## Phase 0: Baseline and Worktree Setup

- [ ] [AI] Confirm `ose-public`'s local `main` is clean and up to date:
      `git status --porcelain` returns empty AND `git rev-parse HEAD` equals
      `git rev-parse origin/main` — acceptance: both hold
- [ ] [AI] Create the worktree: `git worktree add worktrees/pr-review-cycle-scout-and-typesafety -b
pr-review-cycle-scout-and-typesafety` — acceptance: `git worktree list` shows the new worktree
- [ ] [AI] In the worktree: `npm install && npm run doctor -- --fix` — acceptance: both exit 0
- [ ] [AI] Re-verify the mechanically-measured baseline from `brd.md` still holds in the worktree
      (nothing changed between plan-authoring and execution start):
      `grep -c eight repo-governance/development/quality/pr-review-disciplines.md` returns `26`;
      `grep -c eight repo-governance/workflows/pr/pr-review-quality-gate.md` returns `6`;
      `wc -c AGENTS.md` returns `28714`; `ls .claude/agents/ | grep -c pr-review` returns `10` —
      acceptance: all four match; if any differs, STOP and re-baseline `brd.md` before proceeding
      (another actor may have touched this surface since plan authoring)
- [ ] [AI] Run baseline quality gates in the worktree to confirm a known-good starting point:
      `npx nx run rhino-cli:test:quick` — acceptance: exits 0 with zero preexisting failures (if any
      preexisting failure is found, fix it per Root Cause Orientation before Phase 1 begins — do not
      carry a known-red baseline into new work)

### Phase 0 Gate

- [ ] [AI] Worktree exists, toolchain converged, baseline counts confirmed identical to `brd.md`,
      zero preexisting quality-gate failures — safe to begin Phase 1
  - **Pause Safety**: no plan content edited yet; safe to stop indefinitely; resume by re-running the
    baseline commands above

## Phase 1: `pr-review-disciplines.md` Convention Edits

- [ ] [AI] Add a ninth row to the **Eight[→Nine] Reviewer Disciplines** table (rename the section
      heading `## The Eight Reviewer Disciplines` → `## The Nine Reviewer Disciplines`): Discipline
      `Type-soundness`, Specialist agent `pr-review-types-maker`, Owns (per
      [tech-docs.md's Detailed Design](./tech-docs.md#detailed-design-of-pr-review-types-makermd)),
      NOT its job → routes to (per [DD-2](./tech-docs.md#design-decisions)) — acceptance:
      `grep -ci "type-soundness" repo-governance/development/quality/pr-review-disciplines.md`
      returns `>= 1` in the table itself (was `0` per `brd.md`'s baseline)
  - _Suggested executor: `repo-rules-maker`_
- [ ] [AI] Add grey-zone ruling **(g) Compiles vs. is sound** to the **Six[→Seven] Grey-Zone
      Rulings** section (rename heading accordingly), verbatim per
      [DD-2](./tech-docs.md#design-decisions) — acceptance:
      `grep -c "Compiles vs\." repo-governance/development/quality/pr-review-disciplines.md` returns
      `>= 1`
- [ ] [AI] Update the `## The Boundary Tie-Breaker Rule` section's opening sentence ("A ninth role,
      `pr-review-synthesis-maker` (the coordinator), does not discover findings...") to name BOTH
      non-discovery roles: scout (classification/context, does not discover findings either) and
      synthesis-maker (consolidation) — acceptance: the sentence names `pr-review-scout-maker`
      explicitly alongside `pr-review-synthesis-maker`
- [ ] [AI] In `## Risk-tier fan-out (D12)`: replace "all eight specialists plus the coordinator" with
      "all nine specialists plus the coordinator", and add one sentence noting classification is now
      performed by `pr-review-scout-maker`, not `pr-review-synthesis-maker` directly (cross-link to
      `pr-review-scout-maker.md`) — acceptance: `grep -c "pr-review-scout-maker"
repo-governance/development/quality/pr-review-disciplines.md` returns `>= 1`
- [ ] [AI] In `## Shared-context extract-once + large-diff handling (D13)`: same re-attribution to
      scout as the item above
- [ ] [AI] In `## Post-Cutover Monitoring Plan`'s **Per-discipline acceptance rate** bullet: note
      that `type-soundness` joins `performance` and `docs` as a newly-added discipline to watch for
      whether it "earns its fan-out cost" — acceptance: `grep -c "type-soundness"
repo-governance/development/quality/pr-review-disciplines.md` returns `>= 2` (table + this
      mention)
- [ ] [AI] Sweep every remaining literal `eight` occurrence in the file (26 total per baseline, minus
      the ones already touched above): for each, read the surrounding sentence and decide — becomes
      `nine` (current-count statements) or stays as historical narration (e.g. "retired the single
      `pr-review-maker` monolith... into eight discipline-scoped specialists" describing what
      happened at the ORIGINAL cutover stays historically accurate and is NOT changed) — acceptance:
      `grep -n eight repo-governance/development/quality/pr-review-disciplines.md` — manually confirm
      every remaining line is a deliberate historical-narration exception, not a missed current-count
      statement
- [ ] [AI] Add `Type-soundness` to the frontmatter `description` field's brief mention of the
      discipline count where it names the boundary/rulings it defines — acceptance: frontmatter
      `description` still accurately describes the file's content post-edit (manual read-check)

### Phase 1 Gate

- [ ] [AI] `grep -c "type-soundness" repo-governance/development/quality/pr-review-disciplines.md`
      returns `>= 2`; `grep -c "Compiles vs\."` returns `>= 1`; `grep -n eight` shows only deliberate
      historical-narration lines remaining — acceptance: all three hold
  - **Pause Safety**: only the convention doc is edited; the agent files it describes do not exist
    yet, so nothing is inconsistent if paused here; resume by continuing to Phase 2

## Phase 2: `pr-review-quality-gate.md` Workflow Edits

- [ ] [AI] Update `## Participants`: add a new bullet for `pr-review-scout-maker` (pipeline stage 0,
      owns D12/D13/dismissal-read, defined at `.claude/agents/pr-review-scout-maker.md`) BEFORE the
      "Eight discipline specialists" bullet; rename that bullet's own heading text "Eight discipline
      specialists" → "Nine discipline specialists" and add `pr-review-types-maker` to its bulleted
      list; trim the `pr-review-synthesis-maker` bullet's description to remove the
      classify/assemble/dismissal-read clauses (moved to scout's new bullet) — acceptance:
      `grep -c "pr-review-scout-maker" repo-governance/workflows/pr/pr-review-quality-gate.md`
      returns `>= 1` in this section
- [ ] [AI] Update the top-level `flowchart LR` diagram: add a `SC["pr-review-scout-maker"]` node
      (new color class, e.g. `gold`) before the `FANOUT` subgraph, with an arrow `SC --> FANOUT`;
      add `N["pr-review-types-maker"]` inside the `FANOUT` subgraph; update the subgraph label from
      "8 concurrent specialists" to "9 concurrent specialists" — acceptance: rendered diagram (or its
      source) shows 10 boxes inside/around FANOUT+SC combined (9 specialists + scout), matching
      [tech-docs.md Diagram 1](./tech-docs.md#diagram-1--component-interactions-before--after)
- [ ] [AI] Update the `## Loop Algorithm` pseudocode block to match
      [tech-docs.md's updated algorithm](./tech-docs.md#architecture-overview) — insert the
      `scout = fresh pr-review-scout-maker(...)` call and its output (`tier`, `specialists`,
      `context_brief`, `dismissals`) before the `fan_out(...)` call; remove the
      `tier = synthesis_maker.classify_risk_tier(...)` line; keep `synthesis_maker.synthesize(...)`
      unchanged in shape — acceptance: `grep -c "pr-review-scout-maker\|scout ="
repo-governance/workflows/pr/pr-review-quality-gate.md` returns `>= 1` inside the code block
- [ ] [AI] Update the second `sequenceDiagram` (below the Loop Algorithm) to add participant `SC as
pr-review-scout-maker`, with `O->>SC` as the first interaction and `SC->>SP` replacing
      `SY->>SP` for the fan-out — per
      [tech-docs.md Diagram 2](./tech-docs.md#diagram-2--updated-per-cycle-sequence)
- [ ] [AI] Add a new numbered step to `## Steps`: **"1. Per-Cycle Scout Pass (Sequential, Repeats for
      cycle = 1..N)"** — Agent: `pr-review-scout-maker` (fresh each cycle); Args: PR reference, pinned
      head SHA, `prior` state; Output: risk tier, specialist set, shared-context brief, dismissal
      state; Depends on: Step 0 (cycle 1) / previous cycle's CI-green gate (cycle > 1); Success
      criteria: tier is exactly one of trivial/lite/full and is recorded for the header;
      renumber the existing "1. Per-Cycle Fan-Out + Synthesis Pass" → **"2."**, "2. Per-Cycle Fixer
      Pass" → **"3."**, "3. Per-Cycle CI Gate" → **"4."**, "4. Done-Definition Check" → **"5."** —
      update every internal `Depends on: Step N` cross-reference to match the new numbering —
      acceptance: `grep -n "^### [0-9]\." repo-governance/workflows/pr/pr-review-quality-gate.md`
      shows steps numbered 0 through 5 with no gap or duplicate
- [ ] [AI] In the renumbered Step 2's "Success criteria" bullet, add: "the review's header records
      the **cycle number (N of {input.cycles})**" alongside the existing risk-tier/specialist-set/
      diff-slicing mentions — acceptance: `grep -c "cycle number"
repo-governance/workflows/pr/pr-review-quality-gate.md` returns `>= 1`
- [ ] [AI] Update the `## Notes` section's "All nine pipeline agents implemented and wired" bullet:
      change to "All eleven pipeline agents implemented and wired" and update its body to name
      `pr-review-scout-maker` and the nine discipline specialists (was eight) alongside
      `pr-review-synthesis-maker` and `pr-review-fixer` — acceptance:
      `grep -c "eleven pipeline agents"
repo-governance/workflows/pr/pr-review-quality-gate.md` returns `1`
- [ ] [AI] Sweep every remaining literal `eight` occurrence in the file (6 total per baseline, minus
      ones already touched): read each in context, same historical-narration-vs-current-count
      judgment as Phase 1 — acceptance: `grep -n eight
repo-governance/workflows/pr/pr-review-quality-gate.md` shows only deliberate exceptions

### Phase 2 Gate

- [ ] [AI] `grep -n "^### [0-9]\." repo-governance/workflows/pr/pr-review-quality-gate.md` shows
      steps 0-5 with no gap/duplicate; `grep -c "eleven pipeline agents"` returns `1`; `grep -c "cycle
number"` returns `>= 1`; both mermaid diagrams render without syntax errors (`md mermaid
validate` against this file) — acceptance: all hold
  - **Pause Safety**: the workflow doc now describes agents that do not exist yet on disk; this is a
    documented, intentional intermediate state (the convention/workflow docs are the design; Phase 3
    implements them) — safe to pause here, resume by continuing to Phase 3

## Phase 3: New and Edited Agent Files

- [ ] [AI] Create `.claude/agents/pr-review-scout-maker.md` following
      [tech-docs.md's Detailed Design of `pr-review-scout-maker.md`](./tech-docs.md#detailed-design-of-pr-review-scout-makermd)
      verbatim — frontmatter, `## Agent Metadata`, `## Core Responsibility`, `## Risk-Tier
Classification + Specialist-Set Selection (D12)`, `## Shared-Context Assembly, Once (D13)`,
      `## Prior-Cycle Thread-Resolution Read`, `## Trivial-Tier Handoff (DD-7)`, `## Output
Contract`, `## When to Use This Agent`, `## Tools Usage`, `## Reference Documentation` —
      acceptance: file exists; frontmatter `tools: Read, Bash, Grep, Glob`, `model: opus`,
      `color: blue`
  - _Suggested executor: `agent-maker`_
- [ ] [AI] Create `.claude/agents/pr-review-types-maker.md` following
      [tech-docs.md's Detailed Design of `pr-review-types-maker.md`](./tech-docs.md#detailed-design-of-pr-review-types-makermd)
      verbatim — frontmatter, `## Agent Metadata`, `## Core Responsibility`, `## Charter: Owns
Type-Soundness, Cross-Language` (with the four per-language bullet lists), `## NOT Its Job`,
      `## SUPPRESS Block`, `## Finding Requirements (Hard Rules)`, `## Scope Guard`, `## Untrusted-
Input Handling`, `## When to Use This Agent`, `## Tools Usage`, `## Reference Documentation` —
      acceptance: file exists; frontmatter `tools: Read, Bash, Grep, Glob, WebFetch, WebSearch`,
      `model: sonnet`, `color: blue`
  - _Suggested executor: `agent-maker`_
- [ ] [AI] Edit `.claude/agents/pr-review-synthesis-maker.md`: remove the entire `## Pre-Fan-Out
Duties (D12 / D13)` section (all three subsections: Risk-Tier Classification, Shared-Context
      Assembly, Prior-Cycle Thread-Resolution Read) — acceptance: `grep -c "Pre-Fan-Out Duties"
.claude/agents/pr-review-synthesis-maker.md` returns `0`
- [ ] [AI] Same file: add `**Cycle**: N of {total}` as the first line of the `## Consolidated Review
Header` template block, before `**Risk tier**` — acceptance: `grep -A1 "Consolidated Review
Header" .claude/agents/pr-review-synthesis-maker.md | grep -c Cycle` returns `>= 1`
- [ ] [AI] Same file: update the frontmatter `description` and the `## Agent Metadata` Model
      Selection Justification's self-count ("the ninth `pr-review-*-maker` agent") to "the eleventh
      `pr-review-*-maker` agent"; update `## Core Responsibility` and `## Cross-Cycle Behavior` prose
      to reflect that risk-tier classification, context assembly, and the dismissal read are now
      `pr-review-scout-maker`'s upstream job, not this agent's own — this agent's per-cycle work
      starts from the specialists' raw findings scout's fan-out already ran — acceptance: `grep -c
"eleventh" .claude/agents/pr-review-synthesis-maker.md` returns `>= 1`; `grep -c
"pr-review-scout-maker" .claude/agents/pr-review-synthesis-maker.md` returns `>= 1`
- [ ] [AI] Run `repo-rules-checker`'s discipline-conformance audit (per
      [pr-review-disciplines.md's Enforcement section](../../../repo-governance/development/quality/pr-review-disciplines.md#enforcement))
      against both new agent files, confirming each carries a `SUPPRESS`-equivalent scope guard and a
      routing table entry consistent with the convention doc's updated table — acceptance: 0 findings
- [ ] [AI] Verify Agent Naming Convention compliance for both new filenames:
      `ls .claude/agents/*.md | sed 's|.*/||; s|\.md$||' | grep -vE -- '-(maker|checker|fixer|dev|deployer|manager|tester|researcher)$' | grep -v '^README$'`
      — acceptance: empty output (both new names already end in `-maker`, matching the existing
      family)

### Phase 3 Gate

- [ ] [AI] Both new agent files exist with compliant frontmatter and naming; `pr-review-synthesis-
maker.md` no longer contains its old Pre-Fan-Out Duties section and now carries the Cycle
      header field; `repo-rules-checker` reports 0 findings against all three touched/new agent files
      — acceptance: all hold
  - **Pause Safety**: agent files exist on disk but `.opencode/`/`.cursor/`/`.amazonq/` mirrors are
    now stale (not yet regenerated) — this is expected mid-phase state per the multi-harness sync
    pipeline; safe to pause, resume by continuing to Phase 4 (which regenerates them in the same
    commit boundary before the PR opens)

## Phase 4: Catalog, `AGENTS.md`, and Binding Sync

- [ ] [AI] Edit `.claude/agents/README.md`: add catalog entries for `pr-review-scout-maker` and
      `pr-review-types-maker` in the PR Review Cycle family list (alongside the existing 8 discipline + synthesis-maker + fixer entries), one-line descriptions mirroring the existing entries'
      style; update the existing `pr-review-synthesis-maker` catalog line's "atop the eight
      sonnet-tier specialists" → "atop the nine sonnet-tier specialists" — acceptance: `grep -c
"pr-review-scout-maker\|pr-review-types-maker" .claude/agents/README.md` returns `>= 2`
- [ ] [AI] Edit `AGENTS.md`'s PR Review Cycle bullet: change the single word `eight` → `nine` — no
      other change, per [DD-6](./tech-docs.md#design-decisions) — acceptance: `wc -c AGENTS.md`
      returns `<= 28714` (net non-positive byte delta) AND `grep -c "nine discipline"
AGENTS.md` returns `1`
- [ ] [AI] Run `npm run generate:bindings` — acceptance: exits 0; `.opencode/agents/pr-review-scout-
maker.md` and `.opencode/agents/pr-review-types-maker.md` now exist; `.opencode/agents/pr-
review-synthesis-maker.md` reflects the trimmed source
- [ ] [AI] Run `npm run validate:sync` — acceptance: exits 0, 0 drift findings across
      `.opencode/`/`.cursor/`/`.amazonq/`
- [ ] [AI] Run `nx run rhino-cli:instruction-size:validation` — acceptance: exits 0, `AGENTS.md`
      reported within its 30,000 B hard ceiling (expected: still in the pre-existing WARN band per
      `brd.md`'s baseline, unchanged or improved by this plan's net-negative edit — NOT a new
      regression this plan introduces)

### Local Quality Gates (Before Push)

- [ ] [AI] Run `npx nx run rhino-cli:test:quick` — acceptance: exits 0
- [ ] [AI] Run `npm run lint:md:fix` — acceptance: exits 0, no unresolved violations in the
      touched/new files
- [ ] [AI] Fix ALL failures found, including any preexisting issue unrelated to this plan's own
      changes, per Root Cause Orientation — acceptance: zero failures before proceeding
- [ ] [AI] Re-run failing checks to confirm resolution
- [ ] [AI] Verify zero failures before pushing: `md links validate`, `md readme-index validate`,
      `harness duplication validate` — acceptance: all pass

### Commit Guidelines

- [ ] [AI] Commit changes thematically: one commit for the `pr-review-disciplines.md` convention
      edit (Phase 1), one for `pr-review-quality-gate.md` (Phase 2), one for the two new + one edited
      agent file (Phase 3), one for the catalog/`AGENTS.md`/binding-sync edits (Phase 4) — Conventional
      Commits format, no unrelated changes bundled
- [ ] [AI] Push the branch and open the PR against `ose-public`'s `main`:
      `git push -u origin pr-review-cycle-scout-and-typesafety` then `gh pr create` — title
      referencing this plan's slug, body linking `README.md` — acceptance: PR exists and is open

### Phase 4 Gate

- [ ] [AI] All Phase 1-4 commits pushed; PR open; local quality gates green — acceptance: holds
  - **Pause Safety**: PR is open but has not yet run the review cycle; safe to pause here, resume by
    continuing to Phase 5

## Phase 5: Dogfood the New Pipeline and Merge

- [ ] [AI] Invoke the (pre-existing, unmodified-by-this-plan) `pr-review-quality-gate` workflow
      against this plan's own PR with the default `cycles: 3` — this is the **first PR to ever run
      the new scout-first, nine-specialist, cycle-numbered pipeline**, exercising it against the very
      diff that introduces it (mirrors the original eight-discipline split's own `worktree-to-pr-
hardening` Phase 4 cutover precedent, which retired the old monolith immediately rather than
      running old-and-new in parallel)
- [ ] [AI] Confirm cycle 1's posted review carries `**Cycle**: 1 of 3` in its header, and that
      `pr-review-scout-maker` ran (visible via its classification being reflected in the header's
      Risk tier / Specialists fanned out fields) — acceptance: holds
- [ ] [AI] Confirm each subsequent cycle's header increments the cycle number correctly (`2 of 3`,
      `3 of 3`) and never repeats a prior cycle's number — acceptance: holds
- [ ] [AI] Apply `pr-review-fixer` triage each cycle per the workflow's own Step 3 (now renumbered),
      push fixes, resolve threads — acceptance: per the workflow's own Step 3 success criteria
- [ ] [AI] Confirm the CI-green gate holds after each cycle's fixer pass before the next cycle starts
      — acceptance: `gh pr checks <PR>` reports zero failing/pending checks after each cycle
- [ ] [AI] After 3 cycles complete: verify the [Done-Definition for `*-to-pr`
      Modes](../../../repo-governance/workflows/pr/pr-review-quality-gate.md#done-definition-for--to-pr-modes)
      — N cycles complete without escalation, every comment answered with its fix committed and
      pushed, all quality gates green, archival-in-PR N/A until Phase 7 (noted, not yet applicable)
- [ ] [AI] Verify the five hardened merge preconditions (a)-(e) per
      [PR Merge Protocol](../../../repo-governance/workflows/pr/pr-review-quality-gate.md#hardened-merge-preconditions)
      — 3 cycles with no escalation, 0 CRITICAL + 0 HIGH outstanding, branch up-to-date with
      `origin/main`, all gates green, no UI/API surface changed (docs+agent-prompt-only PR — record
      this exemption explicitly per the surface-conditional rule) — acceptance: all five hold
- [ ] [AI] `[AI]` merge the PR once all preconditions hold (no `[HUMAN]` gate declared for this plan)
      — acceptance: PR merged, `origin/main` advances

### Phase 5 Gate

- [ ] [AI] PR merged; local `main` fast-forwarded (or `reset --soft`-recovered) to match `origin/main`
      per [the FF-local-main-after-side-worktree-push practice](../../../repo-governance/development/workflow/worktree-and-artifact-cleanup.md);
      worktree removed — acceptance: `git -C /Users/wkf/ose-projects/ose-public rev-parse HEAD`
      equals `git -C /Users/wkf/ose-projects/ose-public rev-parse origin/main`
  - **Pause Safety**: feature work is fully merged and live; safe to pause indefinitely; resume by
    continuing to Phase 6 (Knowledge Capture) on local `main`

## Phase 6: Knowledge Capture

- [ ] [AI] Create `learnings.md` in this plan's folder (on local `main`, per plan-docs-on-main
      practice) with the mandatory H1 as its first content line, per the
      [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)
- [ ] [AI] Log every learning surfaced during Phases 0-5 as it is discovered (running log, not
      reconstructed after the fact) — candidates to watch for specifically: any surprise in how the
      dogfooded review cycle behaved with the new scout stage (e.g. scout misclassifying a tier,
      the trivial-tier handoff behaving unexpectedly), any `AGENTS.md` byte-budget surprise, any
      `repo-rules-checker` finding against the two new agent files that required a design change not
      anticipated in `tech-docs.md`
- [ ] [AI] Triage every logged learning through the routing matrix's two hard safety gates
      (secret/sensitivity, repo-relevance) and the litmus test ("would the system catch this
      automatically next time?"), routing each to a durable home or discarding with a stated reason
      — per this convention's own Iron Rule: any code-homed learning becomes a separate
      `plans/backlog/` plan, never landed inline, except a same-plan blocker required to finish this
      plan's own declared scope

### Phase 6 Gate

- [ ] [AI] `learnings.md` exists with every discovered learning triaged to a terminal state (routed
      or discarded-with-reason); zero code-homed learnings landed inline outside the Iron Rule 3
      carve-out — acceptance: holds

## Phase 7: Plan Archival

- [ ] [AI] `git mv plans/in-progress/pr-review-cycle-scout-and-typesafety
plans/done/YYYY-MM-DD__pr-review-cycle-scout-and-typesafety` (today's completion date) —
      acceptance: `git status` shows the rename
- [ ] [AI] Update `plans/in-progress/README.md`: remove the Active Plans entry added during plan
      creation
- [ ] [AI] Update `plans/done/README.md`: add a new Completed Projects entry summarizing the three
      shipped enhancements and the dogfood result
- [ ] [AI] Commit and push the archival move directly to `origin/main` from `ose-public`'s local
      checkout (archival-in-PR already landed as part of Phase 5's merged PR if the archival commit
      is bundled there instead — confirm which posture applies and do not double-archive)

### Phase 7 Gate

- [ ] [AI] Plan folder lives at `plans/done/YYYY-MM-DD__pr-review-cycle-scout-and-typesafety/`; both
      README indexes updated; local `main` matches `origin/main` — acceptance: holds; plan complete

## Related Documentation

- [README.md](./README.md), [brd.md](./brd.md), [prd.md](./prd.md), [tech-docs.md](./tech-docs.md)
- [Plans Organization Convention](../../../repo-governance/conventions/structure/plans.md)
- [PR Review Quality Gate workflow](../../../repo-governance/workflows/pr/pr-review-quality-gate.md)

# Phase Gate/Execution Marker and Anti-Hallucination Post-Execution Verification

## 1. Phase Gate and Execution Marker Post-Execution Validation (Step 5f-gates — MANDATORY)

After verifying worktree usage (Step 5e), validate that execution respected the phase gate barrier
rule and surfaced every `[HUMAN]` step. These conventions are defined at
[Plans Organization Convention §Execution Markers](../../../../repo-governance/conventions/structure/plans/17-executor-tagging-tags-and-bias.md#executor-tagging--ai-vs-human-hard-rule)
and
[§Phase Gates and Natural Pauses](../../../../repo-governance/conventions/structure/plans/20-phases-as-natural-pauses.md#phases-as-natural-pauses-with-clear-gates-hard-rule).

### What to Validate

1. **Every `### Phase N Gate` was satisfied before phase N+1 started**
   - Read `delivery.md`. For each phase, confirm its gate checklist items are ticked (or documented as
     verified) before the first step of the next phase is ticked.
   - Check git history for the order in which delivery.md was updated; gate checks should appear in
     commits before the next phase's steps.
   - Evidence missing: **HIGH** finding per phase boundary where ordering cannot be confirmed.
   - Gate items explicitly skipped or commented out without resolution: **CRITICAL** per item.

2. **`[HUMAN]` steps were surfaced — not silently auto-executed or skipped**
   - Identify every `[HUMAN]` marker in `delivery.md`.
   - Confirm in git history or implementation notes that execution paused at each `[HUMAN]` step and
     resumed only after operator confirmation.
   - A `[HUMAN]` step ticked with no implementation note (Date, Status, confirmation evidence):
     **HIGH** finding per step.
   - Evidence that an agent attempted to perform a `[HUMAN]` step autonomously: **CRITICAL** finding.

3. **Each phase reached its Pause-Safety state**
   - For each phase, locate its `> **Pause Safety**:` blockquote. Confirm the described safe-to-stop
     state is verifiable against the post-execution repo (e.g., files exist, commands exit 0).
   - Run the resume command stated in the Pause Safety note and confirm it exits cleanly.
   - Pause Safety state not reached (files missing, commands failing): **HIGH** finding per phase.

### Finding Severity

- Gate items skipped/bypassed without resolution: **CRITICAL**
- Agent auto-executed a `[HUMAN]` step: **CRITICAL**
- Phase gate ordering not confirmed (next phase started before gate was green): **HIGH**
- `[HUMAN]` step ticked without operator confirmation evidence: **HIGH**
- Pause Safety state not verifiable: **HIGH**

## 2. Anti-Hallucination Post-Execution Validation (Step 5f — MANDATORY HARD RULE)

After verifying phase gates and execution markers (Step 5f-gates), verify that every factual claim in
`delivery.md` (file paths, Nx targets, package versions, function names, agent names, test names,
behavior claims) still holds against the post-execution repo state. Hallucinated claims that survived
authoring may have been silently fabricated by the executor — this step catches them.

### What to Validate

**A. File-path claims** — for every file path mentioned in delivery.md (checkbox prose and
implementation-notes blocks): `Bash test -f <path>`. Missing AND no documented deletion/move: **HIGH**
per occurrence. If newly created, verify `git log --diff-filter=A` shows the creation in the
plan-execution timeframe.

**B. Nx-target claims** — for every Nx target invoked in delivery.md commands: read
`apps/<project>/project.json`, confirm the target appears under `targets`. Missing: **HIGH** per
occurrence.

**C. Package-version claims** — `jq` the relevant manifest (`package.json`, `go.mod`, `Cargo.toml`,
etc.). Confirm the cited version matches the post-execution lockfile. Mismatch: **MEDIUM** per
occurrence (may be legitimate version bump during execution; flag for review).

**D. Test-name claims** — `Grep` test files in the affected project. Missing: **HIGH** per occurrence
(the test was claimed but never written).

**E. Agent-name claims** — for every agent name cited (especially `_Suggested executor:_`
annotations): `Bash test -f .claude/agents/<name>.md`. Missing: **HIGH** per occurrence
(Anti-Pattern AP-7).

**F. Behavior claims** — for every claim about library or framework behavior in tech-docs.md: verify
it is backed by a `[Web-cited]` inline excerpt + URL + access date, or by a repo-doc reference.
Missing source: **MEDIUM** per occurrence.

**G. KPI claims** — for every numeric KPI in brd.md or implementation-notes: confirm the number is
either an observable check, a cited measurement, qualitative reasoning, or explicitly labeled
`_Judgment call:_`. Bare unlabeled percentage or duration: **HIGH** per occurrence (Anti-Pattern
AP-5).

**H. Cross-link integrity** — for every relative cross-link in plan files: resolve and `Bash test -f`.
Broken: **HIGH** per occurrence (Anti-Pattern AP-10).

### How to Audit

1. Read all plan files top-to-bottom.
2. For each factual claim, run the recipe in
   [Plan Anti-Hallucination Convention §Repo-Grounding Rule](../../../../repo-governance/development/quality/plan-anti-hallucination/05-repo-grounding-rule-hard.md#repo-grounding-rule-hard).
3. Compare results against the post-execution repo state.
4. File findings per severity table below.
5. For external behavior claims, delegate multi-page verification to `web-researcher` per the lower
   threshold in
   [Plan Anti-Hallucination Convention §Web-Research Delegation](../../../../repo-governance/development/quality/plan-anti-hallucination/13-refuse-on-uncertainty-rule-and-web-research-delegation.md#web-research-delegation-lower-threshold-for-plans).

### Finding Severity

- Missing file path / missing Nx target / missing test / missing agent / unlabeled KPI / broken
  cross-link: **HIGH** per occurrence
- Version mismatch / behavior claim without source / suggested-executor mismatch: **MEDIUM** per
  occurrence
- Stale `[Unverified]` labels remaining post-execution: **MEDIUM** per occurrence (plan-execution
  should have resolved them)

### Why Post-Execution Anti-Hallucination Matters

`plan-checker` runs anti-hallucination at authoring time. `plan-execution-checker` runs it again at
archival time because: the executor may have written fabricated implementation-notes when work was
incomplete; file renames or refactors during execution may have stranded path references; Nx target
additions/removals during execution may have stranded command references; library upgrades during
execution may have outdated cited versions. Both gates exist for a reason; do not skip Step 5f under
time pressure.

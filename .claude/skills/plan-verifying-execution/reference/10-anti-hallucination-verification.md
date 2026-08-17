# Anti-Hallucination Post-Execution Validation (Step 5f)

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
annotations): `find .claude/agents -name '<name>.md'` returns a match (agent definitions live in
nested role subfolders, not flat under `.claude/agents/`). Missing: **HIGH** per occurrence
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
incomplete; file renames/refactors may have stranded path references; Nx target additions/removals
may have stranded command references; library upgrades may have outdated cited versions. Both gates
exist for a reason; do not skip Step 5f under time pressure.

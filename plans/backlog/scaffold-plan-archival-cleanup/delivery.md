# Delivery — Scaffold Plan-Archival Cleanup Steps

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.

Read [tech-docs.md](./tech-docs.md) before starting. It fixes the placement decision (extend Rule 10
rather than mint Rule 22) and the both-directions verification requirement.

## Delivery Mode: worktree-to-pr

Mandatory in `ose-public` — `main` is branch-protected including for admins. Used identically in
`ose-private`; its narrow infrastructure-as-code direct-push exception does not apply to a Skill
change.

## Worktree

Worktree path: `worktrees/scaffold-plan-archival-cleanup/` — to be provisioned at execution start
per [Worktree Specification](../../../.claude/skills/plan-creating-project-plans/reference/worktree-specification.md).
Not yet provisioned; this is a backlog-stage plan.

Provision from the repository root when work starts:

```bash
claude --worktree scaffold-plan-archival-cleanup
```

### Provisioned Worktree Identity

- Declared repository-relative route: `worktrees/scaffold-plan-archival-cleanup/`
- Initial branch: `worktree/scaffold-plan-archival-cleanup`
- Created by: `<executor identity or session — recorded at Phase 0>`
- Created at: `<ISO-8601 UTC timestamp — recorded at Phase 0>`

The plan must not record an absolute, home, tool-prefix, drive, UNC, or other host-specific path.
Resolve its declared route only at runtime against the selected repository root; retain any resolved
path only in ignored runtime evidence after reconciliation with `git worktree list --porcelain`.

### Delivery Branch Inventory

| Branch                                    | Mode      | Lifecycle state | Proof                                    |
| ----------------------------------------- | --------- | --------------- | ---------------------------------------- |
| `worktree/scaffold-plan-archival-cleanup` | `pending` | `not created`   | `<git worktree add timestamp — Phase 0>` |

Append every plan-created delivery branch before use. A `*-to-pr` entry records its merged PR and
40-character reviewed-head SHA. Before removal, classify every entry as delivered, unused, or
retained/escalated; active or unrecorded branches block cleanup.

### Cross-Repository Parity Identity

- Objective slug: `scaffold-plan-archival-cleanup`
- Common worktree basename: `scaffold-plan-archival-cleanup`

| Repository    | Worktree route                              | Branch                                    | Provisioning status |
| ------------- | ------------------------------------------- | ----------------------------------------- | ------------------- |
| `ose-public`  | `worktrees/scaffold-plan-archival-cleanup/` | `worktree/scaffold-plan-archival-cleanup` | pending — Phase 0   |
| `ose-private` | `worktrees/scaffold-plan-archival-cleanup/` | `worktree/scaffold-plan-archival-cleanup` | pending — Phase 3   |

Re-verify `ose-private`'s bare-versus-normal topology at Phase 3 rather than assuming it; this
repository pair has flipped layouts before.

## Delivery Units

| Unit | Phases | Repository    | Boundary rationale                                                                                 |
| ---- | ------ | ------------- | -------------------------------------------------------------------------------------------------- |
| —    | 0      | both          | Baseline only. Opens no PR.                                                                        |
| DU-1 | 1–2    | `ose-public`  | Template, check, recipe, and mirrors ship together; a check without its recipe is half a delivery. |
| DU-2 | 3      | `ose-private` | Same semantics restated into the sibling repository's own shard set.                               |
| —    | 4      | both          | Knowledge Capture. No tracked change, no PR.                                                       |

## Standing Instructions

### Fix-All-Issues Instruction

> **Important**: Fix ALL failures found during quality gates, not just those caused by your
> changes. This follows the root cause orientation principle — proactively fix preexisting
> errors encountered during work.

### Local Quality Gates (Before Push)

- [ ] [AI] Run affected typecheck: `rtk nx affected -t typecheck` — exits 0
- [ ] [AI] Run affected linting: `rtk nx affected -t lint` — exits 0
- [ ] [AI] Run affected quick tests: `rtk nx affected -t test:quick` — exits 0
- [ ] [AI] Run affected spec coverage: `rtk nx affected -t specs:coverage` — exits 0
- [ ] [AI] Fix ALL failures found — including preexisting issues not caused by these changes
- [ ] [AI] Verify all checks pass before pushing

> A `test:quick` failure that disappears on a warm-cache re-run without `--skip-nx-cache` is a known
> flake under parallel hook load, not a regression. Re-run once before investigating.

### Post-Push Verification

- [ ] [AI] Push to the PR branch, redirecting output:
      `rtk git push origin HEAD > local-tmp/push-output.txt 2>&1` — a Husky `EAGAIN` stdout panic
      (`os error 35`) on large output is not a gate failure; read the gate's own final PASS/FAIL
      summary line. Never use `--no-verify`
- [ ] [AI] Monitor with `rtk gh pr checks <pr-number>` — poll every 2 minutes, never `gh run watch`
- [ ] [AI] Verify all CI checks pass; investigate any failure at its root cause
- [ ] [AI] Do NOT proceed to the next phase until CI is green

### Commit Guidelines

- [ ] [AI] Do not stage or commit until the user explicitly authorizes the named change set. The
      standing authorization granted to `update-tmp-folders` is plan-scoped and does NOT carry here
- [ ] [AI] Once authorized, use the fewest build-valid, independently reviewable and revertible
      commits, one coherent purpose each
- [ ] [AI] Follow Conventional Commits: `<type>(<scope>): <description>`
- [ ] [AI] Stage explicit paths — never `git add -A`; sibling trees carry unrelated uncommitted work
- [ ] [AI] Commit with `rtk git commit --only -m "<message>" -- <paths>`; the pre-commit hook
      otherwise sweeps unstaged files in. New files still need an explicit `git add` first, and
      `-m` must precede the `--` separator
- [ ] [AI] Keep regenerated mirrors in the same commit as their source

## Phase 0: Environment Setup and Baseline

**Input**: A clean `ose-public` checkout on `main`.
**Outcome**: The worktree exists, the toolchain is converged, and the baseline is recorded.
**Proof**: Baseline commands exit 0; the worktree identity is filled in above.

- [ ] [AI] Provision the worktree from the `ose-public` repository root:
      `claude --worktree scaffold-plan-archival-cleanup`. Record the resulting creator and
      ISO-8601 UTC timestamp into [Provisioned Worktree Identity](#provisioned-worktree-identity),
      and update the [Delivery Branch Inventory](#delivery-branch-inventory) row to `provisioned` /
      `active`
- [ ] [AI] Verify git identity is not the stray `Test <test@test.com>` override:
      `rtk git config user.email` — if it prints `test@test.com`, STOP and surface it; this is a
      `[HUMAN]`-only fix
- [ ] [AI] Sync: `rtk git fetch origin && rtk git merge --ff-only origin/main` — exits 0
- [ ] [AI] At the worktree root: `rtk npm install && rtk npm run doctor -- --fix` — both exit 0.
      A fresh worktree has no `node_modules`, so this is required, not a formality
- [ ] [AI] Create `plans/backlog/scaffold-plan-archival-cleanup/learnings.md` if absent, with the
      mandatory `# Learnings: scaffold-plan-archival-cleanup` H1 — markdownlint MD041 fails a
      comments-only scaffold
- [ ] [AI] Record the baseline: `rtk nx affected -t build,test:quick,lint` — exits 0. Fix any
      preexisting failure before proceeding
- [ ] [AI] Enumerate the plans the new check will run against, writing the list to
      `local-tmp/scaffold-plan-archival-cleanup/live-plans.txt`:
      `/bin/ls -1 plans/in-progress plans/backlog`. Use `/bin/ls`, not the shell's `eza` alias —
      its hyperlink escapes corrupt piped output

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [ ] [AI] `rtk git status --short` shows only this plan's folder
- [ ] [AI] `rtk nx affected -t build,test:quick,lint` exits 0
- [ ] [AI] `local-tmp/scaffold-plan-archival-cleanup/live-plans.txt` exists and is non-empty
- [ ] [AI] The worktree identity and branch inventory above carry real recorded values, not
      placeholders

> **Pause Safety**: nothing changed but the plan folder. Safe to stop. To resume:
> `rtk nx affected -t build,test:quick,lint` from the worktree root.

## Phase 1: Rules Propagation — Scaffold and Check (`ose-public`)

**Input**: The three Skill reference surfaces named in
[tech-docs.md §File-Impact Analysis](./tech-docs.md#file-impact-analysis).
**Outcome**: The template scaffolds cleanup, `plan-checker` checks for it, `plan-fixer` repairs it.
**Proof**: AC-1, AC-2, AC-3, AC-4; every `RP-` step ticked.

This changes a rules surface, so it is a
[rules-propagation](../../../repo-governance/workflows/rules/rules-propagation.md) run at
`mode: strict`, not an ordinary Skill edit.

- [ ] [AI] **RP-0 Intake** — normalize into falsifiable statements in
      `local-tmp/rules-propagation/statements-public.md`. There are two: (1) a plan's archival
      section must contain a worktree-removal step and a branch-cleanup step routing to the
      canonical convention; (2) `plan-checker` must flag an archival section missing either. Record
      each statement's violating observation
- [ ] [AI] **RP-1 Working tree** — `isolation: current`; the run writes in the Phase 0 worktree.
      Record the parity slug, basename, and branch from
      [Cross-Repository Parity Identity](#cross-repository-parity-identity); the Phase 3 run reuses
      them verbatim
- [ ] [AI] **RP-2 Classification** — assign subject and layer; confirm vendor neutrality. Both
      statements are Agents-layer (Skill reference modules), not Conventions — the convention
      already exists and is unchanged
- [ ] [AI] **RP-3 Conflict scan** — search for an existing rule that already states either
      statement. Expect a **partial semantic no-op**: the obligation exists in
      `plan-execution/finalization-worktree-cleanup-and-pr-archival.md` and
      `plans/worktree-specification-continued.md`. Record those as the binding sources the new
      scaffolding routes to, NOT as supersessions — nothing is being replaced. Halt and surface if
      any higher-layer rule contradicts the scaffolding
- [ ] [AI] **RP-4 Placement** — confirm or overturn
      [tech-docs.md §D-1](./tech-docs.md#d-1-extend-the-existing-worktree-rule-do-not-mint-rule-22).
      Read `.claude/skills/plan-validating-quality/reference/rule10-worktree-specification-validation.md`
      and run `wc -w` on it. If it has headroom, the check goes there and no new shard is created.
      Record the decision and the word count in `local-tmp/rules-propagation/placement-public.md`
- [ ] [AI] **RP-5 Eviction** — if Rule 10's shard has no headroom, evict rather than raise the
      threshold. Only if eviction is genuinely impossible does a new numbered shard become correct —
      and a new shard then needs a link in its folder `README.md` **and** in the parent index, or the
      readme-completeness gate fails the push as an orphan
- [ ] [AI] Edit `.claude/skills/plan-creating-project-plans/reference/plan-archival.md`: add three
      checkboxes to the template, placed before the `rtk date +%F` completion-date step — (1)
      classify every `Delivery Branch Inventory` entry as delivered, unused, or retained/escalated;
      (2) remove each worktree the plan provisioned, non-force, from the repository root; (3)
      complete the canonical
      [branch cleanup](../../../repo-governance/development/workflow/worktree-and-artifact-cleanup/branch-cleanup.md)
      for every plan-created branch, then run `git worktree prune`. Link out for the procedure; do
      not restate its proof gates, per
      [tech-docs.md §D-2](./tech-docs.md#d-2-the-template-links-out-it-does-not-restate-the-procedure)
- [ ] [AI] Add the "not applicable for a main mode" carve-out to the template's own wording, so a
      `main-to-pr` or `main-to-origin-main` plan is not told to remove a worktree it never created
- [ ] [AI] Edit the placement target chosen at RP-4 to add the presence check: an archival section
      that declares a worktree mode and lacks either step is a finding. State the check's severity
      and its non-firing conditions explicitly
- [ ] [AI] Verify the check in BOTH directions before going further, per
      [tech-docs.md §D-3](./tech-docs.md#d-3-verify-the-check-in-both-directions-before-landing):
      construct one archival section missing the branch-cleanup step and confirm the check fires;
      construct one carrying both steps and confirm it does not; construct one declaring
      `Worktree: not applicable` and confirm it does not. Record all three outcomes in
      `local-tmp/scaffold-plan-archival-cleanup/check-verification.md`
- [ ] [AI] Locate the fixer recipe module:
      `rtk grep -rln "rule10\|worktree" .claude/skills/plan-applying-fixes/reference/` — record the
      chosen file. Add a recipe that inserts the missing steps in the template's wording, and that
      never weakens a merge step's human gate
- [ ] [AI] **RP-6 Write and tidy** — confirm no two modules now state the archival cleanup
      obligation in conflicting words, and reindex any folder `README.md` whose child annotations
      changed. Check `wc -w` on each edited `README.md` before committing; governance index files
      sit near a 500-word FAIL ceiling
- [ ] [AI] **RP-7 Enforcement disposition** — record one of `covered` / `gated` /
      `unenforced-by-decision` per statement in
      `local-tmp/rules-propagation/dispositions-public.md`, none silent. Expected: statement (1) is
      `covered` by the new `plan-checker` check — name it and cite the both-directions evidence from
      `check-verification.md`, because a check verified in one direction is half a check; statement
      (2) is the check itself
- [ ] [AI] Run the new check against every plan in `live-plans.txt`. Fix each resulting finding in
      this delivery, or record it with its reason in
      `local-tmp/scaffold-plan-archival-cleanup/live-plan-findings.md`. Leaving an unaddressed
      finding on unrelated work is not shipping (AC-4)

### Phase 1 Gate

> All checks below must pass before starting Phase 2.

- [ ] [AI] `rtk grep -c "branch" .claude/skills/plan-creating-project-plans/reference/plan-archival.md`
      prints a non-zero count
- [ ] [AI] `check-verification.md` records all three cases — fires, does not fire, main-mode does not
      fire
- [ ] [AI] `dispositions-public.md` records a disposition for both statements, none silent
- [ ] [AI] Every plan in `live-plans.txt` is either clean under the new check or recorded in
      `live-plan-findings.md` with its reason
- [ ] [AI] `wc -w` on every edited `README.md` is under the 500-word FAIL ceiling

> **Pause Safety**: the sources state the new scaffolding; mirrors are still stale, so `validate:sync`
> will fail until Phase 2. Nothing executes differently — these are documents. Safe to stop. To
> resume: `rtk npm run validate:sync` and expect it to fail until Phase 2 regenerates.

## Phase 2: Regenerate, Verify, and Land DU-1

**Input**: Phase 1 complete.
**Outcome**: Mirrors match their sources and the change is on `ose-public` `main`.
**Proof**: PR merged with green exact-head/base CI.

- [ ] [AI] **RP-8.1 Regenerate** — `rtk npm run generate:bindings` — exits 0. Never hand-edit a
      mirror under `.agents/skills/`
- [ ] [AI] Verify mirrors: `rtk npm run validate:sync` — exits 0
- [ ] [AI] Verify the full binding surface: `rtk npm run harness:bindings-validation` — exits 0
- [ ] [AI] **RP-8.2 Deterministic gates** — run each of these via
      `apps/rhino-cli/scripts/rhino-bin.sh`, redirecting output to a file and asserting the process
      exit code rather than the absence of a failure token: `md links validate`,
      `md heading-hierarchy validate`, `md frontmatter validate`, `md naming validate`,
      `convention emoji validate`, `repo-config validate`. Never read an exit code through a pipe
- [ ] [AI] Establish the preexisting-failure baseline before calling any failure unrelated:
      `md links validate` reports several hundred broken links repository-wide, almost all under
      `plans/done/`. Demonstrate this run's paths are absent from the failure set
- [ ] [AI] **RP-8.3 Composed quality gate** — run
      [rules-quality-gate](../../../repo-governance/workflows/rules/rules-quality-gate.md) at
      `mode: strict`. Fix findings attributable to this run; report those that predate it. Route
      failures per the workflow's table — budget to RP-5, contradiction to RP-3, duplication to
      RP-6, invalid gate declaration to RP-7
- [ ] [AI] **RP-8.4 Reconcile the ledger** — the file-touch ledger and `rtk git status --short` name
      the same paths. A path in the status but not the ledger is an unintended edit, most often a
      neighbour swept in by the formatting hook; investigate before delivery
- [ ] [AI] Run every check in [Local Quality Gates (Before Push)](#local-quality-gates-before-push)
- [ ] [AI] Ask the user to authorize this change set; do not stage or commit until they do
- [ ] [AI] Commit per [Commit Guidelines](#commit-guidelines). Suggested:
      `docs(plans): scaffold worktree and branch cleanup into plan archival`
- [ ] [AI] Push and open a draft PR against `main`. The body states the new-code cost/benefit (this
      unit adds no code) and links this plan. Keep it free of bare `#NNN` references — a
      `#`-prefixed number in a body parses as a footer and trips the message gate
- [ ] [AI] **RP-9 PR content** — state, per statement: the statement, its destination, its
      enforcement disposition, and the fact that nothing was superseded (the obligation already
      existed; only its scaffolding is new)
- [ ] [AI] **RP-9 Sibling obligation** — record `sibling-obligation: ose-private` in the PR body and
      as a durable note, with the parity slug, basename, and branch from RP-1. Phase 3 discharges it
- [ ] [AI] Run every check in [Post-Push Verification](#post-push-verification)
- [ ] [AI] Confirm the `Quality gate` from `.github/workflows/pr-quality-gate.yml` is green for the
      PR's exact current head and base, plus one authenticated clean current-head `pr-leak-review`
- [ ] [AI] Mark ready for review and merge — `[AI]` merges once those preconditions hold. Record the
      PR number and 40-character reviewed-head SHA in the
      [Delivery Branch Inventory](#delivery-branch-inventory)
- [ ] [AI] Fast-forward local `main` in the primary checkout:
      `rtk git -C <primary-checkout-root> fetch origin && rtk git -C <primary-checkout-root> merge --ff-only origin/main`
      — a side-worktree push advances `origin/main` but not local `main`, and the divergence is
      otherwise silent. Never `reset --hard`

### Phase 2 Gate

> All checks below must pass before starting Phase 3.

- [ ] [AI] `rtk npm run validate:sync` and `rtk npm run harness:bindings-validation` both exit 0
- [ ] [AI] Every RP-8.2 gate exited 0, verified by exit code and not by scanning output text
- [ ] [AI] `rtk gh pr view <pr-number> --json state` reports `MERGED` with all checks green
- [ ] [AI] Local `main` in the primary checkout matches `origin/main`

> **Pause Safety**: `ose-public` scaffolds and checks the cleanup steps; `ose-private` does not yet,
> so the two repositories differ. Nothing is broken in either. Safe to stop. To resume:
> `rtk gh pr list --head worktree/scaffold-plan-archival-cleanup` to confirm nothing is open.

## Phase 3: Rules Propagation — `ose-private` (DU-2)

**Input**: `ose-public` `main` carrying DU-1, and the sibling obligation recorded at RP-9.
**Outcome**: `ose-private` scaffolds and checks the same steps.
**Proof**: AC-5; every `RP-` step ticked against `ose-private` specifically.

A **second, independent** run — one run touches one repository. Nothing here is satisfied by Phase 1
having happened. `mode: strict`.

- [ ] [AI] Re-verify topology before touching it: `rtk git -C <ose-private-root> worktree list` and
      `rtk git -C <ose-private-root> rev-parse --is-bare-repository`. If bare, use
      `-c core.bare=false --work-tree=` for git operations
- [ ] [AI] Provision the sibling worktree:
      `rtk git -C <ose-private-root> worktree add worktrees/scaffold-plan-archival-cleanup -b worktree/scaffold-plan-archival-cleanup origin/main`
      — a git-mechanical `[AI]` step. Update the parity table's provisioning status and timestamp
- [ ] [AI] At that worktree root: `rtk npm install && rtk npm run doctor -- --fix` — both exit 0
- [ ] [AI] **RP-0 to RP-2** — restate the same two statements against `ose-private`'s own wording in
      `local-tmp/rules-propagation/statements-private.md`; confirm the working tree and branch match
      the recorded parity identity with `rtk git rev-parse --abbrev-ref HEAD`; classify subject and
      layer. Do NOT copy `statements-public.md` across repositories — restate
- [ ] [AI] **RP-3 to RP-5** — run the conflict scan against `ose-private`'s own rule corpus, confirm
      the placement target in ITS Skill reference tree (shard filenames differ between the two
      repositories), and apply the eviction protocol if that target has no word-budget headroom
- [ ] [AI] Apply the same three template steps, the same presence check, and the same fixer recipe to
      `ose-private`'s own modules
- [ ] [AI] Verify the check in both directions in `ose-private` too — fires, does not fire, main-mode
      does not fire — recording to `local-tmp/scaffold-plan-archival-cleanup/check-verification-private.md`.
      `ose-public`'s evidence proves nothing here
- [ ] [AI] Run the check against every plan in `ose-private`'s `plans/in-progress/` and
      `plans/backlog/`; fix or record each finding
- [ ] [AI] **RP-6 to RP-7** — tidy and reindex, then record a disposition for both statements in
      `local-tmp/rules-propagation/dispositions-private.md`, none silent
- [ ] [AI] **RP-8** — regenerate mirrors, run the deterministic gates asserting exit codes, run
      `rules-quality-gate` at `mode: strict`, and reconcile the ledger against
      `rtk git status --short`. Establish `ose-private`'s OWN preexisting-failure baseline
- [ ] [AI] Run every check in [Local Quality Gates (Before Push)](#local-quality-gates-before-push)
      from the `ose-private` worktree root
- [ ] [AI] Ask the user to authorize this change set, then commit, push, open, verify, and merge the
      DU-2 PR following the same steps as Phase 2
- [ ] [AI] **RP-9** — the PR body states each statement's destination and disposition, and records
      `sibling-obligation: none — discharged`, naming `ose-public`'s counterpart PR. With both
      repositories landed the parity objective is closed; state it rather than leaving silence
- [ ] [AI] Fast-forward `ose-private`'s local `main` after the merge

### Phase 3 Gate

> All checks below must pass before starting Phase 4.

- [ ] [AI] The DU-2 PR is merged with green CI
- [ ] [AI] Both repositories' plan-archival templates scaffold the same three steps
- [ ] [AI] `check-verification-private.md` records all three cases
- [ ] [AI] Both runs reached `final-status: landed`; neither is `partial` or `halted`
- [ ] [AI] `ose-private` local `main` matches its `origin/main`

> **Pause Safety**: both repositories scaffold and check the cleanup steps. Only knowledge routing
> remains. Safe to stop. To resume: compare the two templates' cleanup steps.

## Phase 4: Knowledge Capture

- [ ] [AI] Apply the litmus test to every `learnings.md` entry — keep only entries where a durable
      surface would catch this automatically next time; discard the rest with a one-line reason
- [ ] [AI] Apply the **secret/sensitivity gate** — sanitize to `<placeholder>` tokens or discard
- [ ] [AI] Apply the **repo-relevance gate** — infra-private content stays in `ose-private` only;
      never cross-route private content into a public repo
- [ ] [AI] Route each surviving entry to exactly one durable home, landing a small non-code edit
      inline. Create or update a `plans/ideas/<slug>.md` two-pager only when the user has literally
      authorized that plan artifact; otherwise report the follow-up and record
      `Reported without plan authorization` with handoff evidence
- [ ] [AI] **Code-routing rule**: a learning whose home is `apps/`, `libs/`, or tests is NEVER landed
      inline in this plan's commits. File a separate `plans/ideas/` two-pager only with literal
      authorization; never create a `plans/backlog/` folder directly. The sole carve-out is a
      failure blocking THIS plan's own scope, fixed inline as ordinary Root Cause Orientation work
- [ ] [AI] Report the follow-up recorded in
      [tech-docs.md §Follow-Ups Recorded, Not Delivered](./tech-docs.md#follow-ups-recorded-not-delivered)
      — whether `plan-execution-checker` should verify cleanup actually happened — as
      `Reported without plan authorization` unless the user literally authorizes an idea artifact
- [ ] [AI] Record the terminal state of every entry directly in `learnings.md`
- [ ] [AI] If execution surfaced no generalizable learning, record the explicit escape
      `No generalizable learnings — <one-line reason>`

### Phase 4 Gate

> All checks below must pass before starting Plan Archival.

- [ ] [AI] Every `learnings.md` entry has a terminal state, or the explicit "none" escape is present
- [ ] [AI] No code-homed learning landed inline

> **Pause Safety**: all learnings are routed, filed, reported, or discarded. Safe to stop. To
> resume: re-check `learnings.md` for any entry without a terminal-state marker.

### Plan Archival

- [ ] Perform the **preliminary** plan-execution end-to-end delivery completeness audit: trace
      approved scope and every canonical PRD acceptance criterion through delivery units, as-built
      artifacts, automated proof, and Knowledge Capture. Reopen execution at the earliest affected
      packet for every missing or unsupported non-delivery row. Checked boxes alone are not proof
- [ ] Verify ALL delivery checklist items are ticked
- [ ] Verify ALL quality gates pass (local + CI)
- [ ] Verify manual assertions pass — this plan has no UI or API surface, so its manual assertions
      are the both-directions check verifications, whose evidence is the recorded output in
      `local-tmp/scaffold-plan-archival-cleanup/`; no `evidence/` subfolder is created
- [ ] Verify ALL supported locales were exercised in UI verification — not applicable; no
      user-facing surface
- [ ] Verify every rule-15 EWT/UWT/DWT defect finding is fixed — not applicable; no web surface
- [ ] Verify every rule-16 AET defect finding is fixed — not applicable; no API surface
- [ ] Register the workflow-owned terminal audit task and its required post-delivery proof fields;
      do not mark that gate complete before merge confirmation
- [ ] [AI] Classify every [Delivery Branch Inventory](#delivery-branch-inventory) entry in both
      repositories as `delivered`, `unused`, or `retained/escalated`. An active or unrecorded branch
      blocks cleanup — this inventory, not the file ledger, controls branch cleanup
- [ ] [AI] Remove both worktrees, non-force, from each repository root — never from inside the
      worktree being removed:
      `rtk git -C <repo-root> worktree remove worktrees/scaffold-plan-archival-cleanup`
- [ ] [AI] Complete the canonical
      [branch cleanup](../../../repo-governance/development/workflow/worktree-and-artifact-cleanup/branch-cleanup.md)
      for every plan-created branch in both repositories. These PRs squash-merge, so expect
      `git branch -d` to decline — a squash merge leaves the branch's own commits off `main`. Only
      then apply the proof-gated terminal path (`MERGED`, `headRefOid` equal to the local tip, merge
      commit contained in `origin/main`, and `HEAD_REF_DELETED_EVENT` with `delete_branch_on_merge`
      enabled) and use `git branch -D`. Any one proof missing means retain and escalate
- [ ] [AI] Never delete `main` or an environment branch. `ose-public` has `prod-*` / `stag-*`;
      `ose-private` currently has none. Confirm per repository with `rtk git branch -a`
- [ ] [AI] Run `rtk git worktree prune` in both repositories. Never `gc` or object-store `prune`
      during cleanup — another process may be writing on this shared machine
- [ ] [AI] Verify the terminal state: `rtk git branch -a` lists no
      `worktree/scaffold-plan-archival-cleanup` ref, local or remote, in either repository
- [ ] After every pre-archival gate passes, run `rtk date +%F`; record the output as
      `<completion-date>`. Do not hardcode or predict this value while authoring the plan
- [ ] Move the plan via
      `rtk git mv plans/backlog/scaffold-plan-archival-cleanup/ plans/done/<completion-date>__scaffold-plan-archival-cleanup/`
- [ ] Update `plans/backlog/README.md` — remove the plan entry
- [ ] Update `plans/done/README.md` — add the plan entry using the same resolved completion date
- [ ] Update any other READMEs that reference this plan
- [ ] Commit: `chore(plans): move scaffold-plan-archival-cleanup to done`

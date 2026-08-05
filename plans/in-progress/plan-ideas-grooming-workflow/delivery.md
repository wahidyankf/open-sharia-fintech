# Delivery Checklist: `plan-ideas-grooming` Workflow

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
>
> **Phase Gate** — every phase ends with a `### Phase N Gate` (must-pass verification) plus a
> `> **Pause Safety**:` note (the safe-to-stop state and the single command to resume). A phase is
> not complete until its gate is green; do not start phase N+1 while any gate check fails.

## Worktree

**No worktree is used for this plan.** Per the user's explicit Delivery Mode override (see
`## Delivery Mode` below), all work happens directly on each of the four repos' already-checked-out
primary `main` branch — `git rev-parse --is-bare-repository` confirms all four repos currently have
a normal (non-bare) working tree checked out at their own root `[Repo-grounded]` (re-verified
2026-08-05; re-check at delivery time since topology is documented to change over time):

- `ose-public`: `/Users/wkf/ose-projects/ose-public/` (this plan's own home repo)
- `ose-primer`: `/Users/wkf/ose-projects/ose-primer/`
- `ose-private`: `/Users/wkf/ose-projects/ose-private/`
- `beaver-nest`: `/Users/wkf/ose-projects/beaver-nest/`

This satisfies the Plans Organization Convention's mandatory Worktree Specification by explicit
N/A-with-reason: `main-to-origin-main` Delivery Mode has no worktree to declare, since there is no
side branch — every phase edits, commits, and pushes directly on `main` in the target repo's
existing checkout. See
[Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans.md#worktree-specification)
and [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md).

## Delivery Mode: main-to-origin-main

All four repos use `main-to-origin-main` — an explicit user override of the repo-wide
`worktree-to-pr` default, applying to this plan's `repo-governance/` changes even though they are
outside the plan-docs-only carve-out. Each repo's changes are edited directly on that repo's local
`main`, committed, and pushed straight to that repo's `origin/main`. **No PR opens, in any repo, at
any phase of this plan's own delivery** — no draft PR, no PR-Review Maker→Fixer Cycle, no PR merge.

**GitHub Actions CI monitoring is omitted entirely from this plan's delivery (deliberate deviation
from `plan-execution.md`'s generic per-push default, by explicit user instruction 2026-08-05)**:
local pre-commit and pre-push hooks (format, lint, markdown/link/naming/frontmatter validators,
`test:quick`, spec coverage) already gate every commit and push in full — see each phase's "Local
Quality Gates" and "Commit Guidelines" sections. The user judged this local coverage sufficient and
GitHub Actions polling — after every phase, or even once at the end — an unnecessary use of time
for a `plans/**`/`repo-governance/**`-only governance change. No phase, and no gate in this plan,
checks `gh run` / GitHub Actions status at any point.

## Parallelization Model

- **N = 3** (default), matching the three independent sibling-repo propagation phases.
- Phase 0 (setup) and Phase 1 (author in `ose-public`) are strictly serial — Phase 1 produces the
  finalized content every propagation phase copies/adapts, so no propagation may start before
  Phase 1's changes have landed on `ose-public`'s `origin/main`.
- Phases 2, 3, and 4 (propagate to `ose-primer`, `ose-private`, `beaver-nest` respectively) are
  mutually independent: no shared files, no shared repo, no ordering constraint between them. They
  fan out to fill all 3 background slots — each phase operates in its own already-separate git
  repository, so no worktree isolation is needed for the independence to hold.
- Phase 5 (Knowledge Capture) and Phase 6 (Plan Archival) depend on all of Phases 2-4 completing
  (their pushes landed on each repo's `origin/main`), and run only in `ose-public` (this plan's
  home repo).
- No worktree cleanup step exists in any phase — no worktree was ever provisioned (see `## Worktree`
  above).

### Delivery Boundaries

| Phase(s) | Delivery unit                                                          | Repo checkout              | Integration point                                                   |
| -------- | ---------------------------------------------------------------------- | -------------------------- | ------------------------------------------------------------------- |
| 0        | — (setup and baseline, `ose-public` only)                              | —                          | none                                                                |
| 1        | Author `grooming` token + workflow doc + catalog entry in `ose-public` | `ose-public` local `main`  | direct push to `ose-public:origin/main`                             |
| 2        | Propagate to `ose-primer`                                              | `ose-primer` local `main`  | direct push to `ose-primer:origin/main`                             |
| 3        | Propagate to `ose-private`                                             | `ose-private` local `main` | direct push to `ose-private:origin/main`                            |
| 4        | Propagate to `beaver-nest`                                             | `beaver-nest` local `main` | direct push to `beaver-nest:origin/main`                            |
| 5-6      | Knowledge Capture + Archival (`ose-public` only)                       | `ose-public` local `main`  | direct push to `ose-public:origin/main` (Phase 6's archival commit) |

Every change-producing phase (1-4) is its own delivery unit and pushes directly to its own repo's
`origin/main` — there is no PR boundary to declare under this Delivery Mode. Phases 5-6 produce no
new reviewable governance change; Phase 6's archival commit (moving this plan's own folder to
`plans/done/`) is the only remaining push, in `ose-public` only.

## Phase 0: Environment Setup and Baseline

> _Executor: repo-setup-manager_
>
> **No PR for this phase, and no PR under any phase of this plan.** Phase 0 is local setup and
> baseline only in `ose-public`: it pushes no branch other than confirming `main` is already in
> sync, and opens nothing.

- [x] [AI] Install dependencies in `ose-public`'s checkout: `npm install` — acceptance: exits 0,
      `node_modules/` synchronized
  - **Date**: 2026-08-05. **Status**: Done. **Files Changed**: none. **Notes**: `npm install`
    exited 0, `node_modules/` synchronized (1596 packages, up to date). Executed via
    `repo-setup-manager`.
- [x] [AI] Converge the full polyglot toolchain: `npm run doctor -- --fix` — acceptance: exits 0
      with no unresolved drift
  - **Date**: 2026-08-05. **Status**: Done. **Files Changed**: none. **Notes**: `npm run doctor -- --fix`
    exits 0, 16/16 tools OK, 0 warning, 0 missing. One session-scoped `npm` version-mismatch
    warning was environment-only (Volta shim recursion guard in the agent harness's own
    launch env), not a repo defect — resolved within the executor's Bash session
    (`env -u _VOLTA_TOOL_RECURSION`), no repo file touched.
- [x] [AI] Create `plans/in-progress/plan-ideas-grooming-workflow/learnings.md` with the mandatory
      scaffold (`# Learnings: plan-ideas-grooming-workflow` H1 followed by the running-log comment
      lines) — acceptance: file exists, first content line is the H1
  - **Date**: 2026-08-05. **Status**: Done. **Files Changed**:
    `plans/in-progress/plan-ideas-grooming-workflow/learnings.md` (new). **Notes**: File created
    with the H1 as its first content line, followed by the running-log HTML comment scaffold.
- [x] [AI] Run existing markdown quality gates to establish baseline:
      `npx nx run rhino-cli:test:quick` — acceptance: baseline pass/fail count recorded; any
      preexisting failure documented
  - **Date**: 2026-08-05. **Status**: Done. **Files Changed**: none. **Notes**: Baseline clean —
    1302 unit tests passed / 0 failed / 1 ignored (run twice, including once cold with
    `--skip-nx-cache`), 13 passed in the secondary test group, typecheck/lint green,
    specs:structure-validation 0 findings across 6 spec domains, specs:behavior:coverage
    67 specs / 424 scenarios / 1740 steps all covered. No preexisting failures found.
- [x] [AI] Resolve all preexisting failures before proceeding — acceptance: no preexisting failure
      remains unresolved
  - **Date**: 2026-08-05. **Status**: Done (vacuous). **Files Changed**: none. **Notes**: Baseline
    run found zero preexisting failures — nothing to resolve.
- [x] [AI] Confirm all four repos have a normal (non-bare) working tree and are on a clean, synced
      `main`: for each of `/Users/wkf/ose-projects/ose-public`, `/Users/wkf/ose-projects/ose-primer`,
      `/Users/wkf/ose-projects/ose-private`, `/Users/wkf/ose-projects/beaver-nest`, run
      `git -C <path> rev-parse --is-bare-repository` (expect `false`),
      `git -C <path> branch --show-current` (expect `main`), and
      `git -C <path> status --porcelain` (expect empty) — acceptance: all three checks pass for
      all four repos, or any dirty/non-`main`/bare state is explicitly surfaced to the user before
      Phase 1 begins
  - **Date**: 2026-08-05. **Status**: Done (with surfaced exception). **Files Changed**: none.
    **Notes**: All four repos confirmed non-bare, on `main`. `ose-primer`, `ose-private`,
    `beaver-nest` are clean (`git status --porcelain` empty) and `0` commits ahead of their own
    `origin/main`. `ose-public` is dirty by this plan's own Phase 0 work-in-progress: this plan's
    own `delivery.md`/`learnings.md` edits (in-flight, expected), plus a `package-lock.json` diff
    (174 stale `"extraneous": true` workspace entries pruned) produced by Phase 0's own
    `npm install` step under the correctly-pinned npm 11.11.0 — a legitimate lockfile-hygiene
    byproduct of routine dependency installation, not foreign work. Surfaced here explicitly per
    the acceptance clause; will land as a separate "preexisting fix" commit alongside Phase 1's
    push (Iron Rule 3 / Iron Rule 7), not committed during Phase 0 itself (Phase 0 pushes nothing).

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [x] [AI] `npm install` exited 0 and `npm run doctor -- --fix` reports no unresolved drift
  - **Date**: 2026-08-05. **Status**: Done. **Notes**: verified above.
- [x] [AI] `learnings.md` exists with the mandatory H1 as its first content line
  - **Date**: 2026-08-05. **Status**: Done. **Notes**: verified above.
- [x] [AI] All four repos are confirmed non-bare, on `main`, and clean (or their state was
      explicitly surfaced and accepted by the user) — falsifiable both ways:
      `git -C <path> status --porcelain` returns empty for a clean tree, non-empty for a dirty one;
      re-run after any surfaced dirty state is resolved
  - **Date**: 2026-08-05. **Status**: Done. **Notes**: `ose-primer`/`ose-private`/`beaver-nest`
    clean; `ose-public` dirty by this plan's own in-flight/Phase-0-byproduct changes only —
    surfaced above, falsifiable both ways (empty before this plan touched anything, non-empty now).
- [x] [AI] Each repo's local `main` is not ahead of its own `origin/main` yet (no plan work has
      landed) — `git -C <path> rev-list --count origin/main..main` returns `0` for all four repos
  - **Date**: 2026-08-05. **Status**: Done. **Notes**: all four repos return `0` (verified above);
    `ose-public`'s dirty working-tree changes are not yet committed, so this holds.

> **Pause Safety**: only the local toolchain was verified, the baseline recorded, and all four
> repos' topology/cleanliness confirmed — no feature work exists yet, nothing is pushed anywhere.
> Safe to stop indefinitely. To resume: re-run the baseline command and the four-repo checks.

## Phase 1: Author the `grooming` Token and Workflow Doc in `ose-public`

- [x] [AI] Edit `ose-public/repo-governance/conventions/structure/workflow-naming.md`: in the Type
      Vocabulary table (currently 4 rows: `quality-gate`, `execution`, `setup`, `planning`), add a
      fifth row `grooming` with the semantics text: "Recurring sweep/reorganization workflow over
      already-existing documentation or artifact state (the Scrum 'backlog grooming' analogy);
      does not converge to zero findings (unlike `quality-gate`), does not produce a new plan as
      terminal deliverable (unlike `planning`), and is not one-time provisioning (unlike `setup`)
      — it re-sweeps and re-organizes existing docs on a stated cadence or trigger" and example
      workflow `plan-ideas-grooming` — acceptance: table has 5 rows,
      `grep -c "| \`grooming\`" workflow-naming.md`returns`1`
  - _Suggested executor: `repo-rules-maker`_
  - **Date**: 2026-08-05. **Status**: Done. **Files Changed**:
    `repo-governance/conventions/structure/workflow-naming.md`. **Notes**: `grep -c` confirms `1`.
    Executed by `repo-rules-maker`.
- [x] [AI] Edit the same file: update the enforcement audit command's regex from
      `-(quality-gate|execution|setup|planning)$` to `-(quality-gate|execution|setup|planning|grooming)$`
      in both the `## Enforcement` section's fenced code block and any other occurrence — acceptance:
      `grep -c 'quality-gate|execution|setup|planning|grooming' workflow-naming.md` returns ≥ `1`
      and no stale 4-token regex remains (`grep -c 'setup|planning)\$' workflow-naming.md` returns `0`)
  - **Date**: 2026-08-05. **Status**: Done. **Files Changed**: same file. **Notes**: both the
    fenced-code-block occurrence and an additional prose occurrence under "Why This Rule Exists"
    updated; `0` stale 4-token regexes remain.
- [x] [AI] Edit the same file's `## Examples` section: add a `**grooming**` bullet listing
      `plan-ideas-grooming` (scope `plan`, type `grooming`) alongside the existing
      `quality-gate`/`execution`/`planning`/`setup` bullets — acceptance:
      `grep -c "plan-ideas-grooming" workflow-naming.md` returns ≥ `1`
  - **Date**: 2026-08-05. **Status**: Done. **Files Changed**: same file.
- [x] [AI] Create new file `ose-public/repo-governance/workflows/plan/plan-ideas-grooming.md`
      following the frontmatter and section shape specified in `tech-docs.md`'s "Detailed Design of
      `plan-ideas-grooming.md`" section verbatim: YAML frontmatter (`name`, `title`, `goal`,
      `termination`, `inputs: repos, dry-run, delivery-mode`,
      `outputs: grooming-log-entries, final-status`), then `# plan-ideas-grooming Workflow`,
      `## Purpose`, `## When to use`, `## Execution Mode` (Direct Orchestration, matching the
      pattern in `plan-execution.md`), `## Steps` (the 10 steps from `tech-docs.md`, written out in
      full prose with the exact urgency/importance rubrics from `prd.md`'s Gherkin scenarios, the
      relocation safety model from DD-4/DD-5, the rename mechanism folded into Step 9 per DD-7, and
      the recurrence trigger from Step 10), `## Related Workflows`, `## Related Documentation` —
      acceptance: file exists, `rhino-cli repo-governance workflows naming validate` (or the
      documented `find | grep` audit) reports the file compliant
  - _Suggested executor: `repo-rules-maker`_
  - **Date**: 2026-08-05. **Status**: Done. **Files Changed**:
    `repo-governance/workflows/plan/plan-ideas-grooming.md` (new). **Notes**: file created per
    tech-docs.md's Detailed Design section. `naming validate` initially rejected it because
    `apps/rhino-cli/src/commands/workflows_validate_naming.rs`'s `WORKFLOW_TYPES` const hardcoded
    the old 4-token list (a code-level enforcement point the doc-only edits above didn't reach) —
    fixed as a discovered same-plan blocker (task #185, TDD RED/GREEN via `swe-rust-dev`); validator
    now reports 0 violations. See item below.
- [x] [AI] Verify the new file contains no absolute local filesystem path (DD-4): run
      `grep -c "/Users/" ose-public/repo-governance/workflows/plan/plan-ideas-grooming.md` —
      acceptance: returns `0`
  - **Date**: 2026-08-05. **Status**: Done. **Notes**: `grep -c` returns `0`, confirmed.
- [x] [AI] Edit `ose-public/repo-governance/workflows/README.md`: add a new row to the "Available
      Workflows" table for `plan-ideas-grooming` (Purpose: sweep and reorganize `plans/ideas/`
      across repos; Agents: none — direct orchestration, mechanical file operations; Complexity:
      Medium) — acceptance: `grep -c "plan-ideas-grooming" workflows/README.md` returns ≥ `1`
      after this edit
  - **Date**: 2026-08-05. **Status**: Done. **Files Changed**: `repo-governance/workflows/README.md`.
- [x] [AI] Edit the same file's `## Type Vocabulary` table (the README's own copy, separate from
      `workflow-naming.md`'s): add the `grooming` row with matching semantics text — acceptance:
      both tables (in `workflow-naming.md` and `workflows/README.md`) list `grooming` with
      consistent wording
  - **Date**: 2026-08-05. **Status**: Done. **Files Changed**: same file.
- [x] [AI] Edit the same file's `### Documentation Workflows` bullet under `## Workflow Families`
      (the `- **plan**: Project planning documents — ...` line): append a clause noting
      `plan-ideas-grooming` as the idea-corpus grooming workflow — acceptance:
      `grep -c "plan-ideas-grooming" workflows/README.md` returns ≥ `2` (catalog row + family
      bullet)
  - **Date**: 2026-08-05. **Status**: Done. **Notes**: `grep -c` returns `2` (catalog row + family
    bullet), confirmed.
- [x] [AI] **[Discovered blocker, not an original checklist item]** Fix
      `apps/rhino-cli/src/commands/workflows_validate_naming.rs`'s hardcoded `WORKFLOW_TYPES` const
      to include `grooming` — required for the item above's acceptance criterion to hold.
  - **Date**: 2026-08-05. **Status**: Done. **Files Changed**:
    `apps/rhino-cli/src/commands/workflows_validate_naming.rs`,
    `apps/rhino-cli/src/application/naming/mod.rs` (added tests). **Notes**: TDD RED/GREEN via
    `swe-rust-dev` — RED: `workflows_validate_naming_accepts_grooming_suffix` failed pre-fix;
    GREEN: passes post-fix (6/6 in that test file, 58/58 in `naming::`). Final
    `cargo run --release -- repo-governance workflows naming validate` reports 0 violations.
    `npx nx run rhino-cli:test:quick --skip-nx-cache` re-run clean afterward (specs:behavior:coverage
    still 67 specs / 424 scenarios / 1740 steps, all covered — no new Gherkin scenario required for
    this data-only enum extension).

### Local Quality Gates (Before Push)

- [x] Run `npx nx run rhino-cli:test:quick` (covers markdown lint, link validation, mermaid
      validation, heading-hierarchy validation, and `rhino-cli repo-governance workflows naming
validate` per `AGENTS.md` §Markdown Quality) — exits 0
  - **Date**: 2026-08-05. **Status**: Done. **Notes**: 1302 unit tests passed, 0 failed (run twice,
    once cold with `--skip-nx-cache`); specs:structure-validation 0 findings; specs:behavior:coverage
    67 specs/424 scenarios/1740 steps all covered.
- [x] Run `npm run lint:md:fix` — exits 0, no unresolved violations in the three touched/new files
  - **Date**: 2026-08-05. **Status**: Done. **Notes**: `markdownlint-cli2 --fix "**/*.md"` — 3923
    files linted, 0 errors.
- [x] Fix ALL failures found — including preexisting issues not caused by this plan's changes
  - **Date**: 2026-08-05. **Status**: Done. **Notes**: two real (non-sweeper) discovered blockers
    found and fixed inline, both required to satisfy this phase's own delivery acceptance criteria
    (Iron Rule 3 current-plan-blocker carve-out, not deferred learnings): (1) `rhino-cli`'s
    `WORKFLOW_TYPES` const (task #185, see item 4 above); (2) `repo-governance/workflows/plan/README.md`
    orphan-file finding from `md readme-index validate` (task #186) — added a Workflows-list bullet
    for `plan-ideas-grooming.md`.
- [x] Re-run failing checks to confirm resolution
  - **Date**: 2026-08-05. **Status**: Done. **Notes**: `md readme-index validate` →
    `README INDEX AUDIT PASSED: no orphan or ghost references found`.
- [x] Verify zero failures before pushing
  - **Date**: 2026-08-05. **Status**: Done. **Notes**: also ran (scoped correctly per the actual
    pre-push hook, excluding `plans/done`/content dirs): `md links validate` → all links valid;
    `harness duplication validate` → 0 clusters; `repo-governance vendor validate` → passed;
    `convention license validate` → passed.

> **Important**: Fix ALL failures found during quality gates, not just those caused by your
> changes. This follows the root cause orientation principle — proactively fix preexisting errors
> encountered during work. Do not defer or skip existing issues. Commit preexisting fixes
> separately with appropriate conventional commit messages.

### Commit Guidelines

- [x] Commit changes thematically — group related changes into logically cohesive commits
- [x] Follow Conventional Commits format: `<type>(<scope>): <description>`
- [x] Split different domains/concerns into separate commits (e.g., the convention amendment as
      one commit, the new workflow file as another, the catalog update as a third)
- [x] Preexisting fixes get their own commits, separate from plan work
- [x] Do NOT bundle unrelated changes into a single commit
  - **Date**: 2026-08-05. **Status**: Done. **Files Changed**: none (verification of prior commits).
    **Notes**: 6 commits landed on local `main`, each single-concern: `466510bd5` (package-lock.json
    preexisting drift), `d070c6d3e` (workflow-naming.md grooming token), `6fd559bdd` (new
    plan-ideas-grooming.md), `5bfaebdd7` (catalog entries in both README.md files),
    `46a2b5ac1` (rhino-cli WORKFLOW_TYPES code fix), `3d0c1e65d` (Scope Boundary hardening — added
    mid-phase per explicit user instruction that the workflow must never write to
    `plans/backlog/`/`plans/in-progress/`, confined strictly to `plans/ideas/**`).
- [ ] [AI] Commit and push to `origin main` from `ose-public`'s local checkout (direct push, no PR
      — per this plan's `main-to-origin-main` Delivery Mode)

### Phase 1 Gate

> All checks below must pass before starting Phases 2-4. GitHub Actions CI is not checked anywhere
> in this plan (see Delivery Mode note) — local pre-commit/pre-push hooks are the sole gate.

- [ ] [AI] `git -C /Users/wkf/ose-projects/ose-public log --oneline -1 origin/main -- repo-governance/workflows/plan/plan-ideas-grooming.md`
      returns a commit (the file exists on `origin/main`) — falsifiable both ways: returns empty
      before the push, non-empty after
- [ ] [AI] `rhino-cli repo-governance workflows naming validate` run against `ose-public`'s
      `origin/main` reports the new file compliant
- [ ] [AI] `grep -c "/Users/" repo-governance/workflows/plan/plan-ideas-grooming.md` (against
      `origin/main`'s copy) returns `0`

> **Pause Safety**: `ose-public`'s convention amendment and new workflow document are pushed
> directly to `main`; local pre-push hooks passed. Safe to stop indefinitely — Phases 2-4 read this
> finalized content whenever they resume. To resume: verify the Phase 1 Gate checks still pass,
> then move to the next sibling repo.

## Phase 2: Propagate to `ose-primer`

- [ ] [AI] Sync `ose-primer`'s local `main` with its own `origin/main` before editing: from
      `/Users/wkf/ose-projects/ose-primer`, run `git checkout main && git pull --ff-only origin main`
      — acceptance: `git status --porcelain` returns empty, `git rev-list --count origin/main..main`
      returns `0`
- [ ] [AI] Read `ose-primer/repo-governance/conventions/structure/workflow-naming.md` in full
      (confirmed to differ from `ose-public`'s copy by 58 lines pre-existing) and locate its own
      Type Vocabulary table's last row — acceptance: insertion point identified without assuming
      `ose-public`'s line numbers apply
- [ ] [AI] Edit `ose-primer/repo-governance/conventions/structure/workflow-naming.md`: apply the
      same conceptual amendment as Phase 1 (add the `grooming` row with matching semantics text,
      update the enforcement regex, update the Examples section) to this repo's own file, leaving
      every other pre-existing difference from `ose-public`'s copy untouched — acceptance:
      `grep -c "| \`grooming\`" workflow-naming.md`returns`1`; a diff against this file's
      pre-edit version touches only the three amendment locations
- [ ] [AI] Copy `ose-public`'s pushed `repo-governance/workflows/plan/plan-ideas-grooming.md`
      byte-identical into `ose-primer/repo-governance/workflows/plan/plan-ideas-grooming.md` —
      acceptance: `diff /Users/wkf/ose-projects/ose-public/repo-governance/workflows/plan/plan-ideas-grooming.md /Users/wkf/ose-projects/ose-primer/repo-governance/workflows/plan/plan-ideas-grooming.md`
      returns no output
- [ ] [AI] Read `ose-primer/repo-governance/workflows/README.md` in full and locate its own
      Available Workflows table's insertion point and Type Vocabulary table's insertion point —
      acceptance: insertion points identified against this repo's own structure
- [ ] [AI] Edit `ose-primer/repo-governance/workflows/README.md`: apply the same conceptual catalog
      additions as Phase 1 (Available Workflows row, Type Vocabulary row, Plan family bullet) —
      acceptance: `grep -c "plan-ideas-grooming" workflows/README.md` returns ≥ `2`

### Local Quality Gates (Before Push)

- [ ] Run this repo's own markdown/naming quality gate equivalent (`npx nx run rhino-cli:test:quick`
      if `ose-primer` carries its own `rhino-cli` fork, else the repo's documented markdown-lint
      target) — exits 0
- [ ] Fix ALL failures found — including preexisting issues not caused by this plan's changes
- [ ] Verify zero failures before pushing

### Commit Guidelines

- [ ] Commit changes thematically (convention amendment, new file, catalog update as separate
      commits) — Conventional Commits format

- [ ] [AI] Commit and push to `origin main` from `ose-primer`'s local checkout (direct push, no PR)

### Phase 2 Gate

> All checks below must pass before this delivery unit is considered done. Phase 2 does not block
> Phases 3-4 (they are independent) but does block Phase 5. GitHub Actions CI is not checked
> anywhere in this plan — local pre-commit/pre-push hooks are the sole gate.

- [ ] [AI] `diff` between `ose-public`'s and `ose-primer`'s `origin/main` copies of
      `plan-ideas-grooming.md` returns no output
- [ ] [AI] `ose-primer`'s own naming-validate equivalent reports the file compliant on `origin/main`

> **Pause Safety**: `ose-primer`'s propagation is pushed directly to its own `main`; local pre-push
> hooks passed. Safe to stop indefinitely — independent of Phases 3-4's progress. To resume: verify
> this gate, then continue to whichever of Phases 3-4 has not yet run.

## Phase 3: Propagate to `ose-private`

- [ ] [AI] Sync `ose-private`'s local `main` with its own `origin/main` before editing: from
      `/Users/wkf/ose-projects/ose-private`, run `git checkout main && git pull --ff-only origin main`
      — acceptance: `git status --porcelain` returns empty, `git rev-list --count origin/main..main`
      returns `0`
- [ ] [AI] Read `ose-private/repo-governance/conventions/structure/workflow-naming.md` in full
      (confirmed to differ from `ose-public`'s copy by 68 lines pre-existing) and locate its own
      Type Vocabulary table's last row — acceptance: insertion point identified against this
      repo's own structure
- [ ] [AI] Edit `ose-private/repo-governance/conventions/structure/workflow-naming.md`: apply the
      same conceptual amendment as Phase 1 to this repo's own file — acceptance:
      `grep -c "| \`grooming\`" workflow-naming.md`returns`1`
- [ ] [AI] Copy `ose-public`'s pushed `plan-ideas-grooming.md` byte-identical into
      `ose-private/repo-governance/workflows/plan/plan-ideas-grooming.md` — acceptance:
      `diff /Users/wkf/ose-projects/ose-public/repo-governance/workflows/plan/plan-ideas-grooming.md /Users/wkf/ose-projects/ose-private/repo-governance/workflows/plan/plan-ideas-grooming.md`
      returns no output
- [ ] [AI] Read `ose-private/repo-governance/workflows/README.md` in full and locate its own
      insertion points — acceptance: identified against this repo's own structure
- [ ] [AI] Edit `ose-private/repo-governance/workflows/README.md`: apply the same conceptual
      catalog additions as Phase 1 — acceptance: `grep -c "plan-ideas-grooming" workflows/README.md`
      returns ≥ `2`

### Local Quality Gates (Before Push)

- [ ] Run this repo's own markdown/naming quality gate equivalent — exits 0
- [ ] Fix ALL failures found — including preexisting issues not caused by this plan's changes
- [ ] Verify zero failures before pushing

### Commit Guidelines

- [ ] Commit changes thematically — Conventional Commits format

- [ ] [AI] Commit and push to `origin main` from `ose-private`'s local checkout (direct push, no
      PR)

### Phase 3 Gate

> GitHub Actions CI is not checked anywhere in this plan — local pre-commit/pre-push hooks are the
> sole gate.

- [ ] [AI] `diff` between `ose-public`'s and `ose-private`'s `origin/main` copies of
      `plan-ideas-grooming.md` returns no output
- [ ] [AI] `ose-private`'s own naming-validate equivalent reports the file compliant on
      `origin/main`
- [ ] [AI] No secret, credential, or infra-state value was introduced by this propagation —
      `grep -riE "(api[_-]?key|password|secret|token)\s*[:=]" ose-private/repo-governance/workflows/plan/plan-ideas-grooming.md`
      returns no match (this is a pure governance-doc propagation; `ose-private`'s stricter secrecy
      posture applies to everything it receives)

> **Pause Safety**: `ose-private`'s propagation is pushed directly to its own `main`; local
> pre-push hooks passed. Safe to stop indefinitely — independent of Phases 2 and 4's progress. To
> resume: verify this gate, then continue to whichever of Phases 2/4 has not yet run.

## Phase 4: Propagate to `beaver-nest`

- [ ] [AI] Sync `beaver-nest`'s local `main` with its own `origin/main` before editing: from
      `/Users/wkf/ose-projects/beaver-nest`, run `git checkout main && git pull --ff-only origin main`
      — acceptance: `git status --porcelain` returns empty, `git rev-list --count origin/main..main`
      returns `0`
- [ ] [AI] Read `beaver-nest/repo-governance/conventions/structure/workflow-naming.md` in full
      (confirmed to differ from `ose-public`'s copy by only 12 lines pre-existing — the smallest
      drift of the three siblings) and locate its own Type Vocabulary table's last row —
      acceptance: insertion point identified against this repo's own structure
- [ ] [AI] Edit `beaver-nest/repo-governance/conventions/structure/workflow-naming.md`: apply the
      same conceptual amendment as Phase 1 to this repo's own file — acceptance:
      `grep -c "| \`grooming\`" workflow-naming.md`returns`1`
- [ ] [AI] Copy `ose-public`'s pushed `plan-ideas-grooming.md` byte-identical into
      `beaver-nest/repo-governance/workflows/plan/plan-ideas-grooming.md` — acceptance:
      `diff /Users/wkf/ose-projects/ose-public/repo-governance/workflows/plan/plan-ideas-grooming.md /Users/wkf/ose-projects/beaver-nest/repo-governance/workflows/plan/plan-ideas-grooming.md`
      returns no output
- [ ] [AI] Read `beaver-nest/repo-governance/workflows/README.md` in full and locate its own
      insertion points — acceptance: identified against this repo's own structure
- [ ] [AI] Edit `beaver-nest/repo-governance/workflows/README.md`: apply the same conceptual
      catalog additions as Phase 1 — acceptance: `grep -c "plan-ideas-grooming" workflows/README.md`
      returns ≥ `2`

### Local Quality Gates (Before Push)

- [ ] Run this repo's own markdown/naming quality gate equivalent (note: `beaver-nest` carries a
      **fork** of `rhino-cli`, per `AGENTS.md` §Related Repositories — confirm which naming-validate
      binary this repo actually runs before invoking it) — exits 0
- [ ] Fix ALL failures found — including preexisting issues not caused by this plan's changes
- [ ] Verify zero failures before pushing

### Commit Guidelines

- [ ] Commit changes thematically — Conventional Commits format

- [ ] [AI] Commit and push to `origin main` from `beaver-nest`'s local checkout (direct push, no
      PR)

### Phase 4 Gate

> GitHub Actions CI is not checked anywhere in this plan — local pre-commit/pre-push hooks are the
> sole gate.

- [ ] [AI] `diff` between `ose-public`'s and `beaver-nest`'s `origin/main` copies of
      `plan-ideas-grooming.md` returns no output
- [ ] [AI] `beaver-nest`'s own naming-validate equivalent reports the file compliant on
      `origin/main`

> **Pause Safety**: `beaver-nest`'s propagation is pushed directly to its own `main`; local
> pre-push hooks passed. Safe to stop indefinitely — independent of Phases 2 and 3's progress. To
> resume: verify this gate, then continue to whichever of Phases 2/3 has not yet run.

## Phase 5: Knowledge Capture

> _Triage every surviving `learnings.md` entry before archival. See the
> [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)._

- [ ] [AI] Apply the litmus test to every `learnings.md` entry accrued during Phases 0-4 — keep
      only if a durable surface would catch this automatically next time; discard the rest with a
      one-line reason — acceptance: every entry has either a route or a discard reason
- [ ] [AI] Apply the **secret/sensitivity gate** to every surviving entry — sanitize any secret,
      credential, token, or private hostname to a `<placeholder>` token, or discard if unsanitizable
      — acceptance: `learnings.md` contains no raw secret
- [ ] [AI] Apply the **repo-relevance gate** to every surviving entry — infra-private content stays
      in `ose-private` only and is NEVER cross-routed into `ose-public`/`ose-primer`; public
      governance content may propagate via the existing parity loop — acceptance: no infra-private
      content appears in this repo's routed output
- [ ] [AI] Route each surviving learning to exactly one durable home. Expected candidate: a
      future-work idea recommending `plan-ideas-grooming`'s first real run be scheduled promptly
      (per `brd.md`'s staleness risk) — if this learning surfaces, file it as a new
      `plans/ideas/plan-ideas-grooming-first-run.md` two-pager in `ose-public` (small non-code
      routing, lands inline) rather than a `plans/backlog/` plan, since scheduling a future workflow
      invocation is not itself a code change — acceptance: every `learnings.md` entry records its
      terminal routing state
- [ ] [AI] If no generalizable learning surfaced beyond the expected future-work idea above, record
      the explicit note in `learnings.md` alongside it — acceptance: `learnings.md` is never
      silently empty

### Phase 5 Gate

> All checks below must pass before Plan Archival.

- [ ] [AI] Every `learnings.md` entry is in a terminal state (routed inline, filed as backlog, or
      discarded with reason), or the file records the explicit "none" escape
- [ ] [AI] No code-homed learning landed inline in this plan's own commits (this plan produced
      no `apps/`/`libs/` change, so this check is vacuously satisfied — confirmed by the File-Impact
      Analysis in `tech-docs.md` naming no such path)

> **Pause Safety**: `learnings.md` is fully triaged; no future process depends on querying it
> later. Safe to stop. To resume: re-read `learnings.md` and confirm every entry is terminal.

## Phase 6: Plan Archival

- [ ] [AI] Verify ALL delivery checklist items above are ticked, across all four repos' phases
- [ ] [AI] Verify the Knowledge Capture phase (Phase 5) is complete — every `learnings.md` entry
      reached a terminal state
- [ ] [AI] Verify ALL local quality gates passed on all four repos' `main` branches (pre-commit +
      pre-push hooks, per each phase's Local Quality Gates / Commit Guidelines sections). GitHub
      Actions CI is not checked anywhere in this plan, at any phase including this one — the local
      hooks are the sole gate, per explicit user instruction 2026-08-05 (see Delivery Mode note)
- [ ] [AI] Confirm no `plans/ideas/**` path was created, modified, or deleted in any of the four
      repos during this plan's delivery — `git -C <repo> log --name-only <phase-start-sha>..origin/main`
      (using each repo's own Phase 0 baseline commit as the start point) contains no
      `plans/ideas/` path, in all four repos — this is the scope-boundary check from `prd.md`'s
      final Gherkin scenario
- [ ] [AI] Rename and move: `git mv plans/in-progress/plan-ideas-grooming-workflow/ plans/done/YYYY-MM-DD__plan-ideas-grooming-workflow/`
      in `ose-public`, using today's date as the completion date (NOT the creation date)
- [ ] [AI] Update `ose-public/plans/in-progress/README.md` — remove the plan entry
- [ ] [AI] Update `ose-public/plans/done/README.md` — add the plan entry with completion date and a
      one-line summary noting the four-repo propagation
- [ ] [AI] Commit and push to `origin main` in `ose-public` (direct push, no PR — this plan's own
      `main-to-origin-main` Delivery Mode, DD-5): `chore(plans): move plan-ideas-grooming-workflow to done`

### Phase 6 Gate

- [ ] [AI] `ose-public`'s `plans/done/` contains the archived folder; `plans/in-progress/` does not

> **Pause Safety**: the plan is fully archived across all bookkeeping in `ose-public`; the four
> repos' actual delivered content already pushed in Phases 1-4 and is unaffected by this final
> housekeeping phase. Safe to stop — this is the plan's terminal state.

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
>
> **Phase Gate** — every phase ends with a `### Phase N Gate` (must-pass verification) plus a
> `> **Pause Safety**:` note (the safe-to-stop state and the single command to resume). A phase
> is not complete until its gate is green; do not start phase N+1 while any gate check fails.

# Delivery: Sync `ose-primer` Governance Parity

## Worktree

Code/content delivery happens entirely in **`ose-primer`**. This plan's own docs (this folder,
including `delivery.md` tick-updates, `learnings.md`, and `evidence/`) live in **`ose-public`** and
also need their own worktree: the
[plan-docs-only direct-push carve-out is retired in `ose-public`](../../../repo-governance/workflows/plan/plan-planning/07-plan-docs-only-carve-out.md#the-plan-docs-only-carve-out-superseded--retired-in-two-of-three-repos)
— `main` is branch-protected there too, so even a pure `plans/**` change goes through
`worktree-to-pr` like any other change.

| Repo         | Worktree path                             | Branch                                   |
| ------------ | ----------------------------------------- | ---------------------------------------- |
| `ose-primer` | `worktrees/sync-primer-governance-parity` | `worktree/sync-primer-governance-parity` |
| `ose-public` | `worktrees/sync-primer-governance-parity` | `worktree/sync-primer-governance-parity` |

**One worktree per repository** — the
[one-worktree-per-repo-per-plan HARD RULE](../../../repo-governance/conventions/structure/plans/31-worktree-cap.md#worktree-cap--one-worktree-per-repository-per-plan-hard-rule).
Two repos, two worktrees, no more.

`delivery.md` tick-updates and `learnings.md` entries accumulate as local commits in the
`ose-public` worktree throughout Phases 0–4 (bookkeeping, not code review); Phase 5 opens the
single `ose-public` PR that lands the full accumulated history plus the archival move — matching
the
[Phase 0 Opens No PR](../../../repo-governance/conventions/structure/plans/23-phase-0-opens-no-pr.md#phase-0-opens-no-pr--the-earliest-pr-is-phase-1-hard-rule)
"evidence rides the first real PR" pattern, applied here to the doc-only side of a cross-repo plan.

Optional manual pre-provisioning (run from each repo's root):

```bash
claude --worktree sync-primer-governance-parity
```

After `git worktree add` in either repo, run `npm install` **and** `npm run doctor -- --fix` per
[Worktree Toolchain Initialization](../../../repo-governance/development/workflow/worktree-setup.md).
Phase 0 enters both worktrees by default; the command above only pre-provisions them. The name
`sync-primer-governance-parity` matches the plan-folder identifier in both repos per the
[Worktree Specification HARD RULE](../../../repo-governance/conventions/structure/plans/29-worktree-specification.md#worktree-specification)
— no naming deviation.

## Delivery Mode: worktree-to-pr

Mandatory in both `ose-primer` and `ose-public` — `main` is branch-protected in both, including for
admins. Each PR is behaviour-classified:

| PR                                          | Repo         | Classification      | Merge requirement                                                                        |
| ------------------------------------------- | ------------ | ------------------- | ---------------------------------------------------------------------------------------- |
| PR1 (rhino-cli sync)                        | `ose-primer` | eligible executable | Up to seven CI-gated review cycles; exit at first clean code MEDIUM/HIGH/CRITICAL result |
| PR2 (`repo-governance/` + root files split) | `ose-primer` | noneligible static  | Green `.github/workflows/pr-quality-gate.yml`, then merge                                |
| PR3 (`.claude/` + mirrors split)            | `ose-primer` | noneligible static  | Green `.github/workflows/pr-quality-gate.yml`, then merge                                |
| PR4 (arm the gates)                         | `ose-primer` | eligible executable | Up to seven CI-gated review cycles; exit at first clean code MEDIUM/HIGH/CRITICAL result |
| PR5 (knowledge capture + archival)          | `ose-public` | noneligible static  | Green `.github/workflows/pr-quality-gate.yml`, then merge                                |

`[AI]` merges by default once all five hardened preconditions hold, in either repo.

## Fully AI-Deliverable

Every step below is `[AI]`. Grounded per category:

| Category               | Why no human is required                                                                            |
| ---------------------- | --------------------------------------------------------------------------------------------------- |
| Worktree create/remove | Git-mechanical steps are `[AI]` in `ose-primer`, same as `ose-public`/`ose-private`                 |
| Commits and pushes     | Push targets are plan branches and PRs, never `main`                                                |
| PR merges              | `[AI]` merges by default under Delivery Mode; markdown-only PRs need only a green quality gate      |
| Secrets                | No step reads, writes, or references any real secret or `.env.prod`/`.env.stag`                     |
| Git identity           | No step runs `git config user.*` at any scope or edits `.git/config`                                |
| Infrastructure         | No deploys, no runner provisioning, no external service calls (`ose-primer` is not Vercel-deployed) |
| Verification           | Gate execution, log reading, real-agent invocation — all in-repo and reproducible                   |
| CI                     | Polled with `gh run view --json status,conclusion` every 2 minutes; never `gh run watch`            |

## Quality Gate Discipline

**Fix ALL failures found during any quality gate run in this plan, not just those caused by your
own changes.** This applies to every "Verify" checkbox, every `### Phase N Gate`, and every
pre-push/CI run across Phases 1–5 — not only Phase 0's baseline resolution.

### Commit Guidelines

- Commit changes thematically — a Rust boundary-copy commit, a `repo-config.yml` gate-registration
  commit, and a convention-doc rename commit (all present together in Phase 1) are each their own
  commit, not one bundled commit.
- Follow Conventional Commits format: `<type>(<scope>): <description>` (e.g.,
  `chore(rhino-cli): sync byte-identical boundary from ose-public`,
  `docs(governance): split repo-governance/ under the 500-word ceiling`).
- Split different domains/concerns into separate commits.
- Do NOT bundle unrelated fixes into a single commit.

## Parallelization Model

**N=1** — this plan is a five-phase linear chain (Phase 1 → 2 → 3 → 4 → 5), each depending on the
previous phase's merged state (Phase 2/3 need Phase 1's dark-launched gates to measure against;
Phase 4 needs Phases 2–3's compliant content to arm safely). No independent subtrees to fan out —
unlike `optimize-governance-md`'s per-subtree parallelization, this plan's smaller scope
(`README.md` §Decisions) does not create genuinely independent work packages.

### Delivery Boundaries

| Phase | Subtree / concern                                                 | Repo         | Worktree                                  | PR   | Boundary? |
| ----- | ----------------------------------------------------------------- | ------------ | ----------------------------------------- | ---- | --------- |
| 0     | Baseline (no changes)                                             | both         | `worktrees/sync-primer-governance-parity` | none | no        |
| 1     | rhino-cli boundary sync + dark-launch gate registration           | `ose-primer` | `worktrees/sync-primer-governance-parity` | PR1  | yes       |
| 2     | `repo-governance/` + `AGENTS.md`/`CLAUDE.md` split                | `ose-primer` | `worktrees/sync-primer-governance-parity` | PR2  | yes       |
| 3     | `.claude/agents/` + `.claude/skills/` split + mirror regeneration | `ose-primer` | `worktrees/sync-primer-governance-parity` | PR3  | yes       |
| 4     | Arm the gates                                                     | `ose-primer` | `worktrees/sync-primer-governance-parity` | PR4  | yes       |
| 5     | Knowledge capture + archival (plan-docs only)                     | `ose-public` | `worktrees/sync-primer-governance-parity` | PR5  | yes       |

Every change-producing phase is its own delivery boundary — matching `optimize-governance-md`'s own
per-phase PR granularity rather than batching phases into fewer, larger PRs; each phase's output is
independently shippable and reviewable on its own. Phases 1–4 are `ose-primer`-only PRs; Phase 5 is
the sole `ose-public` PR, landing this plan's own doc-lifecycle changes (delivery ticks,
`learnings.md`, `evidence/`, archival move) in one PR rather than one per phase, since those are
bookkeeping commits accumulated locally, not independent shippable increments.

---

## Phase 0: Environment Setup and Baseline

> _Executor: repo-setup-manager_
>
> **No PR for this phase.** Phase 0 is local setup and baseline only: it opens no PR, pushes no
> branch, runs no PR-Review Maker→Fixer Cycle, and merges nothing. The earliest phase that may
> open a PR is Phase 1.

- [ ] [AI] Verify `ose-primer` checkout exists at `/Users/wkf/ose-projects/ose-primer`; if absent,
      clone it fresh (`git clone <ose-primer-remote-url> /Users/wkf/ose-projects/ose-primer`)
      — acceptance: `git -C /Users/wkf/ose-projects/ose-primer rev-parse --is-inside-work-tree`
      prints `true`
- [ ] [AI] `git -C /Users/wkf/ose-projects/ose-primer worktree add worktrees/sync-primer-governance-parity -b worktree/sync-primer-governance-parity`
      — acceptance: `git -C /Users/wkf/ose-projects/ose-primer worktree list` shows exactly one
      entry named `sync-primer-governance-parity`
- [ ] [AI] `git worktree add worktrees/sync-primer-governance-parity -b worktree/sync-primer-governance-parity`
      in the `ose-public` checkout (the second worktree, for this plan's own doc lifecycle)
      — acceptance: `git worktree list` in `ose-public` shows exactly one entry named
      `sync-primer-governance-parity`
- [ ] [AI] Install dependencies in both new worktrees: `npm install`
      — acceptance: exits 0 in both, `node_modules/` synchronized
- [ ] [AI] Converge the full polyglot toolchain in both worktrees: `npm run doctor -- --fix`
      — acceptance: exits 0 in both with no unresolved drift
- [ ] [AI] Run the baseline pre-push gate: `apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-push`
      — acceptance: exit code and any pre-existing failures recorded to
      `evidence/phase-0-baseline.txt`
- [ ] [AI] Resolve all preexisting failures found in the baseline run before proceeding
      — acceptance: no preexisting failures remain unresolved, or each is explicitly documented as
      out of this plan's scope with a one-line reason in `evidence/phase-0-baseline.txt`
- [ ] [AI] Re-derive this plan's authoring-time census live (word counts drift): run the same
      `wc -w` sweep documented in `README.md` §Context against
      `repo-governance/`, `.claude/agents/`, `.claude/skills/`, `.cursor/`, `.opencode/`,
      `.amazonq/`, `AGENTS.md`, `CLAUDE.md` — acceptance: fresh totals recorded to
      `evidence/phase-0-census.txt`, superseding the 2026-08-15 numbers in `README.md`/`brd.md`
      wherever they diverge
- [ ] [AI] Record the current `apps/rhino-cli` boundary diff against `ose-public`'s checkout
      (`diff -rq /Users/wkf/ose-projects/ose-public/worktrees/optimize-governance-md/apps/rhino-cli/src apps/rhino-cli/src`,
      repeated for `tests/`, `Cargo.toml`, `Cargo.lock`, `project.json`, `LICENSE`, and the
      Gherkin tree) — acceptance: non-empty diff recorded to `evidence/phase-0-boundary-diff.txt`
      (proves the drift this plan closes)

### Phase 0 Gate

- [ ] [AI] `npm install` exited 0 and `npm run doctor -- --fix` reports no unresolved drift
- [ ] [AI] Baseline `gate run --surface=pre-push` recorded, every preexisting failure resolved or
      explicitly out-of-scope
- [ ] [AI] Nothing was pushed and no PR exists for this branch in either repo:
      `git -C /Users/wkf/ose-projects/ose-primer ls-remote --heads origin worktree/sync-primer-governance-parity | grep -c .`
      returns `0`, `gh pr list --repo <ose-primer-remote> --head worktree/sync-primer-governance-parity --json number --jq 'length'`
      returns `0`, and the equivalent two checks against `ose-public`'s own remote/branch also
      return `0`

> **Pause Safety**: only the local toolchain was verified, the baseline recorded, and the live
> census/boundary-diff captured — no feature work exists yet, nothing is pushed, no PR exists.
> Safe to stop indefinitely. To resume: re-run the baseline command and confirm it is still clean.

---

## Phase 1: rhino-cli Boundary Sync + Dark-Launch Gate Registration (PR1, executable)

_Suggested executor: `swe-implementing-rust`_

### 1a. RED

- [ ] [AI] Confirm the new commands do not yet exist: run
      `apps/rhino-cli/scripts/rhino-bin.sh governance word-budget validate --help` and
      `apps/rhino-cli/scripts/rhino-bin.sh governance readme-index validate --help` in the worktree

  **Gherkin (binds) →** "The new governance commands exist in ose-primer after sync"

  ```gherkin
  Scenario: The new governance commands exist in ose-primer after sync
    Given the rhino-cli boundary sync from FR-1 has completed
    When I run "rhino-cli governance word-budget validate --help" and
      "rhino-cli governance readme-index validate --help" in the ose-primer worktree
    Then both commands are recognized and print usage text
    And the pre-sync command names "harness instruction-size validate" and "md readme-index validate"
      (the un-renamed form) no longer resolve, except where md-readme-index's underlying binary is
      reused unrenamed pending FR-2's repo-config.yml rename
  ```

  — acceptance: both commands currently exit non-zero / print "unrecognized subcommand", proving
  the pre-sync state this phase closes

### 1b. GREEN

- [ ] [AI] Copy byte-for-byte from
      `/Users/wkf/ose-projects/ose-public/worktrees/optimize-governance-md/apps/rhino-cli/{src,tests,Cargo.toml,Cargo.lock,project.json,LICENSE}`
      into the worktree's `apps/rhino-cli/` (full-tree replacement, not additive merge — remove
      any file present in the target but absent from the source copy)
      — acceptance: `diff -rq` on each of the six paths against the `ose-public` source is empty
- [ ] [AI] Copy byte-for-byte
      `specs/apps/rhino/behavior/rhino-cli/gherkin/**` from the same `ose-public` checkout into
      the worktree — acceptance: `diff -rq` is empty
- [ ] [AI] Regenerate the parity manifest: `apps/rhino-cli/scripts/rhino-bin.sh parity manifest generate`
      then `git add apps/rhino-cli/parity-manifest.sha256`
      — acceptance: `apps/rhino-cli/scripts/rhino-bin.sh parity manifest validate` exits 0
- [ ] [AI] Remove `repo-config.yml`'s top-level `instruction-size:` block (lines 200–243 as of
      this plan's authoring — re-locate by content, not line number, since prior edits shift
      lines) and the `instruction-size` gate id entry
      — acceptance: `grep -c "instruction-size" repo-config.yml` returns `0`
- [ ] [AI] Rename `repo-config.yml`'s `md-readme-index` gate id to `governance-readme-index` in
      place, command → `governance readme-index validate`, `args: { fail-kinds: [orphan, ghost] }`
      added, `surfaces` unchanged (`pre-push`/`ci`, both `scope: all-file-type`)
      — acceptance: `apps/rhino-cli/scripts/rhino-bin.sh governance readme-index validate` run
      unarmed reports the same `orphan`/`ghost` result the pre-rename `md readme-index validate`
      reported in Phase 0's baseline (no coverage gap)
- [ ] [AI] Register `governance-word-budget` and `governance-readme-completeness` in
      `repo-config.yml` per `tech-docs.md` §4's YAML, but with **no `pre-push`/`ci` surfaces yet**
      (dark-launched — registration only, matching `ose-public`'s Phase 1 / `ose-private`'s
      Phase 10 state) — acceptance: `apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-push`
      exits 0 and neither new gate id appears in the executed list

  **Gherkin (binds) →** "The two new gates are registered but not yet enforced"

  ```gherkin
  Scenario: The two new gates are registered but not yet enforced
    Given ose-primer's repo-config.yml has been updated per FR-2's registration step
    When I run "rhino-cli gate run --surface=pre-push" against ose-primer's real, not-yet-split
      repo-governance/ tree
    Then the exit code is 0
    And "governance-word-budget" and "governance-readme-completeness" are absent from the executed
      gate list (dark-launched, no pre-push/ci surface registered yet)
  ```

- [ ] [AI] Drop `md-frontmatter`'s `ci: { scope: all-file-type }` surface, keeping only
      `pre-commit: { scope: affected-file-type, glob: "*.md" }` — the proactive mitigation from
      `tech-docs.md` §2

  **Gherkin (binds) →** "md-frontmatter's ci surface is dropped before the FAIL-severity source lands"

  ```gherkin
  Scenario: md-frontmatter's ci surface is dropped before the FAIL-severity source lands
    Given ose-primer's repo-config.yml already registers "ci: { scope: all-file-type }" for
      md-frontmatter, and the copied frontmatter.rs hardcodes FAIL severity for governance docs with
      no config toggle
    When Phase 1's repo-config.yml edit drops the "ci" surface from the md-frontmatter entry, keeping
      only "pre-commit"
    Then a full-tree "rhino-cli md frontmatter validate" run against the not-yet-split
      repo-governance/ tree is not part of any armed pre-push or ci surface
    And CI on Phase 1's own PR does not fail on pre-existing missing-description/missing-when_to_use
      debt that Phases 2-3 have not yet cleared
  ```

  — acceptance: `apps/rhino-cli/scripts/rhino-bin.sh md frontmatter validate` against the real,
  unsplit `repo-governance/` reports its findings, but a full `gate run --surface=ci` does not
  fail on them

- [ ] [AI] `git mv repo-governance/conventions/structure/instruction-file-size-budget.md
repo-governance/conventions/structure/governance-word-budget.md`; port in the content shape
      from `ose-public`'s already-authored
      `repo-governance/conventions/structure/governance-word-budget.md` (word cap, thresholds,
      remediation shape), adjusted for `ose-primer`'s own trigger lists from `tech-docs.md` §4
      — acceptance: file exists at the new path, ≤500 words
- [ ] [AI] Discover and rewrite every inbound link live:
      `grep -rl "instruction-size\|instruction-file-size-budget" repo-governance .claude docs
AGENTS.md` in the `ose-primer` worktree, then update each match
      — acceptance: `grep -rl "instruction-file-size-budget"` after the edit returns no results
      outside this plan's own `plans/backlog/` history reference (there is none in `ose-primer`)

### 1c. REFACTOR

- [ ] [AI] Run `apps/rhino-cli/scripts/rhino-bin.sh doctor --fix` and `npm run lint:md` across the
      touched files — acceptance: both exit 0, no formatting drift left behind

### Verify

- [ ] **Command**: `npx nx run rhino-cli:test:quick && npx nx run rhino-cli:specs:behavior:coverage`
- [ ] **Acceptance**: both exit 0; `diff -rq` across all seven boundary paths
      (`src/`, `tests/`, `Cargo.toml`, `Cargo.lock`, `project.json`, `LICENSE`, Gherkin tree)
      against `ose-public`'s checkout is empty

  **Gherkin (binds) →** "The rhino-cli boundary is byte-identical to ose-public after sync"

  ```gherkin
  Scenario: The rhino-cli boundary is byte-identical to ose-public after sync
    Given the ose-primer worktree has received the byte-for-byte copy of ose-public's apps/rhino-cli
      src, tests, Cargo.toml, Cargo.lock, project.json, LICENSE, and Gherkin behavior tree
    When I run "diff -rq" across each of the seven boundary paths between the ose-public checkout and
      the ose-primer worktree
    Then every diff reports no differences
    And "rhino-cli parity manifest validate" exits 0 in the ose-primer worktree
  ```

### Local Quality Gates (Before Push)

- [ ] Run `apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-push`
- [ ] Fix ALL failures — including preexisting issues not caused by your changes
- [ ] Re-run failing checks to confirm resolution
- [ ] Verify zero failures before pushing

- [ ] [AI] Commit thematically (per §Commit Guidelines) and push to `origin worktree/sync-primer-governance-parity`
- [ ] [AI] Open a draft PR against `main` in `ose-primer` (PR1)
- [ ] [AI] Run the PR-Review Maker→Fixer Cycle to a clean code MEDIUM/HIGH/CRITICAL result (eligible
      executable work — up to seven CI-gated cycles)
- [ ] [AI] Merge PR1 once all five hardened preconditions hold

### Post-Push CI Verification

- [ ] Poll `gh run view --json status,conclusion` for PR1's CI run every 2 minutes until
      conclusion — acceptance: `conclusion == success`; never `gh run watch`
- [ ] If any CI check fails, fix immediately and push a follow-up commit; repeat until green

### Phase 1 Gate

- [ ] [AI] Boundary diff versus `ose-public` is empty for all seven boundary paths
- [ ] [AI] `parity manifest validate` exits 0 in `ose-primer`
- [ ] [AI] `governance-readme-index` (`orphan`/`ghost`) is armed and reports the same result as
      Phase 0's baseline — renamed in place, no gap
- [ ] [AI] `governance-word-budget` and `governance-readme-completeness` are registered but **not**
      armed — findings against the not-yet-split content are expected, not a gate failure
- [ ] [AI] `md-frontmatter`'s `ci` surface is confirmed dropped; `pre-commit` surface unchanged
- [ ] [AI] PR1 merged, CI green

> **Pause Safety**: `ose-primer`'s rhino-cli boundary is byte-for-byte synced with `ose-public` and
> its new gates are registered-but-unarmed. Safe to stop before Phase 2's content splitting begins.
> To resume: re-run `rhino-cli parity manifest validate` and confirm the boundary diff against
> `ose-public` is still empty.

---

## Phase 2: `repo-governance/` + Root Instruction Files (PR2, markdown-only)

_Suggested executor: `swe-developing-content` or a general-purpose content-authoring pass; consult
`.claude/skills/plan-creating-project-plans/reference/` for the progressive-disclosure split
pattern reused here_

- [ ] [AI] Re-derive the live list of `repo-governance/**/*.md` files over 500 words (do not trust
      this plan's 158-file authoring-time count) — acceptance: fresh list recorded to
      `evidence/phase-2-split-list.txt`
- [ ] [AI] **Split**: for each file on that list, create an index parent (keeping the original
      filename/path) plus a sibling directory of capped children
      (`<original-name>/01-slug.md`, `02-slug.md`, …), following the exact pattern documented in
      `tech-docs.md` §3 — acceptance: `apps/rhino-cli/scripts/rhino-bin.sh governance word-budget
validate repo-governance/` (direct, unarmed invocation) reports 0 failures

  **Gherkin (underpins) →** "A split file's index parent and children are all within budget"

- [ ] [AI] **Frontmatter**: add `when_to_use` to every file in `repo-governance/` (0/186 have it
      today); backfill `description` for the 22 files missing it — acceptance:
      `apps/rhino-cli/scripts/rhino-bin.sh md frontmatter validate repo-governance/` exits 0
- [ ] [AI] **Index**: create or update every `repo-governance/**/README.md` with annotated entries
      derived from target frontmatter `description`; split directories are indexed by their parent
      — acceptance: `apps/rhino-cli/scripts/rhino-bin.sh governance readme-index validate
repo-governance/` (direct, unarmed invocation) reports 0 `orphan`/`ghost`/`missing`/
      `unannotated` findings

  **Gherkin (underpins) →** "Every split child is reachable from its parent's README.md"

- [ ] [AI] Rewrite `AGENTS.md` as a directive index preserving `ose-primer`'s own repo-specific
      directives (not a copy of `ose-public`'s post-split content) — acceptance: `wc -w AGENTS.md`
      ≤ 500
- [ ] [AI] Rewrite `CLAUDE.md` as a directive index — acceptance: `wc -w CLAUDE.md` ≤ 500, and the
      resolved tree (`CLAUDE.md` + every `@`-imported file's word count) is ≤ 1,500 words

  **Gherkin (underpins) →** "AGENTS.md and CLAUDE.md are rewritten as directive indexes within budget"

- [ ] [AI] **Verify**: `apps/rhino-cli/scripts/rhino-bin.sh md links validate && apps/rhino-cli/scripts/rhino-bin.sh md heading-hierarchy validate && npm run lint:md`
      — acceptance: all three exit 0

### Local Quality Gates (Before Push)

- [ ] Run `apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-push`
- [ ] Fix ALL failures, including preexisting ones
- [ ] Verify zero failures before pushing

- [ ] [AI] Commit thematically and push to `origin worktree/sync-primer-governance-parity`
- [ ] [AI] Open a draft PR against `main` in `ose-primer` (PR2)
- [ ] [AI] Wait for a green `pr-quality-gate.yml` run (markdown-only, noneligible static work — no
      review cycle)
- [ ] [AI] Merge PR2

### Post-Push CI Verification

- [ ] Poll `gh run view --json status,conclusion` for PR2's `pr-quality-gate.yml` run every
      2 minutes until conclusion — acceptance: `conclusion == success`

### Phase 2 Gate

- [ ] [AI] `governance-word-budget` reports 0 failures under `repo-governance/`, `AGENTS.md`, and
      `CLAUDE.md` (direct invocation — the gate itself remains unarmed until Phase 4)
- [ ] [AI] `governance readme-index validate repo-governance/` reports 0 findings of any kind
      (direct invocation)
- [ ] [AI] `md links validate`, `md heading-hierarchy validate`, `npm run lint:md` all exit 0
- [ ] [AI] PR2 merged, CI green

> **Pause Safety**: `repo-governance/`, `AGENTS.md`, and `CLAUDE.md` are fully compliant and
> self-consistent. Safe to stop before Phase 3's `.claude/` work begins.

---

## Phase 3: `.claude/agents/` + `.claude/skills/` + Generated Mirrors (PR3, markdown-only)

_Suggested executor: `swe-developing-content`; agent-body migrations should consult
`.claude/skills/plan-creating-project-plans/reference/` for the reference-module pattern_

- [ ] [AI] Re-derive the live list of `.claude/agents/*.md` files over 500 words (do not trust this
      plan's 58-file authoring-time count) — acceptance: fresh list recorded to
      `evidence/phase-3-split-list.txt`
- [ ] [AI] **Migrate**: for each oversized agent, move non-charter content to
      `.claude/skills/<name>/reference/*.md`, leaving a charter ≤500 words that unconditionally
      instructs reading every reference module before acting — acceptance:
      `apps/rhino-cli/scripts/rhino-bin.sh governance word-budget validate .claude/agents/` reports
      0 failures

  **Gherkin (underpins) →** "An oversized agent body is migrated to a skill reference module"

- [ ] [AI] Re-derive the live list of `.claude/skills/*/SKILL.md` files over 500 words (do not
      trust this plan's 32-file authoring-time count); split each per the same index-parent
      pattern used in Phase 2 — acceptance:
      `apps/rhino-cli/scripts/rhino-bin.sh governance word-budget validate .claude/skills/` reports
      0 failures
- [ ] [AI] **Frontmatter + Index**: add `when_to_use`/`description` and annotated README entries
      across `.claude/agents/` and `.claude/skills/`, same as Phase 2's operations — acceptance:
      `md frontmatter validate .claude/` exits 0; `governance readme-index validate .claude/`
      (direct invocation) reports 0 findings
- [ ] [AI] Regenerate mirrors: `npm run generate:bindings`
      — acceptance: `.cursor/**/*.md` and `.opencode/agents/**/*.md` and `.amazonq/**/*.md`
      regenerate; `npm run validate:sync` exits 0

  **Gherkin (underpins) →** "Generated mirrors regenerate within budget after source is split"

- [ ] [AI] Verify regenerated mirrors are within budget: `governance word-budget validate .cursor/
.opencode/agents/ .amazonq/` (direct invocation) — acceptance: 0 failures; if any mirror
      still exceeds budget, fix the `.claude/` source or the binding generator, never hand-edit
      the mirror
- [ ] [AI] **Behavioral verification**: invoke at least five migrated agents on real tasks; confirm
      each reads its reference modules and applies a rule that lives only in one of them — record
      transcripts under `evidence/phase-3-agent-verification/`
- [ ] [AI] **Verify**: `apps/rhino-cli/scripts/rhino-bin.sh md links validate && apps/rhino-cli/scripts/rhino-bin.sh md heading-hierarchy validate && npm run lint:md`
      — acceptance: all three exit 0

### Local Quality Gates (Before Push)

- [ ] Run `apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-push`
- [ ] Fix ALL failures, including preexisting ones
- [ ] Verify zero failures before pushing

- [ ] [AI] Commit thematically and push to `origin worktree/sync-primer-governance-parity`
- [ ] [AI] Open a draft PR against `main` in `ose-primer` (PR3)
- [ ] [AI] Wait for a green `pr-quality-gate.yml` run (markdown-only, noneligible static work — no
      review cycle)
- [ ] [AI] Merge PR3

### Post-Push CI Verification

- [ ] Poll `gh run view --json status,conclusion` for PR3's `pr-quality-gate.yml` run every
      2 minutes until conclusion — acceptance: `conclusion == success`

### Phase 3 Gate

- [ ] [AI] `governance-word-budget` reports 0 failures under `.claude/`, `.cursor/`,
      `.opencode/agents/`, `.amazonq/` (direct invocation)
- [ ] [AI] `governance readme-index validate .claude/` reports 0 findings (direct invocation)
- [ ] [AI] `npm run validate:sync` exits 0
- [ ] [AI] Five recorded behavioral verifications exist under `evidence/phase-3-agent-verification/`
- [ ] [AI] PR3 merged, CI green

> **Pause Safety**: `.claude/`, `.cursor/`, `.opencode/`, and `.amazonq/` are fully compliant,
> self-consistent, and mirror-synced. Safe to stop before Phase 4's gate-arming begins.

---

## Phase 4: Arm the Gates (PR4, executable)

_Suggested executor: `swe-implementing-rust` (repo-config.yml + gate-registration change); no Rust
source edit required per `tech-docs.md` §4_

### 4a. RED

- [ ] [AI] Confirm the current pre-arm state: add a fixture file over 900 words under
      `repo-governance/`, run `apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-push`
      — acceptance: exit code 0 (the fixture is not yet caught — `governance-word-budget` is still
      unarmed), then remove the fixture

### 4b. GREEN

- [ ] [AI] Register `governance-word-budget` with `pre-push` and `ci` surfaces (`scope: path-gated`,
      the 9-entry trigger list, `ci-group: governance`) per `tech-docs.md` §4's YAML
      — acceptance: real-repo run reports 0 `[FAIL]` findings across the now-compliant tree, exit 0
- [ ] [AI] Register `governance-readme-completeness` with `pre-push` and `ci` surfaces
      (`args.paths`: `repo-governance/`, `.claude/`, `.codex/`; `fail-kinds`: `missing`,
      `unannotated`) per `tech-docs.md` §4's YAML — acceptance: real-repo run reports 0 findings,
      exit 0
- [ ] [AI] Re-add `md-frontmatter`'s `ci: { scope: all-file-type }` surface
      — acceptance: `apps/rhino-cli/scripts/rhino-bin.sh md frontmatter validate` against the full
      real repo reports 0 findings

  **Gherkin (binds) →** "md-frontmatter's ci surface is re-registered once content is compliant"

  ```gherkin
  Scenario: md-frontmatter's ci surface is re-registered once content is compliant
    Given every repo-governance/**/*.md file now carries when_to_use and description per FR-3/FR-4
    When Phase 4 re-adds "ci: { scope: all-file-type }" to md-frontmatter's repo-config.yml entry
    Then "rhino-cli md frontmatter validate" run against the full real repo reports 0 findings
    And the re-added ci surface does not reintroduce the Phase 1 premature-FAIL break, because the
      content it scans is now compliant
  ```

- [ ] [AI] Register `governance-word-budget` as a `repo-governance audit` category member, matching
      `ose-public`'s `harness_audit.rs` wiring (verify: it may already be true from the Phase 1
      byte-for-byte copy — confirm rather than re-add if already present)

### 4c. Re-verify (confirm the fixture now fails)

- [ ] [AI] Re-add the same over-900-word fixture from 4a under `repo-governance/`; run
      `apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-push`
      — acceptance: exit code 1, finding names the fixture; remove the fixture afterward

  **Gherkin (binds) →** "The armed gates fail on a deliberately reintroduced violation"

  ```gherkin
  Scenario: The armed gates fail on a deliberately reintroduced violation
    Given governance-word-budget and governance-readme-completeness are registered with pre-push and
      ci surfaces per FR-5's repo-config.yml edit
    When a fixture file over 900 words is added under repo-governance/ and
      "rhino-cli gate run --surface=pre-push" is run
    Then the exit code is 1
    And the finding names the fixture file
  ```

### 4d. REFACTOR

- [ ] [AI] `apps/rhino-cli/scripts/rhino-bin.sh doctor --fix`; confirm no drift left behind

### Local Quality Gates (Before Push)

- [ ] Run `apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-push`
- [ ] Fix ALL failures, including preexisting ones
- [ ] Verify zero failures before pushing

- [ ] [AI] Commit thematically and push to `origin worktree/sync-primer-governance-parity`
- [ ] [AI] Open a draft PR against `main` in `ose-primer` (PR4)
- [ ] [AI] Run the PR-Review Maker→Fixer Cycle to a clean code MEDIUM/HIGH/CRITICAL result (eligible
      executable work — up to seven CI-gated cycles)
- [ ] [AI] Merge PR4 once all five hardened preconditions hold

### Post-Push CI Verification

- [ ] Poll `gh run view --json status,conclusion` for PR4's CI run every 2 minutes until
      conclusion — acceptance: `conclusion == success`

### Phase 4 Gate

- [ ] [AI] `governance-word-budget` and `governance-readme-completeness` are armed (`pre-push` +
      `ci`) and report 0 failures against the real repo
- [ ] [AI] `md-frontmatter`'s `ci` surface is re-registered and reports 0 findings
- [ ] [AI] The RED→GREEN fixture cycle in 4a/4c is proven (recorded, fixture removed)
- [ ] [AI] PR4 merged, CI green
- [ ] [AI] `ose-primer` now enforces the identical gate set `ose-public`/`ose-private` enforce —
      `apps/rhino-cli/scripts/rhino-bin.sh parity manifest validate` still exits 0 (no boundary
      drift introduced by this phase's config-only changes)
- [ ] [AI] Remove the `ose-primer` worktree now that no further phase uses it — per the Worktree
      Specification, cleanup is immediate, not deferred to archival:
      `git -C /Users/wkf/ose-projects/ose-primer worktree remove worktrees/sync-primer-governance-parity`
      — acceptance: `git -C /Users/wkf/ose-projects/ose-primer worktree list` no longer shows it

> **Pause Safety**: `ose-primer`'s governance surface is fully split, compliant, and the two new
> gates plus `md-frontmatter`'s FAIL severity are armed identically to `ose-public`/`ose-private`.
> The `ose-primer` worktree is removed. Safe to stop indefinitely — this is the plan's substantive
> completion point. To resume: re-run `gate run --surface=pre-push` in a fresh `ose-primer` clone
> and confirm it is still green.

---

## Phase 5: Knowledge Capture and Archival (PR5, `ose-public`, markdown-only)

> _Triage every surviving `learnings.md` entry before archival. See the
> [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md).
> This entire phase runs in the **`ose-public`** worktree — Phases 1–4's `ose-primer` worktree is
> already removed by this point (see Phase 4's own cleanup note in its Gate)._

- [ ] [AI] Apply the litmus test to every `learnings.md` entry — keep only if a durable surface
      would catch this automatically next time; discard the rest with a one-line reason
      — acceptance: every entry has either a route or a discard reason
- [ ] [AI] Apply the **secret/sensitivity gate** to every surviving entry — sanitize any secret,
      credential, token, or private hostname to a `<placeholder>` token, or discard if unsanitizable
      — acceptance: `learnings.md` contains no raw secret
- [ ] [AI] Apply the **repo-relevance gate** — infra-private content stays out of `ose-public` and
      `ose-primer` entirely (neither is `ose-private`) — acceptance: no infra-private content
      appears in this repo's routed output
- [ ] [AI] Route each surviving learning to exactly one durable home; a learning whose home is
      `apps/`, `libs/`, or tests in `ose-public`, `ose-primer`, or `ose-private` is ALWAYS filed as
      a separate `plans/backlog/<slug>/` plan in the owning repo, never landed inline here
      — acceptance: every `learnings.md` entry records its terminal routing state
- [ ] [AI] For any entry routed to `plans/ideas/`, scan `plans/ideas/README.md` first for a brief
      already covering the same area; fold in rather than duplicate
      — acceptance: the entry's routing line names either the folded-into brief or confirms no
      overlap
- [ ] [AI] If no generalizable learning surfaced, record the explicit escape:
      `No generalizable learnings — <one-line reason>` — acceptance: `learnings.md` is never
      silently empty

### Phase 5 Gate

- [ ] [AI] Every `learnings.md` entry is in a terminal state, or the file records the explicit
      "none" escape
- [ ] [AI] No code-homed learning landed inline in this plan's own PRs
- [ ] [AI] Verify ALL delivery checklist items in Phases 0–4 are ticked
- [ ] [AI] Verify ALL quality gates pass (local + CI) across every merged PR
- [ ] [AI] Verify `ose-primer`'s `governance-word-budget`, `governance-readme-completeness`, and
      `md-frontmatter` gates are armed and green on `main`

> **Pause Safety**: `learnings.md` is fully triaged (or explicitly recorded as empty); no future
> process depends on querying it later. Safe to stop. To resume: re-read `learnings.md` and confirm
> every entry is terminal.

### Plan Archival (in the `ose-public` worktree provisioned in Phase 0)

- [ ] [AI] Verify ALL delivery checklist items in Phases 0–4 are ticked in this worktree's copy of
      `delivery.md`
- [ ] [AI] Verify the Knowledge Capture phase is complete per the gate above
- [ ] [AI] Verify ALL manual assertions (rhino-cli command invocations, gate runs) pass with
      committed evidence in `evidence/`
- [ ] [AI] Rename and move, inside the `ose-public` worktree:
      `git mv plans/backlog/sync-primer-governance-parity/ plans/done/YYYY-MM-DD__sync-primer-governance-parity/`
      using the actual completion date
- [ ] [AI] Update `plans/backlog/README.md` — remove the plan entry
- [ ] [AI] Update `plans/done/README.md` — add the plan entry with completion date
- [ ] [AI] Update `optimize-governance-md`'s own archived `README.md` (in `plans/done/`) if it still
      says "A follow-up plan must close it" without a forward reference — add one
- [ ] [AI] Commit thematically (per §Commit Guidelines) and push to
      `origin worktree/sync-primer-governance-parity` in `ose-public`
- [ ] [AI] Open a draft PR against `main` in `ose-public` (PR5 — the sole `ose-public` PR this plan
      opens, carrying the full accumulated `delivery.md`/`learnings.md`/`evidence/` history plus
      the archival move)
- [ ] [AI] Wait for a green `pr-quality-gate.yml` run (markdown-only, noneligible static work — no
      review cycle); merge PR5
- [ ] [AI] Remove the `ose-public` worktree:
      `git worktree remove worktrees/sync-primer-governance-parity` (run from the `ose-public`
      primary checkout)

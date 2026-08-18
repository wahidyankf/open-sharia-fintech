# 🚚 Delivery Checklist: Repo Rules Sweep

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
> Every step in this plan is `[AI]`. If execution discovers work that genuinely requires a person,
> stop that item and surface it rather than adding a human participant silently.

## Worktree

**`ose-public`** — `worktrees/optimize-gov/`, which **already exists and is already checked out** on
branch `worktree/optimize-gov`. No `git worktree add` runs for this repository; Phase 0 verifies and
fast-forwards it. The branch is 26 commits ahead of `origin/main` with a zero content diff (residue
of an earlier squash-merge), so the PR's file diff is correct while its commit list carries landed
history — accepted rather than rewritten.

**`ose-private`** — `worktrees/repo-rules-sweep/`, provisioned in Phase 4.

One worktree per repository per plan, per
[Worktree Cap](../../../repo-governance/conventions/structure/plans/31-worktree-cap.md#worktree-cap--one-worktree-per-repository-per-plan-hard-rule).

## Delivery Mode

**`worktree-to-pr`.** Exactly **one PR per repository for the entire plan** — every phase commits to
its repository's single branch and nothing opens a PR until Phase 6. Phase 0 opens no PR and pushes
no branch. `[AI]` merges once the PR-Review Maker→Fixer Cycle and the quality gate are satisfied.

Because there is one PR per repo, the Knowledge Capture and Archival phases commit to the same branch
and land inside that PR. The plan is complete at the moment the PR merges, which is what makes
in-PR archival coherent here.

## Workstreams

| ID | Workstream | Phases | Status |
| --- | --- | --- | --- |
| — | Shared baseline | 0 | Specified |
| WS-A | Ordinal filename prefixes in governed trees | 1–4 | Specified |
| WS-B | File Naming Convention rework | — | **Declared, not executable** |
| — | Knowledge Capture, Archival, and integration (terminal) | 5–6 | Specified |

A workstream added later inserts its phases before Knowledge Capture and renumbers the terminal
phases. No workstream executes until its phases, gates, and acceptance criteria are written here and
its requirements into `prd.md`.

## Parallelization Model

- **Serial spine**: Phase 1 (convention and machinery) → Phase 2 (index tooling) → Phase 3
  (`ose-public` sweep) → Phase 4 (`ose-private`) → Phase 5 (Knowledge Capture) → Phase 6
  (archival and integration). Each builds what the next reads: the rule is what rename decisions are
  made against, the order-preserving generator is the precondition that makes renaming non-lossy,
  and `ose-private` copies a finished `rhino-cli` change.
- **No independent branch.** Every phase writes to `repo-governance/` or `.claude/`, or depends on a
  tooling change, so nothing fans out. This is a genuine serial chain, not a list that happens to be
  ordered.
- **Chosen N**: 3 (the repository default). Within Phase 3 the per-directory rename work may fan out
  across N agents, since directories do not read each other's output; the rename map is the shared
  artifact and is written before the fan-out, not during it.
- **Terminal node**: Phase 6 depends on every other phase. Both PRs open there, and no worktree is
  removed until both have merged.

### Delivery Boundaries

| Phase(s) | Delivery unit | Worktree | Branch | PR opens |
| --- | --- | --- | --- | --- |
| 0 | — (setup and baseline) | — | — | no |
| 1–3, 5–6 | `ose-public` rules sweep | `worktrees/optimize-gov` (existing) | `worktree/optimize-gov` (existing) | yes — at Phase 6 |
| 4, 6 | `ose-private` rules sweep | `worktrees/repo-rules-sweep` (in `ose-private`) | `repo-rules-sweep` | yes — at Phase 6 |

## Phase 0: Baseline

- [ ] [AI] Verify the active worktree is `worktrees/optimize-gov` — acceptance: `git rev-parse --show-toplevel`
      ends in `worktrees/optimize-gov` and `git branch --show-current` prints `worktree/optimize-gov`.
- [ ] [AI] Fast-forward the branch with `git fetch origin && git merge --ff-only origin/main` —
      acceptance: `git rev-list --count HEAD..origin/main` returns 0.
- [ ] [AI] Run `npm install` — acceptance: exits 0 (this worktree has no `node_modules/` yet).
- [ ] [AI] Run `npm run doctor -- --fix` — acceptance: exits 0 with no unresolved toolchain findings.
- [ ] [AI] Run `npx nx run rhino-cli:test:quick` — acceptance: exits 0; record the pass count.
- [ ] [AI] Record the `ose-public` numbering baseline into
      `local-tmp/repo-rules-sweep/baseline-public.md`, capturing verbatim output of each command —
      acceptance: all five figures recorded.
      - `find repo-governance -name '*.md' | grep -cE '/[0-9]{2}-'`
      - `find .claude -name '*.md' | grep -cE '/[0-9]{2}-'`
      - `find . -name '*.md' -not -path './node_modules/*' | grep -E '/[0-9]{2}[a-z]-'`
      - `find repo-governance/workflows -name '*.md' | grep -E '/[0-9]{2}-phase-[0-9]+'`
      - `grep -rEn '\]\([^)]*/[0-9]{2}-[a-z0-9-]+\.md' --exclude-dir=node_modules --exclude-dir=.git . | wc -l`
- [ ] [AI] Record the same five figures for `ose-private` into
      `local-tmp/repo-rules-sweep/baseline-private.md` — acceptance: recorded; at authoring time
      `repo-governance` was 1704 of 2131 and `.claude` was 217.
- [ ] [AI] Confirm `ose-private` is on a clean `main` — acceptance:
      `git -C <ose-private-path> status --short` prints nothing.

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [ ] [AI] `npx nx run rhino-cli:test:quick` — exits 0.
- [ ] [AI] `git status --short` — prints nothing.
- [ ] [AI] Both baseline files exist with all five figures each.

> **Pause Safety**: the existing worktree is verified and current, the toolchain converged, and both
> repositories' numbering baselines recorded. Nothing is committed and no branch is pushed. Safe to
> stop. To resume: `npx nx run rhino-cli:test:quick`.

## Phase 1: Convention and Rules-Machinery Propagation

### The convention

- [ ] [AI] Create `repo-governance/conventions/structure/ordinal-filename-prefixes.md` stating the
      rule from `tech-docs.md` §2 plus its four worked cases, including
      `01-init-with-repo-setup-manager.md` as a passing example — acceptance: the file exists and
      `rhino governance word-budget validate` reports it under 500 words.
- [ ] [AI] Add the required frontmatter (`title`, `description`, `when_to_use`, `category`,
      `subcategory`, `tags`, `created`) — acceptance: `rhino md frontmatter validate` reports no
      finding for the file.
- [ ] [AI] Edit `repo-governance/conventions/structure/file-naming.md`: replace the "no prefixes,
      abbreviations, or hierarchical encoding" clause with a deferral to the new convention, and add
      the cross-link — acceptance: `grep -c 'no prefixes' repo-governance/conventions/structure/file-naming.md`
      returns 0 and a link to `ordinal-filename-prefixes.md` is present.
- [ ] [AI] Edit `repo-governance/conventions/structure/governance-word-budget-remediation.md` to
      state that shard filenames carry no ordinal and the parent index carries reading order —
      acceptance: the sentence is present and links the new convention.
- [ ] [AI] Edit `repo-governance/conventions/structure/workflow-naming.md` (and its shards) so the
      workflow filename rule composes with the ordinal rule — acceptance: the two conventions
      cross-link and neither asserts a rule the other forbids.
- [ ] [AI] Edit `repo-governance/development/infra/temporary-files/08-report-file-naming-standard.md`
      to state whether report filenames are exempt — acceptance: an explicit exempt-or-not sentence
      exists.
- [ ] [AI] Add the new convention to `repo-governance/conventions/structure/README.md` with a
      description-plus-`when_to_use` annotation — acceptance:
      `rhino governance readme-index validate --paths repo-governance/` reports no `orphan` or
      `unannotated` finding.

### Discovery for the machinery sweep

- [ ] [AI] Enumerate every governance, agent, and skill file stating a filename-naming rule with
      `grep -rln "kebab-case\|[Ff]ile [Nn]aming" --exclude-dir=node_modules .claude repo-governance docs`
      and record the list in the execution ledger with a `states-the-rule` or `merely-links-it`
      verdict per file — acceptance: at authoring time this returned about 50 files; every entry
      carries a verdict, none blank.

### The repo-rules machinery

- [ ] [AI] Edit `.claude/agents/repo/repo-rules-checker.md` to add ordinal-prefix judgement to its
      Core Repository Validation step as an **AI-only** category with no deterministic delegate —
      acceptance: the category and its criticality are stated, and
      `rhino governance word-budget validate` keeps the file under 500 words.
- [ ] [AI] Edit `.claude/agents/repo/repo-rules-fixer.md` to carry the ordinal-prefix fix
      disposition — acceptance: the file states the rename-and-relink sequence it may apply and the
      refusal condition for any path inside a generated mirror.
- [ ] [AI] Edit `.claude/agents/repo/repo-rules-maker.md` so newly authored conventions and shards are
      named under the rule — acceptance: the rule is stated or the convention linked as authority.
- [ ] [AI] Edit `.claude/skills/repo-validating-governance-rules/reference/01-core-validation-and-agent-duplication.md`
      to add the category to the Core Repository Validation list — acceptance: the category and its
      criticality are stated.
- [ ] [AI] Add an ordinal-prefix fix recipe to `.claude/skills/repo-rules-fixing/` — acceptance: the
      recipe states the rename sequence, the `rewrite-paths` step, the mirror-regeneration
      obligation, and the refusal condition.
- [ ] [AI] Edit `.claude/skills/repo-defining-workflows/SKILL.md` so workflow shard and step files
      follow the rule — acceptance: the rule is stated with one worked filename.
- [ ] [AI] Edit `.claude/skills/docs-managing-file-operations/reference/01-when-to-use-and-naming.md`
      so `docs-file-manager` renames under the rule — acceptance: the rule is stated or linked.
- [ ] [AI] Edit `repo-governance/workflows/repo/repo-rules-quality-gate/15-skip-list-curation-rules.md`
      to state the stable-key format for an ordinal-prefix finding — acceptance: the format is stated.
- [ ] [AI] Edit `repo-governance/workflows/repo/repo-rules-quality-gate/22-what-changed.md` to record
      the new AI-only category — acceptance: an entry naming it exists.
- [ ] [AI] For every remaining `states-the-rule` file from the discovery step, apply the same
      reconciliation — acceptance: every such entry has a recorded disposition of `updated` or
      `no-change-needed` with a one-line reason; none blank.
- [ ] [AI] Run `npm run generate:bindings` and `npm run validate:sync` — acceptance: both exit 0 and
      the regenerated mirrors are committed alongside the `.claude/` edits.

### Phase 1 Gate

- [ ] [AI] `rhino governance word-budget validate` — exits 0.
- [ ] [AI] `rhino governance readme-index validate --paths repo-governance/ --paths .claude/` — exits 0.
- [ ] [AI] `npm run validate:sync` — exits 0.
- [ ] [AI] `grep -rn 'ordinal-filename-prefixes' repo-governance/conventions/structure/file-naming.md` — at least one match.
- [ ] [AI] Every discovery entry with a `states-the-rule` verdict has a recorded disposition.

> **Pause Safety**: the rule is published, the `file-naming.md` contradiction is resolved, and the
> maker/checker/fixer triad plus the quality-gate workflow agree with it. No filename outside
> `.claude/` has changed and no tooling behaviour has changed. Safe to stop.
> To resume: `npm run validate:sync`.

## Phase 2: Order-Preserving Index Tooling

TDD is required. Each behaviour cycle is one RED step binding exactly one Gherkin scenario, then a
GREEN step, then a REFACTOR step.

- [ ] [AI] Add the three index-tooling scenarios from `prd.md` to
      `specs/apps/rhino/behavior/rhino-cli/gherkin/governance/governance-readme-index.feature` —
      acceptance: `rhino specs structure validate` exits 0 and the three titles are present.
- [ ] [AI] RED: add a failing unit test in
      `apps/rhino-cli/src/application/governance/readme_index.rs` asserting order preservation.
      **Gherkin (binds) →** "Generate no longer rewrites an existing index's order"

      ```gherkin
      Scenario: Generate no longer rewrites an existing index's order
        Given a directory already has a README.md index with hand-authored entry order
        When the maintainer runs rhino-cli governance readme-index generate on that directory
        Then the existing entries keep their order and annotations
        And only genuinely missing entries are appended
      ```

      — acceptance: `npx nx run rhino-cli:test` fails on that test only.
- [ ] [AI] GREEN: parse an existing index's entry list in `generate_index_file`, preserve each
      entry's position and annotation verbatim, and append only on-disk targets absent from it —
      acceptance: `npx nx run rhino-cli:test` exits 0.
- [ ] [AI] RED: add a failing unit test asserting the scaffold path is unchanged.
      **Gherkin (binds) →** "Generate still scaffolds a directory with no index"

      ```gherkin
      Scenario: Generate still scaffolds a directory with no index
        Given a directory has no README.md index
        When the maintainer runs rhino-cli governance readme-index generate on that directory
        Then a complete annotated index is written
        And every sibling file and subdirectory appears exactly once
      ```

      — acceptance: `npx nx run rhino-cli:test` fails on that test only.
- [ ] [AI] GREEN: keep today's `sorted_names()` scaffold behaviour for the no-index case —
      acceptance: `npx nx run rhino-cli:test` exits 0.
- [ ] [AI] RED: add a failing unit test for the new mode.
      **Gherkin (binds) →** "Rewrite-paths updates link targets without touching order"

      ```gherkin
      Scenario: Rewrite-paths updates link targets without touching order
        Given a rename map of old and new paths for a directory's children
        When the maintainer runs rhino-cli governance readme-index rewrite-paths with that map
        Then every index link target is updated to its new path
        And entry order, annotation text, and surrounding prose are unchanged
      ```

      — acceptance: `npx nx run rhino-cli:test` fails on that test only.
- [ ] [AI] GREEN: implement `readme-index rewrite-paths --map <tsv>` operating over the tracked
      markdown corpus, rewriting link targets only — acceptance: `npx nx run rhino-cli:test` exits 0.
- [ ] [AI] REFACTOR: extract index parsing into one named function shared by `generate` and
      `rewrite-paths` — acceptance: `npx nx run rhino-cli:test` and `npx nx run rhino-cli:lint` exit 0.
- [ ] [AI] Document both behaviours in
      `repo-governance/conventions/structure/governance-readme-completeness.md` — acceptance: the
      order-preserving contract and the `rewrite-paths` mode are described.

### Phase 2 Gate

- [ ] [AI] `npx nx run rhino-cli:test` — exits 0.
- [ ] [AI] `npx nx run rhino-cli:lint` — exits 0.
- [ ] [AI] A dry-run `readme-index generate` over `repo-governance/` produces no index reordering —
      `git diff --stat` after the dry run is empty.

> **Pause Safety**: the generator preserves hand-authored order and a rename-aware mode exists. No
> filename has changed. Safe to stop. To resume: `npx nx run rhino-cli:test`.

## Phase 3: `ose-public` Sweep

- [ ] [AI] Build the per-directory rename plan for every numbered directory under
      `repo-governance/` and `.claude/`, recording for each file a disposition of `renamed`,
      `merged-into`, or `kept` with a one-line reason — acceptance: every numbered file in the Phase 0
      baseline appears exactly once with a disposition; the `kept` set contains only real step
      sequences whose ordinal equals the step number.
- [ ] [AI] For each continuation-shard run (files whose titles continue one another by rule or
      section number), decide the boundary rework and record it — acceptance: each run has a recorded
      decision of `merge` or `rename-in-place`, with `rename-in-place` reserved for runs whose merge
      would change meaning.
- [ ] [AI] Apply the merges, then run `rhino governance word-budget validate` — acceptance: exits 0;
      any file over 500 words is re-split on a topic seam yielding self-standing names, never back
      into a numbered continuation.
- [ ] [AI] Apply every rename with `git mv`, emitting the old→new rename map as
      `local-tmp/repo-rules-sweep/renames-public.tsv` — acceptance: the map row count equals the
      `renamed` plus `merged-into` disposition count.
- [ ] [AI] Run `rhino governance readme-index rewrite-paths --map local-tmp/repo-rules-sweep/renames-public.tsv`
      over the tracked markdown corpus — acceptance: exits 0 and
      `grep -rEn '\]\([^)]*/[0-9]{2}-[a-z0-9-]+\.md' --exclude-dir=node_modules --exclude-dir=.git repo-governance .claude`
      returns only links to `kept` files.
- [ ] [AI] Run `npm run generate:bindings` and `npm run validate:sync` — acceptance: both exit 0 and
      the regenerated mirrors are committed with the `.claude/` renames.
- [ ] [AI] Run `rhino md links validate` — acceptance: exits 0, no broken link.
- [ ] [AI] Run `rhino governance readme-index validate --paths repo-governance/ --paths .claude/` —
      acceptance: exits 0; no `missing`, `orphan`, `ghost`, or `unannotated` finding.
- [ ] [AI] Spot-verify that annotations survived by diffing one index's entry text before and after —
      acceptance: entry text is byte-identical apart from link targets.

### Phase 3 Gate

- [ ] [AI] `find repo-governance .claude -name '*.md' | grep -E '/[0-9]{2}-'` returns only files on
      the recorded `kept` list.
- [ ] [AI] `find . -name '*.md' -not -path './node_modules/*' | grep -E '/[0-9]{2}[a-z]-'` — zero matches.
- [ ] [AI] No basename under `repo-governance/` carries both a leading ordinal and a `phase-<n>` or
      `step-<n>` token.
- [ ] [AI] `rhino md links validate`, `rhino governance readme-index validate`,
      `rhino governance word-budget validate`, `npm run validate:sync` — all exit 0.
- [ ] [AI] `npx nx run rhino-cli:test:quick` — exits 0.

> **Pause Safety**: `ose-public`'s governance and `.claude/` trees are fully swept, every index keeps
> its order and annotations, and the mirrors are regenerated. Committed to the branch, not yet pushed
> or reviewed. Safe to stop. To resume: `rhino md links validate`.

## Phase 4: `ose-private` Sweep

- [ ] [AI] Provision `worktrees/repo-rules-sweep/` in `ose-private` and branch `repo-rules-sweep`
      from its `main` — acceptance: `git worktree list` in `ose-private` shows the path.
- [ ] [AI] Apply the Phase 2 `apps/rhino-cli/` change byte-identically — acceptance: `diff -r` between
      the two repositories' `apps/rhino-cli/src/application/governance/` trees prints nothing.
- [ ] [AI] Apply the matching `specs/apps/rhino/` scenario additions — acceptance: the feature files
      are byte-identical across both repositories.
- [ ] [AI] Apply the Phase 1 convention and machinery edits, adapted to `ose-private`'s own paths —
      acceptance: the ordinal-prefix convention exists there and its `file-naming.md` carries the
      same reconciliation.
- [ ] [AI] Run the Phase 3 sweep procedure over `ose-private`'s `repo-governance/` and `.claude/`,
      emitting `renames-private.tsv` — acceptance: the same five gate commands exit 0 in
      `ose-private`.
- [ ] [AI] Run the `parity-manifest` gate in both repositories — acceptance: both exit 0.
- [ ] [AI] Run `npx nx run rhino-cli:test` in `ose-private` — acceptance: exits 0.

### Phase 4 Gate

- [ ] [AI] `parity-manifest` exits 0 in both repositories.
- [ ] [AI] `rhino md links validate`, `rhino governance readme-index validate`,
      `rhino governance word-budget validate`, `npm run validate:sync` — all exit 0 in `ose-private`.
- [ ] [AI] `npx nx run rhino-cli:test` — exits 0 in `ose-private`.

> **Pause Safety**: both repositories are swept and their tooling is byte-identical. Both branches
> hold committed, unpushed work. Safe to stop. To resume: run `parity-manifest` in either repository.

## Phase 5: Knowledge Capture

- [ ] [AI] Triage every entry in `learnings.md` through the
      [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)
      routing matrix — acceptance: every entry reaches a terminal state (routed inline, filed as a
      backlog plan, or discarded with a one-line reason).
- [ ] [AI] Run both safety gates (secret/sensitivity and repo-relevance) on every surviving entry —
      acceptance: each entry records a gate verdict.
- [ ] [AI] Record what `file-naming.md` still gets wrong, as the specification input for WS-B —
      acceptance: a WS-B input note exists in `learnings.md` or a `plans/backlog/` follow-up.

### Phase 5 Gate

- [ ] [AI] `learnings.md` has no untriaged entry, or carries the explicit
      `No generalizable learnings — <reason>` escape.
- [ ] [AI] Every large or code-bearing routing exists as a `plans/backlog/` folder.
- [ ] [AI] The WS-B specification input is recorded.

> **Pause Safety**: all durable knowledge has a home outside this plan folder. Safe to stop.
> To resume: re-read `learnings.md`.

## Phase 6: Archival and Integration

Archival commits to the same branch and lands inside the single PR, per the Delivery Mode section
above.

- [ ] [AI] Move the plan folder to `plans/done/<YYYY-MM-DD>__repo-rules-sweep/` using the completion
      date — acceptance: the folder exists under `plans/done/` and no longer under
      `plans/in-progress/`.
- [ ] [AI] Update `plans/README.md` and `plans/in-progress/README.md` indexes — acceptance:
      `rhino governance readme-index validate --paths plans/` exits 0.
- [ ] [AI] Push the `ose-public` branch to `origin worktree/optimize-gov` — acceptance: the branch
      exists on `origin`.
- [ ] [AI] Push the `ose-private` branch to `origin repo-rules-sweep` — acceptance: the branch exists
      on `origin`.
- [ ] [AI] Open one draft PR per repository against that repository's `main` — acceptance:
      `gh pr view` shows a PR in each.
- [ ] [AI] Run the PR-Review Maker→Fixer Cycle on each PR per
      [pr-review-quality-gate](../../../repo-governance/workflows/pr/pr-review-quality-gate.md),
      supplying the per-directory rename maps as the review artifact — acceptance: a clean cycle on
      each with no unresolved MEDIUM-or-higher thread.
- [ ] [AI] Merge the `ose-public` PR once `pr-quality-gate.yml` is green — acceptance: `gh pr view`
      shows MERGED.
- [ ] [AI] Merge the `ose-private` PR once its gate is green — acceptance: `gh pr view` shows MERGED.
- [ ] [AI] Verify nothing is uncommitted or unpushed in either worktree — acceptance:
      `git status --short` prints nothing in both.
- [ ] [AI] Remove `worktrees/repo-rules-sweep/` in `ose-private` — acceptance: `git worktree list`
      no longer shows it.
- [ ] [AI] Leave `worktrees/optimize-gov/` in place — acceptance: it still appears in
      `git worktree list`; it predates this plan and is not this plan's to remove.
- [ ] [AI] Delete `local-tmp/repo-rules-sweep/` in both repositories — acceptance: the path no longer
      exists in either.

### Phase 6 Gate

- [ ] [AI] Both PRs show MERGED.
- [ ] [AI] `parity-manifest` exits 0 in both repositories against their merged `main`.
- [ ] [AI] The plan folder exists only under `plans/done/`.
- [ ] [AI] `git worktree list` in `ose-private` shows no plan worktree.

> **Pause Safety**: both repositories carry the swept trees on `main`, the plan is archived, and only
> the pre-existing `optimize-gov` worktree remains. Terminal state.

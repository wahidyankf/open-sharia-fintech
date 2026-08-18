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

**`ose-private`** — `worktrees/repo-rules-sweep/`, provisioned in Phase 5.

One worktree per repository per plan, per
[Worktree Cap](../../../repo-governance/conventions/structure/plans/31-worktree-cap.md#worktree-cap--one-worktree-per-repository-per-plan-hard-rule).

## Delivery Mode

**`worktree-to-pr`.** Exactly **one PR per repository for the entire plan** — every phase commits to
its repository's single branch, and no phase opens a second PR.

**`ose-public`'s PR already exists**: <https://github.com/wahidyankf/ose-public/pull/227>, opened as
a **draft** carrying the plan documents, before execution began. This is a deliberate deviation from
the usual "PR opens at the delivery boundary" flow, taken so the plan is executed *through* its own
PR. Two consequences bind the executor:

- **Never run `gh pr create` for `ose-public`.** It would fail; the PR exists. At Phase 7 the action
  is `gh pr ready 227`, not create.
- **Every phase pushes to `worktree/optimize-gov`**, including Phase 0. The Phase 0 "pushes nothing,
  opens no PR" exemption
  ([§Phase 0 Opens No PR](../../../repo-governance/conventions/structure/plans/23-phase-0-opens-no-pr.md))
  is already discharged: the PR was opened before Phase 0 and Phase 0 opens nothing further. Pushing
  Phase 0's baseline evidence to the existing branch satisfies that convention's intent — the
  evidence lands in the first (and only) PR — while its letter, "do not open a PR for Phase 0",
  is not violated because no PR-opening action occurs in Phase 0.

Intermediate phases push for durability and run **no** PR-Review cycle. The cycle runs once, at
Phase 7, against the whole accumulated PR. Knowledge Capture and Archival commit to the same branch
and land inside that PR, so the plan is complete at the moment the PR merges — which is what makes
in-PR archival coherent here.

## Autonomous Execution Contract

This plan is designed to run end-to-end under
[plan-execution](../../../repo-governance/workflows/plan/plan-execution.md) **with no human in the
loop**. Everything that workflow would otherwise stop and ask about is pre-resolved here. If
execution reaches a decision this section does not cover, that is a plan defect — surface it rather
than inventing an answer.

| plan-execution stop | Resolution for this plan |
| --- | --- |
| `[HUMAN]` / `[AI+HUMAN]` checkbox (Iron Rule 2) | **None exist.** All 123 checkboxes are `[AI]`. |
| Rule-15 three-tester web-UI retest (shard 36) | **Not applicable — no rendered surface.** This plan changes markdown, `repo-config.yml`, and Rust CLI internals. It ships no route, component, or template. Do not invoke `web-exploratory-tester`, `web-usability-tester`, or `web-design-tester`. |
| Rule-16 API retest (shard 37) | **Not applicable — no HTTP surface.** No REST, GraphQL, or tRPC endpoint is added or changed. Do not invoke `api-exploratory-tester`. |
| Rule-1 production visual sign-off (shard 36) | **Not applicable** — same reason as rule-15. |
| Infra-Execution Gate (shard 40) | **Not applicable.** No `terraform apply`, no Ansible converge, no state-changing infrastructure operation appears in any phase. |
| Manual behavioral assertions (Iron Rule 8) | **Satisfied by gate commands, not by Playwright or curl.** The behavioral assertions for this plan are the acceptance clauses on each checkbox — exit codes and grep counts. There is nothing to click and nothing to `curl`. |
| `gh pr create` at the delivery boundary (shard 25) | **`ose-public`: forbidden**, PR #227 exists — use `gh pr ready 227`. **`ose-private`: see the `ose-private` delivery row in the Delivery Boundaries table.** |
| PR-Review Maker→Fixer Cycle (shard 39) | Runs **once per repository at Phase 7**, N = 3 cycles, hard ceiling. An `escalated` exit blocks the merge and is a legitimate stop — surface it. |
| Merge actor (shard 42) | **`[AI]`.** Merge once all four done-definition items hold. No `[HUMAN]` merge gate is declared anywhere in this plan. |
| Worktree cleanup prompt (shards 41, 42) | See **Worktree Disposition** below — pre-authorized, no prompt. |
| "Wait for user commit approval" (shard 02, item 10) | **Superseded by the per-phase gate flow.** Each `### Phase N Gate` commits and pushes under Iron Rules 5 and 7; there is no separate end-of-run approval step for this plan. |

**Tie-breakers, so no judgment call needs a human.** These bind Phases 4 and 5:

1. **Ordinal ambiguity → strip.** A directory keeps its ordinals only when the prose explicitly
   calls the files steps or phases *and* they are read in order. If the evidence is merely
   suggestive, de-number. The burden of proof is on keeping the number.
2. **Boundary rework → conservative merge only.** Merge a continuation run only when its titles
   continue one another *and* the combined text stays under 500 words. Every other run gets a
   self-standing rename in place. Never rewrite a rule's wording to make a merge fit — if it needs
   rewording, it is not a mechanical merge.
3. **Commit shape → one commit per top-level subtree.** `repo-governance/conventions/`,
   `repo-governance/development/`, `repo-governance/workflows/`, `repo-governance/principles/`,
   `repo-governance/vision/`, `.claude/skills/`. Roughly six commits, each independently revertible.
4. **When 1 and 2 disagree** — a run that should be merged sits inside a directory that should keep
   its ordinals — the directory-level verdict wins and the run is renamed in place, not merged.

**Legitimate stops that remain.** Autonomy is not a mandate to push through a genuine blocker. Stop
and surface, do not improvise, when: a gate fails for a reason no checkbox anticipated; the PR-Review
cycle exits `escalated`; a rename decision is genuinely ambiguous under the tie-breakers below and
the conservative default would lose information; or `ose-private` is unreachable.

## Workstreams

| ID | Workstream | Phases | Status |
| --- | --- | --- | --- |
| — | Shared baseline | 0 | Specified |
| WS-A | Ordinal filename prefixes in governed trees | 1–2, 4–5 | Specified |
| WS-C | Withdraw rules that obstruct: two suffix rules, one undocumented budget carve-out | 3 | Specified |
| WS-B | File Naming Convention rework | — | **Declared, not executable** |
| — | Knowledge Capture, Archival, and integration (terminal) | 6–7 | Specified |

WS-C runs **before** the sweep on purpose: it deletes thirteen numbered shards under
`agent-naming/` and `workflow-naming/` that the sweep would otherwise rename first and discard
second.

A workstream added later inserts its phases before Knowledge Capture and renumbers the terminal
phases. No workstream executes until its phases, gates, and acceptance criteria are written here and
its requirements into `prd.md`.

## Parallelization Model

- **Serial spine**: Phase 1 (convention and machinery) → Phase 2 (index tooling) → Phase 3
  (withdraw obstructive rules) → Phase 4 (`ose-public` sweep) → Phase 5 (`ose-private`) → Phase 6
  (Knowledge Capture) → Phase 7 (archival and integration). Each builds what the next reads: the rule
  is what rename decisions are made against, the order-preserving generator is the precondition that
  makes renaming non-lossy, the withdrawal removes files the sweep would otherwise process, and
  `ose-private` copies a finished `rhino-cli` change.
- **No independent branch.** Every phase writes to `repo-governance/` or `.claude/`, or depends on a
  tooling change, so nothing fans out. This is a genuine serial chain, not a list that happens to be
  ordered.
- **Chosen N**: 3 (the repository default). Within Phase 4 the per-directory rename work may fan out
  across N agents, since directories do not read each other's output; the rename map is the shared
  artifact and is written before the fan-out, not during it.
- **Terminal node**: Phase 7 depends on every other phase. Both PRs open there, and no worktree is
  removed until both have merged.

### Delivery Boundaries

| Phase(s) | Delivery unit | Worktree | Branch | PR opens |
| --- | --- | --- | --- | --- |
| 0 | — (setup and baseline) | — | — | no |
| 1–4, 6–7 | `ose-public` rules sweep and rule withdrawal | `worktrees/optimize-gov` (existing) | `worktree/optimize-gov` (existing) | yes — at Phase 7 |
| 5, 7 | `ose-private` rules sweep and rule withdrawal | `worktrees/repo-rules-sweep` (in `ose-private`) | `repo-rules-sweep` | yes — at Phase 7 |

## Phase 0: Baseline

_Suggested executor:_ `repo-setup-manager`

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

- [ ] [AI] Commit the baseline evidence and push to the existing `worktree/optimize-gov` branch —
      acceptance: `git status --short` prints nothing and `git rev-list --count origin/worktree/optimize-gov..HEAD`
      returns 0. Phase 0 opens no PR; PR #227 already exists, so this push adds evidence to it rather
      than creating anything.

> **Pause Safety**: the existing worktree is verified and current, the toolchain converged, both
> repositories' numbering baselines recorded, and the evidence pushed to the existing branch. No PR
> was opened. Safe to stop. To resume: `npx nx run rhino-cli:test:quick`.

## Phase 1: Convention and Rules-Machinery Propagation

_Suggested executor:_ `repo-rules-maker` for the convention text; `agent-maker` and `repo-workflow-maker` for the machinery edits

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

_Suggested executor:_ `swe-rust-dev`

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
- [ ] [AI] Regenerate the parity checksum manifest with `rhino parity manifest generate` and stage
      it in the same commit — acceptance: `rhino parity manifest validate` exits 0.
      `apps/rhino-cli/parity-manifest.sha256` checksums every `rhino-cli` file against the Git index,
      so **any** add, delete, or edit under `apps/rhino-cli/` invalidates it until regenerated.
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

## Phase 3: Withdraw Rules That Obstruct (WS-C)

_Suggested executor:_ `swe-rust-dev` for the deletions and gate registry; `repo-rules-maker` for the convention removals and the word-budget documentation; `repo-rules-fixer` for the prose sweep

Two enforced filename rules are withdrawn: the **agent role suffix** (`harness naming validate`) and
the **governance workflow type suffix** (`repo-governance workflows naming validate`). Both check
only a basename's last token against a closed vocabulary. Neither prevents a real defect, and both
force a rename whenever a genuinely new kind of agent or workflow appears.

**Existing filenames do not change.** `repo-rules-checker.md` and `pr-review-quality-gate.md` keep
their names; they simply stop being mandatory. This phase removes a constraint, not a convention in
practice.

### The mirror-drift hazard

`harness naming validate` has a **second, unrelated job**: it walks every generated tier in the
harness registry and reports `mirror-drift` when a `.claude/agents/` file has no counterpart. That
duty must survive. `harness sync validate` already covers `.opencode/` and `.cursor/`, and
`harness bindings validate` covers the Amazon Q bridge — but `harness sync validate` is reachable
only through `npm run validate:sync`; it is **not a declared gate**. Deleting `harness naming
validate` without acting would remove the only *gated* `.opencode/` mirror check.

- [ ] [AI] Confirm the hazard before deleting anything: `rhino harness naming validate` reports a
      `mirror-drift` kind, and `grep -F 'harness-sync' repo-config.yml` returns zero matches —
      acceptance: both hold, proving the coverage gap is real and not assumed.
- [ ] [AI] Declare a `harness-sync` gate in `repo-config.yml` running `harness sync validate` on the
      `pre-push` and `ci` surfaces — acceptance: `rhino repo-config validate` exits 0, and
      `grep -F 'harness sync validate' repo-config.yml` returns exactly one match.
- [ ] [AI] Prove the replacement gate actually catches what is being deleted: delete one
      `.opencode/agents/*.md` in a scratch copy, run `rhino harness sync validate`, restore it, run
      again — acceptance: non-zero exit before restore, exit 0 after. A gate that passes in both
      states has not replaced anything.

### Convention removal

- [ ] [AI] Delete `repo-governance/conventions/structure/agent-naming.md` and the seven files under
      `repo-governance/conventions/structure/agent-naming/` — acceptance:
      `find repo-governance/conventions/structure -name 'agent-naming*' | wc -l` returns 0.
- [ ] [AI] Delete `repo-governance/conventions/structure/workflow-naming.md` and the six files under
      `repo-governance/conventions/structure/workflow-naming/` — acceptance:
      `find repo-governance/conventions/structure -name 'workflow-naming*' | wc -l` returns 0.
- [ ] [AI] Record the withdrawal in
      `repo-governance/conventions/structure/file-naming.md` — one short paragraph naming both
      withdrawn rules and why, so a future reader finds the decision instead of the absence —
      acceptance: `grep -F 'role suffix' repo-governance/conventions/structure/file-naming.md`
      returns at least one match.
- [ ] [AI] Re-index the parent: `rhino governance readme-index generate` on
      `repo-governance/conventions/structure/` — acceptance:
      `rhino governance readme-index validate` exits 0 with no `ghost` finding.

### Tooling removal

- [ ] [AI] Delete `apps/rhino-cli/src/commands/harness_validate_naming.rs` and
      `apps/rhino-cli/src/commands/workflows_validate_naming.rs` — acceptance: both paths absent.
- [ ] [AI] Delete `apps/rhino-cli/src/internal/naming.rs` and
      `apps/rhino-cli/src/application/naming/` (`mod.rs`, `reporter.rs`). These are used **only** by
      the two deleted commands — acceptance:
      `grep -rn 'internal::naming\|application::naming' apps/rhino-cli/src apps/rhino-cli/tests`
      returns zero matches, and `npx nx run rhino-cli:build` exits 0.
- [ ] [AI] Remove both `pub mod` lines from `apps/rhino-cli/src/commands.rs`, both subcommand
      variants and both dispatch arms from `apps/rhino-cli/src/cli.rs`, and the three stale CLI
      parser tests that assert these commands parse (`old_harness_validate_naming_fails`,
      `new_harness_validate_naming_passes`, `verb_middle_workflows_validate_naming_no_longer_parses`)
      — acceptance: `npx nx run rhino-cli:build` exits 0 and
      `rhino harness naming validate` exits non-zero with an unrecognised-subcommand error.
- [ ] [AI] Delete `apps/rhino-cli/tests/agent_naming_validator.rs` and the twelve
      `tests/golden-master/{harness-naming*,harness-validate-naming*,workflows-validate-naming*,repo-governance-workflows-naming*}.{exit,stdout,stderr}`
      fixtures. **Keep every `md-naming*` fixture** — `md naming validate` is a different command and
      stays — acceptance: `find apps/rhino-cli/tests/golden-master -name 'md-naming*' | wc -l`
      is unchanged from the Phase 0 baseline.
- [ ] [AI] Delete the two feature files
      `specs/apps/rhino/behavior/rhino-cli/gherkin/harness/agents-validate-naming.feature` and
      `specs/apps/rhino/behavior/rhino-cli/gherkin/workflows/workflows-validate-naming.feature`, plus
      `specs/apps/rhino/behavior/rhino-cli/gherkin/agent-naming/agent-naming-validator.feature` —
      acceptance: `rhino specs coverage` exits 0, reporting neither an orphaned feature nor an
      uncovered command.

### Gate removal

- [ ] [AI] Delete the `harness-naming` and `workflows-naming` gate entries from `repo-config.yml` —
      acceptance: `grep -F 'harness naming validate' repo-config.yml` and
      `grep -F 'workflows naming validate' repo-config.yml` each return zero matches, while
      `grep -F 'md naming validate' repo-config.yml` still returns one.
- [ ] [AI] Regenerate the hook shims and CI job matrix from the registry — acceptance:
      `rhino gate validate` exits 0 and no CI job references a removed gate id.

### Prose sweep

- [ ] [AI] Enumerate every site stating either rule, with a per-file verdict, before editing any of
      them:
      `grep -rn 'harness naming validate\|workflows naming validate\|role suffix\|Role Vocabulary\|Type Vocabulary' AGENTS.md CLAUDE.md .claude repo-governance docs specs`
      — acceptance: the verdict table lists every hit as `edited`, `deleted`, or
      `no-change (unrelated sense)`. `<type>` and `<role>` appear in Conventional-Commits and
      emoji-vocabulary docs in an unrelated sense; those are `no-change`.
- [ ] [AI] Edit `AGENTS.md` §AI Agents to drop `<domain>-<role>` naming — acceptance:
      `grep -F '<domain>-<role>' AGENTS.md` returns zero matches, and `rhino governance word-budget validate` exits 0.
- [ ] [AI] Update `.claude/agents/README.md`, `repo-governance/workflows/README.md`,
      `repo-governance/development/agents/ai-agents/10-agent-naming-conventions.md`,
      `docs/reference/rhino-cli-command-triage.md`, `docs/reference/sdlc-gate-standard.md`, and
      `repo-governance/development/infra/nx-target-naming/04-cli-command-naming.md` — acceptance:
      every verdict in the table above is discharged and `rhino md links validate` exits 0.
- [ ] [AI] Regenerate mirrors: `npm run generate:bindings` — acceptance: `npm run validate:sync`
      exits 0 and mirrors land in the same commit as their `.claude/` sources.

### The word budget that already does not apply to `plans/`

`plans/**/README.md` is **already** outside the word budget: the `governance-word-budget` gate
carries an `exclude` prefix list (`plans/`, `docs/`, `specs/`, `.fvm/`, `.fvm-cache/`,
`.opencode/skills/`, `.opencode/commands/`), and `governance_validate_word_budget.rs` folds that same
list into a bare CLI run. No config change is needed. The defect is that
`governance-word-budget.md` publishes the `**/README.md` 700/900/900 row as though it were universal,
devotes a paragraph to glob-overlap resolution, and never mentions the exclusions — so an author
trims a plan README to satisfy a budget that was never going to be measured.

- [ ] [AI] Verify the exclusion before documenting it, rather than trusting the config: create a
      throwaway `plans/in-progress/probe/README.md` of 1200 words, run
      `rhino governance word-budget validate`, delete it — acceptance: exit 0 with no finding naming
      that path. If it *does* report, the exclusion is not what it appears and this section becomes
      a config change instead.
- [ ] [AI] Delete the throwaway probe directory — acceptance: `plans/in-progress/probe/` does not
      exist and `git status --short` shows no trace of it.
- [ ] [AI] Document the exclusion list in
      `repo-governance/conventions/structure/governance-word-budget.md`, next to the surface table:
      the seven excluded prefixes, that they are `str::starts_with` prefixes and not globs, and that
      `plans/`, `docs/`, and `specs/` are content trees the budget was never meant to reach —
      acceptance: `grep -F 'plans/' repo-governance/conventions/structure/governance-word-budget.md`
      returns at least one match, and the file still passes its own 500-word budget.
- [ ] [AI] State the rule the exclusion implies — a budget surface is a glob **minus** the registered
      exclude prefixes, and the exclude list is part of the published rule, not an implementation
      detail — acceptance: the convention says so in one sentence.

### Phase 3 Gate

- [ ] [AI] `npx nx run rhino-cli:test` and `npx nx run rhino-cli:lint` — both exit 0.
- [ ] [AI] `rhino parity manifest generate` has been run and staged after the deletions —
      acceptance: `rhino parity manifest validate` exits 0. Four source files and a module directory
      were removed; the manifest lists them until regenerated.
- [ ] [AI] `rhino repo-config validate`, `rhino gate validate`, `rhino specs coverage` — all exit 0.
- [ ] [AI] `rhino md links validate` — exits 0; no document links to a deleted convention.
- [ ] [AI] `rhino governance word-budget validate` — exits 0, and `governance-word-budget.md`
      documents the exclude list it has always applied.
- [ ] [AI] `npm run validate:sync` — exits 0, with the new `harness-sync` gate carrying it.
- [ ] [AI] An agent file named `.claude/agents/repo/repo-rules-frobnicator.md` passes every gate —
      acceptance: `rhino gate run --surface=pre-push` exits 0 with that file present. This is the
      point of the phase; if it still fails, the rule was not actually withdrawn. Delete the probe
      file afterwards.

> **Pause Safety**: the two rules and their tooling are gone, `harness-sync` covers the mirror duty
> that `harness naming validate` used to carry, and no file has been renamed. Safe to stop. To
> resume: `rhino gate validate && npx nx run rhino-cli:test`.

## Phase 4: `ose-public` Sweep

_Suggested executor:_ `docs-file-manager` for the renames and link repair; `repo-rules-fixer` for boundary rework

> **No identity-bearing filename is at risk.** All 232 numbered files under `.claude/` are skill
> **reference modules** (`.claude/skills/*/reference/NN-*.md`). Zero agent definitions and zero
> `SKILL.md` files carry an ordinal — verified at authoring time with
> `find .claude/agents -name '*.md' | grep -cE '/[0-9]{2}-'` returning 0. Agent and skill names are
> identities (frontmatter `name` must equal the filename stem or directory name); reference modules
> are reached only by link, which `rewrite-paths` repairs. Re-verify this before renaming: if either
> count is non-zero, stop — the sweep would break agent resolution.

- [ ] [AI] Re-verify the identity-safety precondition — acceptance:
      `find .claude/agents -name '*.md' | grep -cE '/[0-9]{2}-'` and
      `find .claude/skills -name 'SKILL.md' | grep -cE '/[0-9]{2}-'` both return 0. Stop if not.
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
- [ ] [AI] Repair links from **other** in-progress plans into renamed paths. At authoring time
      `plans/in-progress/repository-onboarding-readme-refresh/delivery.md` carries three such links.
      `md links validate` excludes `plans/done` but **not** `plans/in-progress`, so these break the
      gate. This is a mechanical link repair caused by our rename, so it is our obligation — but it
      touches another plan's docs: record every such path on the file-touch ledger and change nothing
      but the link target — acceptance: `grep -rEl '\]\([^)]*repo-governance/[^)]*/[0-9]{2}-[a-z0-9-]+\.md' plans/in-progress/`
      returns no file outside this plan's own folder.
- [ ] [AI] Run `rhino md links validate` — acceptance: exits 0, no broken link. The rewrite covers
      the whole tracked corpus including `docs/` and `specs/`, which link **into** `repo-governance/`
      even though they are out of scope for renaming.
- [ ] [AI] Run `rhino governance readme-index validate --paths repo-governance/ --paths .claude/` —
      acceptance: exits 0; no `missing`, `orphan`, `ghost`, or `unannotated` finding.
- [ ] [AI] Spot-verify that annotations survived by diffing one index's entry text before and after —
      acceptance: entry text is byte-identical apart from link targets.

### Phase 4 Gate

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

## Phase 5: `ose-private` Sweep

_Suggested executor:_ `docs-file-manager` and `repo-rules-fixer`, same split as Phase 4

- [ ] [AI] Provision `worktrees/repo-rules-sweep/` in `ose-private` and branch `repo-rules-sweep`
      from its `main` — acceptance: `git worktree list` in `ose-private` shows the path.
- [ ] [AI] Apply the Phase 2 and Phase 3 `apps/rhino-cli/` changes byte-identically — acceptance:
      `diff -r` prints nothing for `src/application/governance/`, `src/commands/`, `src/internal/`,
      and `src/application/` between the two repositories, and neither repository still contains
      `naming.rs` under `src/internal/`. Do **not** blanket-converge the two `rhino-cli` trees: the
      parity boundary is not the whole app and each repository legitimately carries files the other
      does not.
- [ ] [AI] Regenerate and stage `ose-private`'s parity manifest with `rhino parity manifest generate`
      — acceptance: `rhino parity manifest validate` exits 0 there.
- [ ] [AI] Apply the matching `specs/apps/rhino/` scenario additions — acceptance: the feature files
      are byte-identical across both repositories.
- [ ] [AI] Apply the Phase 1 convention and machinery edits, adapted to `ose-private`'s own paths —
      acceptance: the ordinal-prefix convention exists there and its `file-naming.md` carries the
      same reconciliation.
- [ ] [AI] Apply the Phase 3 withdrawal: delete the same two convention trees, the same `rhino-cli`
      commands and shared `naming` modules, the same gate entries, and add the same `harness-sync`
      gate — acceptance: `rhino harness naming validate` exits non-zero in `ose-private` too, and
      `grep -F 'harness sync validate' repo-config.yml` returns one match there.
- [ ] [AI] Run the Phase 4 sweep procedure over `ose-private`'s `repo-governance/` and `.claude/`,
      emitting `renames-private.tsv` — acceptance: the same five gate commands exit 0 in
      `ose-private`.
- [ ] [AI] Run the `parity-manifest` gate in both repositories — acceptance: both exit 0.
- [ ] [AI] Run `npx nx run rhino-cli:test` in `ose-private` — acceptance: exits 0.

### Phase 5 Gate

- [ ] [AI] `parity-manifest` exits 0 in both repositories.
- [ ] [AI] `rhino md links validate`, `rhino governance readme-index validate`,
      `rhino governance word-budget validate`, `npm run validate:sync` — all exit 0 in `ose-private`.
- [ ] [AI] `npx nx run rhino-cli:test` — exits 0 in `ose-private`.

> **Pause Safety**: both repositories are swept and their tooling is byte-identical. Both branches
> hold committed, unpushed work. Safe to stop. To resume: run `parity-manifest` in either repository.

## Phase 6: Knowledge Capture

_Suggested executor:_ the orchestrator directly — triage is judgment, not delegation

- [ ] [AI] Triage every entry in `learnings.md` through the
      [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)
      routing matrix — acceptance: every entry reaches a terminal state (routed inline, filed as a
      backlog plan, or discarded with a one-line reason).
- [ ] [AI] Run both safety gates (secret/sensitivity and repo-relevance) on every surviving entry —
      acceptance: each entry records a gate verdict.
- [ ] [AI] Record what `file-naming.md` still gets wrong, as the specification input for WS-B —
      acceptance: a WS-B input note exists in `learnings.md` or a `plans/backlog/` follow-up.
- [ ] [AI] Record the withdrawal criterion WS-C applied — a rule that inspects one token, never reads
      the file, and forces a code change to name a document — and audit the three surviving gated
      filename rules against it — acceptance: each of `md naming`, the `harness-sync` mirror check,
      and the `specs coverage` mapping carries a keep-or-withdraw verdict with a reason.
- [ ] [AI] Record the general defect WS-C's word-budget item exposed: a gate's `args` (exclude lists,
      thresholds) are part of the published rule, and a convention that documents only its surface
      globs misstates what is enforced — acceptance: the entry names at least one other gate whose
      `args` are undocumented, or states that none were found.

### Phase 6 Gate

- [ ] [AI] `learnings.md` has no untriaged entry, or carries the explicit
      `No generalizable learnings — <reason>` escape.
- [ ] [AI] Every large or code-bearing routing exists as a `plans/backlog/` folder.
- [ ] [AI] The WS-B specification input is recorded.

> **Pause Safety**: all durable knowledge has a home outside this plan folder. Safe to stop.
> To resume: re-read `learnings.md`.

## Phase 7: Archival and Integration

_Suggested executor:_ the orchestrator directly

Archival commits to the same branch and lands inside each repository's single PR, per the Delivery
Mode section above. **`ose-public`'s PR (#227) already exists as a draft** — this phase readies it,
it does not create it.

- [ ] [AI] Move the plan folder to `plans/done/<YYYY-MM-DD>__repo-rules-sweep/` using the completion
      date — acceptance: the folder exists under `plans/done/` and no longer under
      `plans/in-progress/`.
- [ ] [AI] Update `plans/README.md`, `plans/in-progress/README.md`, and `plans/done/README.md`
      indexes — acceptance: `rhino governance readme-index validate --paths plans/` exits 0 and
      `plans/done/README.md` carries a dated entry for this plan.
- [ ] [AI] Search for orphaned references to `plans/in-progress/repo-rules-sweep` and repoint them —
      acceptance: `grep -rn 'plans/in-progress/repo-rules-sweep' --exclude-dir=node_modules --exclude-dir=.git .`
      returns zero matches.
- [ ] [AI] Push the `ose-public` branch to `origin worktree/optimize-gov` — acceptance:
      `git rev-list --count origin/worktree/optimize-gov..HEAD` returns 0.
- [ ] [AI] Push the `ose-private` branch to `origin repo-rules-sweep` — acceptance: the branch exists
      on `origin`.
- [ ] [AI] Mark PR #227 ready for review with `gh pr ready 227` — acceptance: `gh pr view 227 --json isDraft`
      reports `false`. **Do not run `gh pr create` for `ose-public`**; it would fail.
- [ ] [AI] Open the `ose-private` PR — acceptance: `gh pr view` in `ose-private` shows an open PR
      against its `main`.
- [ ] [AI] Run the PR-Review Maker→Fixer Cycle on each PR per
      [pr-review-quality-gate](../../../repo-governance/workflows/pr/pr-review-quality-gate.md),
      supplying the per-directory rename maps as the review artifact — acceptance: N = 3 cycles
      complete on each, every thread answered, no unresolved MEDIUM-or-higher thread, and the loop
      did not exit `escalated`. An `escalated` exit blocks the merge and is a legitimate stop.
- [ ] [AI] Merge the `ose-public` PR once `pr-quality-gate.yml` is green — acceptance: `gh pr view 227`
      shows MERGED. `[AI]` merges; no human gate is declared.
- [ ] [AI] Merge the `ose-private` PR — acceptance: `gh pr view` shows MERGED. **Expect
      `parity-manifest` to report drift on this PR until it merges**: `apps/rhino-cli` byte-identity
      spans both repositories, so between the two merges the trees genuinely differ. That drift is
      the gate working, not a defect — it clears when the second merge lands. Merge the two as close
      together as the review cycles allow, and assert parity only after both.
- [ ] [AI] Verify nothing is uncommitted or unpushed in either worktree — acceptance:
      `git status --short` prints nothing in both.
- [ ] [AI] Remove `worktrees/repo-rules-sweep/` in `ose-private` with non-force
      `git worktree remove` — acceptance: `git worktree list` no longer shows it. **The user has
      pre-authorized this removal**; the interactive confirmation that
      [shard 42](../../../repo-governance/workflows/plan/plan-execution/42-finalization-pr-merge-and-final-status.md)
      normally requires is granted here in writing, so do not prompt. The safety preconditions still
      apply in full: refuse if `git status --porcelain` is non-empty or the branch is not an ancestor
      of `origin/main`.
- [ ] [AI] Leave `worktrees/optimize-gov/` in place — acceptance: it still appears in
      `git worktree list`. It predates this plan and is not this plan's to remove; the pre-authorization
      above does **not** extend to it.
- [ ] [AI] Delete `local-tmp/repo-rules-sweep/` in both repositories — acceptance: the path no longer
      exists in either.

### Phase 7 Gate

- [ ] [AI] Both PRs show MERGED.
- [ ] [AI] `parity-manifest` exits 0 in both repositories against their merged `main`.
- [ ] [AI] The plan folder exists only under `plans/done/`.
- [ ] [AI] `git worktree list` in `ose-private` shows no plan worktree; `worktrees/optimize-gov/`
      still exists in `ose-public`.

> **Pause Safety**: both repositories carry the swept trees on `main`, the plan is archived, and only
> the pre-existing `optimize-gov` worktree remains. Terminal state.

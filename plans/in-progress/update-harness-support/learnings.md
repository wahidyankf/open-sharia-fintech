<!-- Knowledge Capture running log — append entries during execution. -->
<!-- Triage every entry (or record the explicit "none" escape) before archival. -->

# Learnings: update-harness-support

## Baseline

Recorded at Phase 0 on branch `worktree/update-harness-support`, merged up to `origin/main`
`c668d23ef`. All figures are `git ls-files <path> | grep -c .` unless stated.

| Binding tree | Tracked files | Plan expectation | Match |
| ------------ | ------------- | ---------------- | ----- |
| `.claude`    | 659           | 659              | yes   |
| `.opencode`  | 112           | 112              | yes   |
| `.cursor`    | 93            | 93               | yes   |
| `.agents`    | 24            | 24               | yes   |
| `.amazonq`   | 2             | 2                | yes   |
| `.codex`     | 2             | 2                | yes   |
| `.pi`        | 1             | 1                | yes   |

Instruction-file word counts (`tr -s '[:space:]' '\n' < "$f" | grep -c .`):

| File        | Words | Fail threshold | Headroom |
| ----------- | ----- | -------------- | -------- |
| `AGENTS.md` | 487   | 500            | 13       |
| `CLAUDE.md` | 423   | 500            | 77       |

Governance sweep sets, written to the uncommitted `local-tmp/harness-sweep-baseline.txt`:

- `Cursor` (case-insensitive): 43 files
- `windsurf|junie|antigravity|aider|copilot|pi\.dev|amazonq|Amazon Q|Kiro`: 45 files

Both counts match the plan's predictions exactly, so Phase 3's sweep is sized correctly.

### Phase 0 deviations

- **Sync method.** The checklist says `git rebase origin/main`. The branch was already pushed and
  carries an open delivery boundary, so a rebase would have required a force-push. Merged instead
  (`6e6520dac`); the acceptance that matters — zero commits behind `origin/main` — holds either way.
  The incoming commit `c668d23ef` groomed `plans/ideas/`, and its full diff was read before
  continuing.
- **Plan adapted to the incoming commit.** `c668d23ef` added three Q2 briefs whose premises name
  harnesses this plan drops (`harness-level-env-file-enforcement-gap`,
  `extend-byte-identity-to-claude-hooks`, `governance-command-name-reconciliation`). Rather than
  narrowing only those three, Phase 9 gained a generalized step that sweeps the whole `plans/ideas/`
  tree and records a verdict per file — `origin/main` keeps adding briefs, so the class needed the
  fix, not the three sites.
- **`npm doctor` warning left standing.** `npm` is v11.16.0 against a required v11.11.0. `doctor
--fix` exits 0 and reports "Nothing to fix"; the pin is a global Volta concern outside this plan's
  scope, so it is recorded rather than changed.

## PR

- `ose-public` — [#232](https://github.com/wahidyankf/ose-public/pull/232), opened as a draft after
  the Phase 0 gate. Every later phase pushes to this same PR; a second number appearing means the
  one-PR-per-repository override was violated.
- `ose-private` — opened during the Cross-Repo Parity Ritual, after Phase 11.

## Phase 1 notes

- **Four Amazon Q unit tests were removed a phase early.** `amazonq_dry_run_{text,json,markdown}_output_runs_without_panic`
  and `harness_amazonq_dry_run_via_run_reaches_dry_run_branch` read `harness.amazonq.agent-name`
  from the real `repo-config.yml`. The moment the registry contracted, that entry was gone and the
  path they exercise became unreachable — so they went red at Phase 1 rather than at the Phase 2
  flag-removal step the plan scheduled them for. Deleting a test for a deliberately-removed
  capability is honest; marking it `#[ignore]` would have been test-integrity gaming, so the removal
  moved forward instead.
- **`KNOWN_BINDING_DIRS` had to learn `.agents` at Phase 1, not Phase 6.** The Codex registry entry
  declares `skills-dir: .agents/skills`, and `harness-bindings.feature`'s data-driven scenario
  asserts every registry-declared path appears in that constant. Declaring the surface in the
  registry is what forced the constant to follow — which is the direction the plan wants, and worth
  noting as evidence the registry really is authoritative.
- **Fixture repos now need a `repo-config.yml`.** Five `agents-sync` scenarios drove
  `harness bindings generate --harness opencode` against a temp repo with no config at all. Once
  `--harness` resolves through the registry, a config-less repo is not a valid fixture. They were
  given the same three-entry registry production carries rather than having the guard weakened to
  tolerate a missing file.

## Phase 2 notes

- **Two Phase 2 acceptance clauses are internally unsatisfiable as written; the substantive half
  won.** P2.7 instructs retargeting two tests to assert the `unknown harness name 'amazonq'`
  rejection, then asserts `git grep -c '"amazonq"' apps/rhino-cli/src/commands/harness_generate_bindings.rs`
  returns no match — but a test that asserts the rejection must spell the rejected name. Same shape
  in P2.11: it instructs carrying the US-2 scenarios from `prd.md`, which name `.cursor/`,
  `.amazonq/`, `.pi/` and `--harness cursor` by design, then asserts no surviving scenario names a
  dropped harness. In both cases the test/scenario proving the _absence_ of support is the more
  valuable artifact, so it was kept and the grep-count clause recorded as not met. The general
  lesson: a "no match" grep clause and an instruction to write a regression test naming the removed
  thing cannot both hold — the plan-authoring pass should catch that pairing.
- **US-2's "Historical records keep their dropped-harness references" scenario was deferred to
  Phase 3.** Its second `Then` asserts no live governance document presents a dropped harness as
  supported — that is precisely what the Phase 3 prose sweep produces. Landing it at Phase 2 would
  have created a knowingly-red test, so it moves to Phase 3 beside P3.13's carve-out check.
- **The mutated/missing generated-file Gherkin scenarios were removed rather than retargeted.**
  Between the Amazon Q emitter's deletion here and Phase 5's Codex emitter, `expected_bindings`
  returns an empty vector, so there is no generated binding file for a CLI-level scenario to mutate
  or delete. The plan already relocated that coverage to unit tests in `bindings.rs` that construct
  a `BindingFile` fixture directly; the CLI-level scenarios return in Phase 5 pointed at Codex.
- **The gate trigger sweep was widened past the three names the step listed.** P2.6 names only
  `.cursor/`, `.pi/`, `.amazonq/`, but the `harness-bindings` pre-push trigger also listed
  `.windsurf/`, `.junie/`, `GEMINI.md`, and `CONVENTIONS.md` — every one a dropped harness whose
  surface `KNOWN_BINDING_DIRS` no longer knows. Removing only the three named would have left the
  same defect class behind, so all seven went.
- **One stale comment survives on purpose.** The explanatory comment above the
  `governance-readme-completeness` gate still names `.pi/` in its scoped-trees sentence. P2.6
  explicitly excludes those comment lines from its scope; the Phase 3 prose sweep owns them.
- **`emit_bindings` had three callers outside `bindings.rs`.** `tests/repo_config_data_driven.rs`
  and `tests/specs_tree.rs` both drove it to build fixtures, and the data-driven feature carried an
  Amazon-Q-definition-name scenario. Deleting an emitter is never a single-file edit — grep the test
  tree and the feature tree for the symbol before calling the deletion scoped.

## Sweep verdicts

58 paths, recomputed post-Phase-2 into `local-tmp/harness-sweep-current.txt`. One row per path.

| Path                                                                                                                            | Verdict         | Note                                                                       |
| ------------------------------------------------------------------------------------------------------------------------------- | --------------- | -------------------------------------------------------------------------- |
| `.claude/agents/README.md`                                                                                                      | EDIT            | mirror list names `.cursor/`, `.amazonq/`                                  |
| `.claude/skills/api-testing-exploratory-methodology/reference/session-based-methodology.md`                                     | FALSE-POSITIVE  | pagination cursor                                                          |
| `.claude/skills/api-testing-exploratory-methodology/reference/test-dimensions-checklist-part1.md`                               | FALSE-POSITIVE  | pagination cursor                                                          |
| `.claude/skills/pr-review-scout-classification/reference/shared-context-and-prior-cycle-read.md`                                | EDIT            | generated-path list names `.amazonq/**`                                    |
| `.claude/skills/repo-harness-compatibility-protocol/reference/phase0-parity-invariants.md`                                      | EDIT            | Invariant 3 diff set                                                       |
| `.claude/skills/repo-harness-compatibility-protocol/reference/phase1-drift-dimensions-d1-d3.md`                                 | EDIT            | harness enumeration names Aider                                            |
| `.claude/skills/repo-harness-compatibility-protocol/reference/phase1-drift-dimensions-d4-d7.md`                                 | EDIT            | D7 is a Cursor-only dimension                                              |
| `.claude/skills/repo-validating-governance-rules/reference/core-validation-and-agent-duplication.md`                            | EDIT            | mirror exclusion list                                                      |
| `CLAUDE.md`                                                                                                                     | EDIT            | §Multi-harness configuration                                               |
| `docs/explanation/plan-domain-parity-decisions.md`                                                                              | HISTORICAL-KEEP | dated 2026-06-06 decision record                                           |
| `docs/explanation/post-mortems/2026-05-03-amazonq-bindings-prettier-parity-guard-break.md`                                      | HISTORICAL-KEEP | incident record                                                            |
| `docs/explanation/post-mortems/README.md`                                                                                       | HISTORICAL-KEEP | index entry for that incident                                              |
| `docs/explanation/software-engineering/platform-web/tools/fe-nextjs/styling.md`                                                 | FALSE-POSITIVE  | CSS `cursor:`                                                              |
| `docs/explanation/software-engineering/platform-web/tools/fe-react/accessibility.md`                                            | FALSE-POSITIVE  | CSS `cursor:`                                                              |
| `docs/explanation/software-engineering/platform-web/tools/fe-react/data-fetching.md`                                            | FALSE-POSITIVE  | pagination cursor                                                          |
| `docs/explanation/software-engineering/platform-web/tools/fe-react/styling.md`                                                  | FALSE-POSITIVE  | CSS `cursor:`                                                              |
| `docs/explanation/software-engineering/programming-languages/c-sharp/api-standards.md`                                          | FALSE-POSITIVE  | cursor-based pagination                                                    |
| `docs/explanation/software-engineering/programming-languages/typescript/memory-management.md`                                   | FALSE-POSITIVE  | database cursor                                                            |
| `docs/explanation/software-engineering/programming-languages/typescript/performance.md`                                         | FALSE-POSITIVE  | database cursor                                                            |
| `docs/reference/ai-model-benchmarks.md`                                                                                         | FALSE-POSITIVE  | CursorBench is an external benchmark name                                  |
| `docs/reference/platform-bindings.md`                                                                                           | EDIT            | catalog rows; Phase 4 and Phase 10 refine further                          |
| `docs/reference/rhino-cli-command-triage.md`                                                                                    | EDIT            | command inventory                                                          |
| `docs/reference/sdlc-gate-standard.md`                                                                                          | EDIT            | gate inventory                                                             |
| `docs/reference/security/frameworks/nist-sp-800-53-rev5.md`                                                                     | FALSE-POSITIVE  | "precursors"                                                               |
| `repo-governance/conventions/structure/governance-readme-completeness.md`                                                       | EDIT            | mirror list                                                                |
| `repo-governance/conventions/structure/governance-vendor-independence/forbidden-vendor-terms-models-and-concepts.md`            | EDIT            | keep terms forbidden (DD-3), drop supported framing                        |
| `repo-governance/conventions/structure/governance-vendor-independence/forbidden-vendor-terms-names-and-paths.md`                | EDIT            | same                                                                       |
| `repo-governance/conventions/structure/governance-vendor-independence/platform-binding-directory-pattern-and-migration.md`      | EDIT            | same                                                                       |
| `repo-governance/conventions/structure/governance-vendor-independence/purpose-and-scope.md`                                     | EDIT            | same                                                                       |
| `repo-governance/conventions/structure/governance-vendor-independence/vocabulary-map.md`                                        | EDIT            | same                                                                       |
| `repo-governance/conventions/structure/governance-word-budget.md`                                                               | EDIT            | surface table                                                              |
| `repo-governance/conventions/structure/multi-harness-binding/platform-binding-examples.md`                                      | EDIT            | three-harness model                                                        |
| `repo-governance/conventions/structure/post-mortems/mandatory-sections-timeline-through-resolution.md`                          | HISTORICAL-KEEP | worked example quotes a real incident                                      |
| `repo-governance/conventions/structure/post-mortems/no-secrets-rule-diagrams-and-examples.md`                                   | HISTORICAL-KEEP | same                                                                       |
| `repo-governance/conventions/structure/post-mortems/optional-sections-and-severity-scale.md`                                    | HISTORICAL-KEEP | same                                                                       |
| `repo-governance/conventions/tutorials/in-the-field/guide-structure-part2-database-example-setup.md`                            | FALSE-POSITIVE  | database cursor                                                            |
| `repo-governance/development/agents/ai-agents/multi-harness-binding-directory-hierarchy-format.md`                              | EDIT            | directory hierarchy                                                        |
| `repo-governance/development/agents/ai-agents/tool-access-patterns-writing-to-platform-binding-directories.md`                  | EDIT            | mirror list                                                                |
| `repo-governance/development/agents/model-selection.md`                                                                         | EDIT            | index line names Cursor                                                    |
| `repo-governance/development/agents/model-selection/platform-binding-examples.md`                                               | EDIT            | Cursor tier-collapse table                                                 |
| `repo-governance/development/infra/nx-target-naming/cli-command-naming.md`                                                      | EDIT            | renamed-command table                                                      |
| `repo-governance/development/infra/nx-target-naming/domain-work-scheme.md`                                                      | EDIT            | target description                                                         |
| `repo-governance/development/infra/nx-targets/domain-work-naming-for-governance-targets.md`                                     | EDIT            | target description                                                         |
| `repo-governance/development/practice/file-touch-discipline/agent-checklist-and-related-docs.md`                                | EDIT            | mirror list                                                                |
| `repo-governance/development/practice/file-touch-discipline/standard-9.md`                                                      | EDIT            | mirror list                                                                |
| `repo-governance/development/practice/mechanize-cross-file-invariants/prior-art-in-this-repository.md`                          | EDIT            | mirror list                                                                |
| `repo-governance/development/quality/pr-review-disciplines/cost-control-noise-control-mechanics-shared-context-extract-once.md` | EDIT            | generated-path list                                                        |
| `repo-governance/development/quality/pr-review-disciplines/post-cutover-monitoring-rollback-rollback-trigger.md`                | EDIT            | resync instruction                                                         |
| `repo-governance/development/workflow/no-destructive-git-operations/whole-tree-staging-is-forbidden.md`                         | EDIT            | mirror list                                                                |
| `repo-governance/development/workflow/trunk-based-development.md`                                                               | EDIT            | mirror list                                                                |
| `repo-governance/workflows/plan/plan-execution/iron-rules-6-11.md`                                                              | EDIT            | mirror list                                                                |
| `repo-governance/workflows/repo/repo-harness-compatibility-quality-gate/step-1-initial-validation.md`                           | EDIT            | binding-sync no-op diff set                                                |
| `specs/apps/rhino/behavior/rhino-cli/gherkin/governance/governance-word-budget.feature`                                         | EDIT            | example rows use dropped paths                                             |
| `specs/apps/rhino/behavior/rhino-cli/gherkin/harness/README.md`                                                                 | EDIT            | annotated index still says Amazon Q                                        |
| `specs/apps/rhino/behavior/rhino-cli/gherkin/harness/agents-bindings.feature`                                                   | HISTORICAL-KEEP | US-2 purge scenario names the dropped harnesses as the thing proven absent |
| `specs/apps/rhino/behavior/rhino-cli/gherkin/harness/governance-word-budget-thresholds.feature`                                 | EDIT            | `.github/copilot-instructions.md` surface; Phase 11 owns the final list    |
| `specs/apps/rhino/behavior/rhino-cli/gherkin/repo-governance/repo-governance-vendor-audit.feature`                              | HISTORICAL-KEEP | DD-3: scenarios prove the forbidden tokens are still caught                |
| `specs/apps/rhino/behavior/rhino-cli/gherkin/specs/harness-registry-driven.feature`                                             | EDIT            | scenario text still names Amazon Q                                         |

## Phase 3 notes

- **Three `EDIT`-verdict files no explicit P3.x step named** still had to be swept for the gate to
  pass: `specs/.../gherkin/governance/governance-word-budget.feature` (example rows retargeted to
  `.codex/agents/example.md` and `.agents/skills/example/SKILL.md`),
  `specs/.../gherkin/harness/README.md` (index line generalized to "every generated-tier harness
  binding"), and `specs/.../gherkin/specs/harness-registry-driven.feature` (scenario text
  de-vendored, with the matching step string in `apps/rhino-cli/tests/specs_tree.rs` updated in the
  same edit). Lesson: the verdict table, not the step list, is the authority on Phase 3 scope.
- **`docs/reference/platform-bindings.md` had to be edited in Phase 3**, not deferred wholesale to
  Phases 4/10. Its verdict row says "Phase 4 and Phase 10 refine further", but the Phase 3 Gate's
  own clause 2 pathspec includes `docs/reference`, and the catalog listed Cursor as `Active`. The
  Phase 3 edit trims the table to the three registry harnesses and deletes the Amazon Q bridge
  section, the Kiro succession section, and both Cursor translation sections. Phase 4's
  `"never an official"` sentence and Phase 10's generated-region markers are untouched.
- **`repo-config.yml` carried three dead word-budget surface globs** (`.cursor/**/*.md`,
  `.pi/**/*.md`, `.amazonq/**/*.md`) plus two stale comments. P2.6 scoped its sweep to the `gates:`
  section only, so the `word-budget: surfaces:` list survived. Phase 11 rewrites that list wholesale;
  Phase 3 only removed the globs pointing at directories deleted in Phase 2.
- **`md links validate` reports 312 broken links repo-wide, all inside `plans/done/`.** The gate
  clause as written omits the `--exclude plans/done` that `repo-config.yml`'s `md-links` gate
  declares. With the gate's own exclusion the command reports `All links valid!`. Zero broken links
  fall in any path this plan touched. Recorded rather than silently reinterpreted.
- **The worktree had no `node_modules` of its own**, and that broke `nx affected` at
  `organiclever-app-web:codegen` with `TypeError: Cannot read properties of undefined (reading
'AnyKeyword')`. Root cause: `npx @hey-api/openapi-ts` checks `${cwd}/node_modules/.bin` and does
  **not** walk up to the parent checkout's hoisted tree, so it silently fell back to a broken
  package in the global `~/.npm/_npx/` cache. Running `npm install` inside the worktree fixed it.
  Generalizable: a worktree that only ever ran Rust/Nx-cached targets can look healthy for phases
  and then fail on the first TypeScript-touching `affected` run. Same class as
  `project_ose_primer_rhino_cli_propagation_polyglot_provisioning`.
- Phase 3 Gate clause 2 admits verdicts `FALSE-POSITIVE` and "carries the DD-3 forbidden-terms
  rationale". Three `HISTORICAL-KEEP` files under
  `repo-governance/conventions/structure/post-mortems/` still match, because their worked examples
  quote a real `.amazonq/` incident. They do not present a dropped harness as supported, which is
  the clause's stated intent; the verdict vocabulary in the clause is narrower than the table's.

## Parity boundary set

Re-checked 2026-08-19 by reading `apps/rhino-cli/parity-manifest.sha256` in **both** repositories
rather than converging one onto the other.

- `ose-private` on `main` at `6949b4040`, clean, no worktree, identical to `origin/main`.
- Boundary size: 579 paths in `ose-private`, 574 in this branch.
- The difference is exactly the five paths this plan deleted, all present only in `ose-private`:
  - `apps/rhino-cli/src/application/agents/cursor.rs`
  - `apps/rhino-cli/src/commands/harness_emit_bindings.rs`
  - `apps/rhino-cli/tests/cursor_binding.rs`
  - `specs/apps/rhino/behavior/rhino-cli/gherkin/cursor-binding/cursor-binding.feature`
  - `specs/apps/rhino/behavior/rhino-cli/gherkin/cursor-binding/README.md`
- No path exists only in `ose-public`. The boundary is otherwise byte-for-byte the same set, so the
  cross-repo obligation is a straight replay of this branch's `apps/rhino-cli/**` and
  `specs/apps/rhino/**` changes, with no `ose-private`-only file to reconcile in the other direction.

## Phase 4 notes

- The Codex defect was a **validator inversion, not an omission**. `validate_no_codex_agents_dir`
  actively failed when `.codex/agents/` existed, on the false premise that the directory was never a
  Codex convention. It is now `validate_codex_agents_dir`: the directory is permitted, and only a
  file whose extension is not `.toml` is a finding — reported by name. Falsifiability proved both
  ways on the real tree: `.codex/agents/probe.md` → exit 1, `.codex/agents/probe.toml` → exit 0,
  directory removed → exit 0.
- Two constants (`CODEX_AGENT_DIR`, `CODEX_AGENT_EXTENSION`) and one predicate
  (`is_rejected_codex_agent_filename`) now carry the rule, all in `bindings.rs`. No other source
  file in `apps/rhino-cli/src/` hard-codes `.codex/agents`, so Phase 5's emitter has one place to
  import from.
- A pre-existing test named the old belief in its own name
  (`validate_fails_when_codex_agents_dir_exists`). Renaming it to
  `validate_permits_an_empty_codex_agents_dir` was part of the fix, not a cosmetic follow-up — a
  test whose name asserts the wrong rule outlives the code that implemented it.

## CI flake — beavernest-be DatabaseConfigurationTests

`.NET quality gate` failed on PR #232 at `beavernest-be:test:coverage` with
`DatabaseConfigurationTests.database configuration refuses empty, root, home, repository, and
nonpositive timeout values` — `Assert.True() Failure, Expected: True, Actual: False`
(`apps/beavernest-be/tests/unit/Tests/DatabaseConfigurationTests.fs:30`).

Evidence it is not caused by this branch:

- This branch touches **no** file under `apps/beavernest-be/`. It is pulled into `nx affected` only
  because `repo-config.yml` and `AGENTS.md` are global Nx inputs.
- `beavernest-be:test:unit` passed **104/104** seconds earlier **in the same job**, on the same
  binary; `test:coverage` then failed 1/104. Same code, two results.
- The identical job passed on the previous CI run of this branch.
- `npx nx run beavernest-be:test:coverage --skip-nx-cache` passes locally.

The failing assertion iterates seven invalid inputs, three of which are computed from the
environment (`Path.GetPathRoot(Path.GetTempPath())`,
`Environment.GetFolderPath(SpecialFolder.UserProfile)`, `Directory.GetCurrentDirectory()`) and
compared against values `isDisallowedDirectory` recomputes the same way. The list does not report
which element failed, so the log cannot narrow it further — that missing detail is itself the defect
worth fixing. Routed to Knowledge Capture as a follow-up rather than fixed inline: fixing an
unrelated app's test inside this plan would violate the "do NOT bundle unrelated fixes" rule.

## Phase 5 notes

- The `gherkin/harness/` directory is run wholesale by `tests/agents.rs`, so a second cucumber
  runner over the same directory would meet the other's undefined steps and fail under
  `fail_on_skipped`. Both runners now filter on the feature-level `@codex-binding` tag via
  `filter_run_and_exit` — `codex_binding.rs` takes the tagged features, `agents.rs` takes the rest.
  The deleted Cursor binding avoided this by owning its own spec folder; the plan's checklist places
  the Codex feature in `gherkin/harness/`, so the tag split is what makes both hold.
- The P5.4 RED step could not be made to fail. Agent identity already comes from the `name`
  frontmatter key because `converter::discover_agent_sources` — shared with the OpenCode mirror —
  resolves it there. The scenario was written with `name:` deliberately disagreeing with both the
  filename stem and the role subfolder, and it passed on its first run with no production change.
  Recorded rather than manufactured: writing a deliberately path-keyed emitter first, only to
  replace it, would have been scaffolding, not a test.
- `.codex/config.toml` is deliberately absent from `expected_bindings`. Only its delimited region is
  emitter-owned, so whole-file byte parity would fail on the hand-maintained
  `[mcp_servers.nx-mcp]`, `[features]`, and `[agents.ci-monitor-subagent]` tables. A separate
  `validate_codex_config_region` check compares just the region, and was proved falsifiable both
  ways (renaming one generated table exits 1; `git checkout -- .codex/` exits 0).
- The validator resolves each agent's description through `plan_codex_agents`, which shares
  `convert_codex_agent_inner` with the emit path. A first draft hand-rolled a second frontmatter
  reader in `bindings.rs`; that would have drifted the moment a description was quoted or carried a
  colon.
- `harness_generate_bindings.rs`'s existing `run(...)` smoke tests resolve the git root from the
  process CWD, so they are only as isolated as the whole test binary. Adding two more of them made
  `harness_unknown_name_is_error` fail once under parallel execution and pass in isolation; the two
  new tests were removed rather than left as a flake source. Filed as a candidate learning for
  Knowledge Capture.
- `specs behavior-coverage validate` treats a second `#[then]` alias with no matching Gherkin step
  as an orphan step implementation. Convenience aliases on a step definition are a gate failure
  here, not dead code.

## Phase 5 gate evidence

- `npx nx run rhino-cli:test:quick` — exits 0.
- `git ls-files .codex | grep -c .` — 95 (2 at baseline).
- `git grep -c "ci-monitor-subagent" .codex/config.toml` — 2.
- `npm run generate:bindings && git diff --quiet .codex/` — exits 0 (idempotent).
- `harness bindings validate` — 198 checks, 0 failed; exits 1 after
  `printf 'x' >> .codex/agents/agent-maker.toml`, exits 0 again after `git checkout -- .codex/`.
- `npx nx affected -t typecheck,lint,test:quick` — exits 0 across 28 projects.
- `governance word-budget validate` — exits 0 (TOML is outside the markdown surface, as planned).
- `governance readme-index validate` at both gate scopings — exits 0.

## Vendored .agents baseline

Captured before any `.agents/` emitter existed (Phase 6a). 24 tracked files across the eight
vendored plugin skill directories; none has a `.claude/skills/` counterpart, so none can be
regenerated (DD-7).

```text
cabf9d48a0d8d7bb3c7de5306bf9208dfec8fb7d3e50d5b43264d22abaaecd8c  .agents/skills/cavecrew/SKILL.md
e026b0fbaf28a84db086d76664050baffa9886018477f740edbc317f14c433a8  .agents/skills/caveman-commit/SKILL.md
cf876eb5972a4cc44a4eaea0889b221ea373081d521c8591fac50b054530978e  .agents/skills/caveman-compress/README.md
ac3432493cfe71368a141f437bf35562eb8f4ce07ae699e5399c0cb665e02da3  .agents/skills/caveman-compress/SECURITY.md
d45b4cb20815db99234f8b39b8323b8a1521b7f060ba628c3f2d444122faa5e4  .agents/skills/caveman-compress/SKILL.md
429c3e1c5cc5b9705f28d77f303c728304ae68693913ad3d5ce9b5a44c8ee40f  .agents/skills/caveman-compress/scripts/__init__.py
6d8b7d7846a845059d7a3107143f11131f63c5511d669b44085b15ec5e3d2279  .agents/skills/caveman-compress/scripts/__main__.py
877793ffc2cba946deb748097a137a9c810ac35fd01ec2be3c92aef3ba96ebbd  .agents/skills/caveman-compress/scripts/benchmark.py
caa8a8620990f15cbe4d4f5d4a43d33d7b136aac1c5a0f3e696444d5e151451d  .agents/skills/caveman-compress/scripts/cli.py
f7380666f19a869e0bf49d895fa8fe5ecfc3fa87e6b3ae3902191c8d61f02b6c  .agents/skills/caveman-compress/scripts/compress.py
568aff4b04f5b17ab3870a24b55546bc2020faa450d6e923af4390aa8d3f59ee  .agents/skills/caveman-compress/scripts/detect.py
4f0de7965297e1977f93007ad20fa79ce4792a2077400a7b1bb0786b589dfc63  .agents/skills/caveman-compress/scripts/validate.py
2706cba96d6989ba5ef60bd8352e83aae0a84fcae72d220447c41f1719d1f1fa  .agents/skills/caveman-help/SKILL.md
73b4c3c7d7c74dfd9070c011742c47abc27fedd7f4997800dacf2e6ffae84167  .agents/skills/caveman-review/SKILL.md
b9e49e46ede956e0c1633eae82a695c996f728bc48f3903f001d301068a2b0ea  .agents/skills/caveman-stats/SKILL.md
8ecb0d04872bfef578e767b9b7d3c0a3ec4ca7bbbda536ddc0627e2023c734cf  .agents/skills/caveman/SKILL.md
18230a1cb812741e46a53c195652f57d0ac376de87794464a4f6368735aa950e  .agents/skills/compress/SKILL.md
429c3e1c5cc5b9705f28d77f303c728304ae68693913ad3d5ce9b5a44c8ee40f  .agents/skills/compress/scripts/__init__.py
6d8b7d7846a845059d7a3107143f11131f63c5511d669b44085b15ec5e3d2279  .agents/skills/compress/scripts/__main__.py
877793ffc2cba946deb748097a137a9c810ac35fd01ec2be3c92aef3ba96ebbd  .agents/skills/compress/scripts/benchmark.py
caa8a8620990f15cbe4d4f5d4a43d33d7b136aac1c5a0f3e696444d5e151451d  .agents/skills/compress/scripts/cli.py
f7380666f19a869e0bf49d895fa8fe5ecfc3fa87e6b3ae3902191c8d61f02b6c  .agents/skills/compress/scripts/compress.py
568aff4b04f5b17ab3870a24b55546bc2020faa450d6e923af4390aa8d3f59ee  .agents/skills/compress/scripts/detect.py
4f0de7965297e1977f93007ad20fa79ce4792a2077400a7b1bb0786b589dfc63  .agents/skills/compress/scripts/validate.py
```

Counterpart probe — `for d in cavecrew caveman caveman-commit caveman-compress caveman-help
caveman-review caveman-stats compress; do test -d ".claude/skills/$d" && echo "COUNTERPART $d"; done`
— printed only `done`, with no `COUNTERPART` line.

## Phase 6 blockers — CI infra, NOT this branch

Two consecutive `beavernest-app-test-local-deploy-stag` E2E jobs (runs `32231836567`, job
`96013835006`) were cancelled at their 35-minute `timeout-minutes` while still inside
`./.github/actions/setup-playwright`. Proof of the exact step, from the job's own teardown rather
than inference: `Complete job` printed `Terminate orphan process: pid (4377) (npm exec playwright
install-deps)`. That is the **cache-hit** branch of `.github/actions/setup-playwright/action.yml`,
which shells out to `apt-get update` against `azure.archive.ubuntu.com`. The earlier run showed the
same signature with repeated `Ign:` lines and 32 minutes of silence.

Two separate Phase 12 backlog candidates, neither fixed inline (would bundle unrelated fixes):

1. **`repo-config.yml` in an app workflow's `pull_request.paths:` filter.** It is the only
   PR-changed file matching that filter, so every governance-only edit drags a full BE+FE E2E run.
   Same class as `repo-config.yml`/`AGENTS.md` behaving as global Nx inputs.
2. **`setup-playwright` has no apt retry or per-step timeout guard.** One mirror stall consumes the
   whole 35-minute job budget and surfaces as a generic cancellation with no actionable message.

Phase 6 proceeds: the failing job exercises no code path this branch touches, and the merge gate is
not due until the terminal section.

## Phase 6 notes

- **6.12 Prettier round trip: exit 0, zero files modified.** No `.prettierignore` entry is needed.
  The repo's only Prettier surface is `**/*.md` (`format:md`), the mirrored `.md` files are byte
  copies of an already-formatted source, and both trees share one config — so the mirror is
  Prettier-clean by construction. The vendored `.py` files are never in scope. Measured BEFORE
  wiring any guard, per DD-9.
- **6.13 implemented in `validate_skills_mirror`, not `expected_bindings`.** `BindingFile.content`
  is a `String`; routing 545 mirror files (including vendored `.py`) through it would require
  `from_utf8_lossy` and produce false failures on any non-UTF-8 byte. The mirror check compares raw
  bytes instead, and reuses the emitter's own diff so "what the mirror should hold" is decided in
  exactly one place. Acceptance met verbatim: exits 0, exits 1 naming the tampered file, exits 0
  after restore.
- **6.14 needed a real fix, not just a check.** `npm run validate:sync` runs `harness sync validate`,
  which covered only the OpenCode mirror and did NOT report `.agents/`. Moved the mirror check into
  `validate_sync` so both entry points report it from one implementation; `harness bindings validate`
  picks it up transitively. No new flag, no `package.json` change (`git diff --stat package.json`
  empty), check count 96 → 97 and 198 → 199.
- **The mirror exposed a pre-existing defect class: 47 dangling links across 22 skill files.**
  `docs/links.rs` exempted skill files from link validation, but keyed the rule on the literal
  `.claude/skills/`. The byte-identical mirror at `.agents/skills/` fell outside it, so the same
  bytes were reported as both broken and fine. Fixed at root cause by making the exemption a
  property of skill files as a class (`SKILL_TREE_MARKERS`), covering both trees, with a test that
  is falsifiable both ways — the same dangling link outside a skill tree is still reported.
  Repo-wide count returned to exactly the 312 baseline, so no coverage was weakened.
  **Backlog candidate (Phase 12, NOT fixed here):** those 47 anchors are genuinely dangling in the
  `.claude/skills/` sources — several point at split-pattern parents that no longer carry the
  heading. They were invisible for as long as the exemption existed. Fixing them is real work on
  unrelated content and does not belong in this PR.
- **6.20 acceptance needs a post-commit re-read.** `git status --porcelain .opencode/` reports 17
  while the `git rm` is staged-but-uncommitted; every one is a `D` entry. The check that actually
  matters — nothing _recreated_ — is 0 non-`D` entries after `npm run generate:bindings`, which is
  what was verified. Re-confirmed as 0 after the Phase 6 commit.

### Phase 6 commit split (recorded post-commit)

Three code commits plus one plan-docs commit:

1. `fix(rhino-cli): exempt every skill tree from link validation` — the `links.rs` root-cause fix.
2. `feat(rhino-cli): mirror .claude/skills into .agents/skills as real files` — emitter, validator,
   registry fields, Gherkin, the 545-file mirror, and the refreshed parity manifest.
3. `chore(harness)!: delete the ungoverned .opencode skill and command trees` — 17 deletions plus
   the accepted-capability-loss record.

`repo-config.yml` carries changes belonging to both commit 2 (the `skills-mirrors`/`vendored`
declarations) and commit 3 (the removed word-budget excludes). A single file cannot straddle two
commits, so it landed whole in commit 2.

`rhino-cli parity manifest generate` refuses to run while any parity-boundary file differs from the
Git index. The boundary is wider than `apps/rhino-cli/src`: it also covers
`specs/apps/rhino/behavior/rhino-cli/gherkin/harness/README.md`. Stage the whole boundary before
generating.

6.20 re-confirmed after the commit: `git status --porcelain -uall .opencode` returns 0 lines, and
`git ls-files .opencode/skills .opencode/commands` returns 0 — the pre-commit binding regeneration
did not resurrect either tree.

## Phase 7 notes

**7.14 — the check that would have caught `.opencode/skills/` the day it appeared.**
Run against the real repository with the release binary:

| Step                                                      | Command                      | Exit                                        |
| --------------------------------------------------------- | ---------------------------- | ------------------------------------------- |
| baseline                                                  | `harness ownership validate` | 0                                           |
| probe present (`git add .opencode/skills/probe/SKILL.md`) | `harness ownership validate` | 1, naming `.opencode/skills/probe/SKILL.md` |
| probe removed (`git rm -f`)                               | `harness ownership validate` | 0                                           |

`git status --porcelain -uall .opencode` returns 0 afterwards, so the probe left nothing behind.

**7.15 — each class is enforced independently.**

| Probe                                                                | Command                      | Exit                                                                                                                      | Why                                                                              |
| -------------------------------------------------------------------- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| (a) GENERATED edit — `.opencode/agents/agent-maker.md`               | `harness ownership validate` | 1, `❌ Agent: agent-maker`                                                                                                | a generated file must reproduce byte-for-byte                                    |
| (b) VENDORED edit — `.agents/skills/caveman/SKILL.md`                | `harness ownership validate` | 0, file still present                                                                                                     | a vendored path has no in-repo source to compare against, and nothing deletes it |
| (c) SOURCE target — `.opencode/agents` temporarily declared `source` | `harness bindings generate`  | 1, `refusing to generate: harness "opencode" would write to ".opencode/agents", which ".opencode/agents" declares source` | the emitter refuses before the first write                                       |

Each probe was restored (`git checkout --` / config restored from a backup) and the validator
re-run at exit 0 before the next probe.

**A generated-class probe must target an emitted file, not any file in the mirror.** The first
attempt at (a) edited `.opencode/agents/README.md` and the validator exited **0** — correctly, since
the README is not one of the byte-guarded agent mirrors. A probe that picks `git ls-files <dir> |
head -1` can therefore certify nothing while looking like a pass. Same false-zero class as the
benchmark-harness case: assert the probe changed the thing the check actually guards.

**US-8's Gherkin splits across two feature files.** Four scenarios exercise
`harness ownership validate` and live in `harness/harness-ownership.feature`; the fifth asserts that
there is no fourth class and no reason-less vendored declaration, which is a `repo-config validate`
claim, so it lives in `repo-config-validate/repo-config-validate.feature` beside the other schema
scenarios. Each runner then keeps exactly one step-definition set.

**The per-class count line prints only under `--verbose`.** The default text reporter emits the
pass/fail tally alone, so an acceptance clause that greps for the class counts must pass
`--verbose` or it reads as a missing line rather than a passing check.

**7.18 — the path-gated declaration was observed firing, in both directions.** Run in an isolated
no-origin git fixture whose gate registry contains only `harness-ownership`, triggered on `.codex/`:

| Staged change        | Output                             | Exit                                        |
| -------------------- | ---------------------------------- | ------------------------------------------- |
| `.codex/config.toml` | `Running gate harness-ownership`   | 1 (the fixture has no bindings to validate) |
| `README.md` only     | no `harness-ownership` line at all | 0                                           |

The full-registry fixture aborts at the first failing gate (`test-quick`, which cannot run outside
an Nx workspace), so the registry has to be reduced to the gate under test before the line can be
observed. A `path-gated` declaration that is never exercised is indistinguishable from a passing one.

**A `--help`-shaped exit code is not the command's exit code.** `repo-governance word-budget
validate` does not exist — the command is `governance word-budget validate` — and clap's
unrecognized-subcommand error exits **2**, which reads exactly like a validator failure. Confirm the
subcommand exists before treating its exit code as a verdict.

**The word budget counts YAML frontmatter.** `ownership-classes.md` measured 414 words with `wc -w`
before its frontmatter block was added and 505 after — over the 500-word FAIL limit — while the body
never changed. A new governance file that looks comfortably inside the budget by body length can
still fail once the required `title`/`description`/`when_to_use`/`tags` block is prepended. Measure
with `governance word-budget validate`, not `wc -w`, and measure after the frontmatter exists.

## Phase 8 notes

**Splitting one feature directory across N cucumber runners needs ONE shared exclusion list.** Phase
7 added `tests/harness_ownership.rs` as the fifth runner over the same `harness/` directory but never
added `binding-ownership` to the exclusion list in `tests/agents.rs`, so `agents.rs` picked the
feature up with none of its steps defined and `.fail_on_skipped()` turned that into five failures.
The defect is structural, not a typo: with one `const` per foreign runner, adding a runner means
editing every sibling, and forgetting one is invisible because the new runner itself passes. Fixed by
collapsing every per-runner constant in `agents.rs` into a single `FOREIGN_TAGS` list with a
tag-to-runner table in the doc comment, so the next runner is one line in one place.

**Timestamps were never an option, and the guard says so in code.** Divergence is decided by content:
`git show HEAD:<path>` against the working bytes, with `HEAD` as the shared reference both sides are
measured from. A path absent from `HEAD` counts as differing. The prohibition is executable —
`git grep -nE "\.modified\(\)|SystemTime|mtime"` over `triage.rs` must exit 1 — because a comment
saying "do not use mtime" is not falsifiable and a fresh clone would otherwise report all 732
generated files as diverged.

**Verbatim body promotion corrupts relative links.** The emitter flattens `.claude/agents/<role>/x.md`
into `.opencode/agents/x.md` and rewrites `../../../` to `../../` on the way. Promoting a mirror body
back verbatim therefore writes the shallower depth into a deeper canonical file, and every link in
the promoted agent silently points one directory too high. `rebase_links_to_canonical` inverts both
shapes — bare-filename agent links resolved through a unique `name` lookup, every other link through
a pure depth change — and the resulting diff was exactly the hand edit and nothing else. Any
mirror→source promotion across a path-shape change needs the emitter's transform run backwards, not
skipped.

**The both-diverged HARD STOP, verbatim** (P8 Gate item 4). Captured by appending a comment to
both `.claude/agents/general/agent-maker.md` and `.opencode/agents/agent-maker.md`, then running
`harness sync triage`, which exited 1. The failure marker each finding opens with is U+2718,
transcribed here as `[x]` because no tracked markdown in this repository carries that codepoint and
`convention emoji validate` scans every file type in CI:

```text
harness sync triage: 732 generated file(s) compared, 2 divergence(s)
[x] .codex/agents/agent-maker.toml — the canonical source is ahead of this mirror
    canonical source: .claude/agents/general/agent-maker.md
    regenerate:       rhino-cli harness bindings generate
[x] .opencode/agents/agent-maker.md — HARD STOP: both sides were hand-edited
    canonical source: .claude/agents/general/agent-maker.md
    Both files carry edits this tool cannot reconcile. No automatic
    resolution exists and none is offered. Reconcile them by hand,
    then re-run.
Error: 2 divergence(s), at least one with edits on BOTH sides — reconcile by hand
```

The single canonical edit shows up twice because two mirrors derive from it: `.codex` is
canonical-ahead, `.opencode` is both-diverged. The one-sided formatters each offer exactly one route
(mirror-side offers promote, canonical-side offers generate and never promote); the both-diverged
formatter offers neither, which is the point.

**The failure marker cannot be a literal glyph in Rust source.** `convention emoji validate` scans
`*.rs` at pre-commit and killed the first attempt at this commit over five U+2718 codepoints. The
repository's existing convention is the escape form — `reporter.rs` writes `\u{274C}` — which keeps
the source bytes ASCII while the rendered output is unchanged. A prose comment that merely mentions
the character trips it too; reword the comment rather than escaping it.

**Promotion cannot silently overwrite, by construction** (Gate item 5). `harness sync promote` prints
a unified diff and ends with `Nothing was written.`; `git diff --quiet .claude/` exits 0 immediately
afterwards. The at-risk list is not a safety net bolted on top — the canonical file's own frontmatter
is the base being edited, with only `description` and body substituted, so a field the editing
harness never carried (`permissionMode`, `isolation`) is never in a position to be dropped. The list
tells the reviewer which fields the mirror could not have represented.

**Vendored versus generated, observed** (Gate item 6). Editing vendored
`.agents/skills/caveman/SKILL.md` yields 0 divergences; editing generated `.agents/skills/README.md`
yields 1. Triage is scoped to the `generated` class only (DD-12) by filtering `classify()`, so the
Phase 7 ownership declarations are what makes Phase 8 correct — a vendored payload reported as
diverged would be a false alarm on a file with no source to regenerate from.

**Deviation from 8.3 as written.** The task asked that triage and `harness bindings validate` share
one generation path. Implemented instead as: `harness bindings generate` and triage both call
`application::agents::emit::emit()`. Routing `bindings validate` through scratch regeneration would
replace a fast byte comparison against committed content with a full tree copy plus a full emitter
run on every validation, including in the pre-push hook. The anti-drift property the task wanted —
no second, separately-maintained emitter path — is delivered by both writers invoking identical
emitters; `validate` remains a reader.

**The branch carries a deliberate pre-existing RED.** `cargo test --release` fails two
`governance-word-budget.feature` Examples rows (`.codex/agents/example.md`,
`.agents/skills/example/SKILL.md`), landed in Phase 3 commit `95a131551` as the standing RED that
Phase 11 turns green. The phase gate is `nx run rhino-cli:test:quick`, which exits 0. Reading the
full suite as the gate would read a planned RED as a regression.

**Two golden-master fixtures track the subcommand list.** Adding `triage` and `promote` changed
`harness-help.stderr` and `harness-sync.stderr`; regeneration is driven from `manifest.json`, whose
keys are `file` and `args`. A new subcommand is never a code-only change.

## Ideas-tree verdicts

Sweep command and set: `git grep -ilE "\.cursor/|\.amazonq/|\.pi/|\.kiro/|Amazon Q|Antigravity|Windsurf|Junie|Aider" -- plans/ideas`
→ `local-tmp/harness-ideas-sweep.txt`, **10 paths**. One verdict per path, no exceptions.

| Path                                             | Verdict        | What changed                                                                                                                                                               |
| ------------------------------------------------ | -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| `plans/ideas/README.md`                          | NARROWED       | four one-liners rewritten to match their briefs' new scope; two new briefs inserted alphabetically                                                                         |
| `q2/extend-byte-identity-to-claude-hooks.md`     | NARROWED       | out-of-scope list named `.amazonq/`/`.cursor/` mirrors; retargeted to the surviving three. Hook byte-identity premise untouched                                            |
| `q2/governance-command-name-reconciliation.md`   | NARROWED       | same shape — `.cursor/` in the regenerate-in-same-commit sentence. Command-name premise untouched                                                                          |
| `q2/governance-path-ownership-registry.md`       | NARROWED       | zero-owner path 2 (`.cursor/**`) deleted; Rule 8 delivers this brief's proposal for binding trees. Four wider zero-owner paths survive                                     |
| `q2/harness-binding-catalog-drift.md`            | NARROWED       | Windsurf/Devin and Copilot moot; Codex finding fixed in Phase 4; OpenCode prose fixed in Phase 9. Only the read-the-body-not-the-summary lesson survives                   |
| `q2/harness-converter-preserve-agent-mode.md`    | NARROWED       | Amazon Q and Cursor tiers gone; the dropped-field risk now spans OpenCode **and** Codex, so the brief widened rather than shrank                                           |
| `q2/harness-level-env-file-enforcement-gap.md`   | NARROWED       | retitled; Cursor/Amazon Q halves moot, Codex half survives, OpenCode joins it — the original excused OpenCode on an unrelated ground                                       |
| `q2/ose-private-opencode-ci-monitor-orphan.md`   | NARROWED       | dropped mirrors and the deleted `.opencode/commands                                                                                                                        | skills` counter-examples corrected; ose-public solved the Codex sibling by declaring it vendored |
| `q2/refresh-agent-illustrative-example-paths.md` | NARROWED       | the ~183-hit count is stale across a changed mirror set — recount before acting                                                                                            |
| `q2/vendor-audit-kiro-term.md`                   | FALSE-POSITIVE | matched on the very terms it exists to catch. DD-3 keeps dropped-harness tokens in the scanner deliberately — the scanner guards vendor-neutral prose, not the binding set |

**A term-based sweep matches the brief that exists to catch those terms.** `vendor-audit-kiro-term`
is a false positive by construction: any pattern broad enough to find briefs _about_ dropped
harnesses also finds the brief about _detecting mentions of_ dropped harnesses. Worth expecting
rather than re-deriving — the sweep is a candidate list, and the verdict column is where the
judgement lives.

## Phase 9 notes

**P9.1 was already satisfied before Phase 9 started.** The `sst/opencode` → `anomalyco/opencode`
citation was corrected during the Phase 3 prose sweep, so the acceptance criterion "returns nothing
after the edit, where it returned at least one match before" had no before-state left to observe.
Falsifiability was proven instead by injecting a probe file, confirming the search returns a match,
removing it, and confirming exit 1. Class fix, no per-site edit needed.

**The acceptance clause as written can never pass.** `git grep -c "sst/opencode" -- . ':!worktrees'
':!node_modules' ':!plans/done'` includes this plan's own `delivery.md`, which contains the search
string twice as literal command text, and `README.md`, which narrates the move. Any plan whose
acceptance criterion greps for a token it also documents needs `':!<its own folder>'` in the
pathspec, or the gate is unsatisfiable by construction. Recorded as a deviation: the verified form
excludes `plans/in-progress/update-harness-support`.

**Writing a narrowing note reintroduces the token you swept for.** The first draft of the
catalog-drift narrowing spelled the old organization path to explain the correction, which put the
match straight back. Re-run the sweep command **after** writing the note, not only before.

**Three stale converter paths, found while editing the neighbouring line.** The catalog cited
`apps/rhino-cli/src/internal/agents/converter.rs` for `convert_color`, `convert_model`, and
`convert_permission`; that directory does not exist and the file lives under `application/`. No
validator covers a prose file path, which is exactly the gap
[doc-command-existence-validation](../../ideas/q2-not-urgent-important/doc-command-existence-validation.md)
describes for commands.

**Bash tool edits trip `guard-env-file-access` on content, not just targets.** A `python3` heredoc
rewriting an ideas brief was blocked because the _text being written_ contained the restricted-tier
filenames. The file under edit was a markdown brief, not an env file. Use the Edit tool for prose
that quotes those names; the guard reads the command string.

## Phase 10 notes

**The emitter is Prettier-stable; DD-9 needed no remedy.** The measurement: generate, hash, run
`prettier --write`, hash again — both `aaf28c31...`. Prettier's markdown table rule is per-column
padding to the widest cell measured in **characters**, and the emitter reproduces it. This was
verifiable in advance, because `prettier --check docs/reference/platform-bindings.md` already
exited 0 before the phase started: whatever padding the file carried was Prettier-canonical, so
matching the existing table byte-for-byte was the same thing as matching Prettier. That also ruled
out the plan's second remedy — the document is ~300 lines of hand-authored prose Prettier keeps
formatted, and a `.prettierignore` entry to accommodate one generated region would unformat all
of it.

**The plan's DD-9 command cannot answer the DD-9 question in this phase.** The stated form is
`generate && prettier --write && git diff --quiet <file>`, but `git diff --quiet` compares against
HEAD, and HEAD does not yet carry the region markers this phase introduces. It exits 1 for a
reason that has nothing to do with Prettier. Recorded as a deviation: the question "does Prettier
alter what the emitter produced" is a before/after hash of the same working file, which is what
was measured.

**Transcribe cells verbatim before changing any of them.** The registry was populated with the
existing table's exact cell text — footnote references (`[^mcp]`, `[^agents]`, `[^skills]`), inline
code spans, `**and**` — so the first generated output diffs to nothing but the two marker lines.
Had a content correction been folded into the same step, a non-empty diff would not have
distinguished "the emitter is wrong" from "the content changed". Content changes are now
individually visible.

**A "last table row" scan found a table 230 lines away.** The first marker-insertion script walked
forward from the verification stamp to the last line starting with `|` — which is in a different
table near the end of the document, so the end marker landed at line 262 and would have swallowed
half the file. The fix is to stop at the end of the **contiguous** block, and to assert its size
(`header + separator + 3 rows`) rather than trust the walk. Same class as the wrapped-checklist and
repeated-heading defects already recorded: a scan that does not assert its own extent.

**Footnote definitions must stay outside the region, references inside.** Cells carry `[^mcp]`;
the `[^mcp]:` definition block is hand-authored prose below the end marker. The cucumber fixture
encodes this — its `PROSE_AFTER` holds a footnote definition, and the byte-identity step asserts
that specific line survives, so a whole-file rewrite fails on a named assertion rather than only
on an aggregate comparison.

**The verification stamp has no per-harness home.** The plan lists seven `catalog:` fields, all
per-harness, but puts the stamp inside the generated region. Three harness entries cannot own one
document-level date without being able to disagree. Recorded as a deviation: a sibling top-level
`harness-catalog:` block declares `document:` and `verified:`. The date is declared, never stamped
at generation time — a generated timestamp would change on every run and make the drift guard fire
on its own output, which is the Phase 8 timestamp prohibition applied to a second emitter.

**`harness audit` named no member on the passing path.** P10.7's acceptance is that the audit
output names the catalog check, but the per-validator reporters print only failures at the audit's
verbosity, so a passing audit listed nothing it had run. Added a `harness audit: <name>` line per
member. This was a pre-existing gap for all five prior members, not a catalog-specific one.

**The aggregate audit is not the enforcement path.** Gates invoke `harness bindings validate` and
`harness ownership validate` as their own `command:` entries; nothing invokes `harness audit`. So
wiring `validate-catalog` into the audit gives it aggregate coverage but **no CI enforcement** —
see the open question below.

**Addition beyond the Phase 10 checklist: a `harness-catalog` gate.** The checklist stops at
wiring `validate-catalog` into `harness audit`, but nothing invokes `harness audit` — the gate
registry calls validators directly by `command:`. Without a gate entry the drift guard would run
only when someone typed it, which does not deliver US-5's claim that the document and the registry
"cannot disagree". Declared path-gated on `repo-config.yml` and
`docs/reference/platform-bindings.md` — the only two inputs its verdict depends on — mirroring the
P7.17 precedent exactly. `gate validate` and `repo-config validate` both exit 0, the gate lists on
both `ci` and `pre-push`, and the command exits 1 under the hand-edit probe and 0 after
regeneration. Flag for review: this is a governance-surface change the checklist did not ask for.

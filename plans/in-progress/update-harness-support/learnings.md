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

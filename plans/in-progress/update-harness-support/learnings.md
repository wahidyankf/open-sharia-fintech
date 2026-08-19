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
  dropped harness. In both cases the test/scenario proving the *absence* of support is the more
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

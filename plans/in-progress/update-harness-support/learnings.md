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

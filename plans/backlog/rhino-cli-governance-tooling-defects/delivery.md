# Delivery — rhino-cli Governance Tooling Defects

**Delivery Mode**: `worktree-to-pr` (mandatory — this plan changes executable code).

**Worktree**: one per repository. `ose-public/worktrees/rhino-cli-tooling-defects/` on branch
`worktree/rhino-cli-tooling-defects`; the `ose-private` mirror is provisioned only when Phase 4
starts. Phase 0 opens no PR.

**Delivery boundaries**: three. Each workstream is independently shippable, so each opens its own PR
at its phase's end. Phase 4 (parity) rides the last one.

**Executor legend**: `[AI]` — an agent performs it. `[HUMAN]` — requires a person.

## Phase 0: Baseline

_Suggested executor:_ `repo-setup-manager`

- [ ] [AI] Provision the `ose-public` worktree and branch — acceptance: `git worktree list` shows it
      and `git status --short` is empty.
- [ ] [AI] Run `npm install` and `npm run doctor -- --fix` — acceptance: both exit 0.
- [ ] [AI] Run `npx nx run rhino-cli:test:quick` and record the pass count — acceptance: exits 0; the
      count is written to `local-tmp/rhino-cli-tooling-defects/baseline.md`.
- [ ] [AI] Capture the vendor audit's **full** current finding set over `repo-governance/` to
      `local-tmp/rhino-cli-tooling-defects/vendor-baseline.txt` — acceptance: the file is non-empty
      or explicitly records `0 findings`, and its finding count is stated.
- [ ] [AI] Enumerate every caller of `readme-index rewrite-paths` (registry gates, husky hooks, CI
      matrix, npm scripts, plan scripts) — acceptance: a list with a per-caller verdict on whether a
      non-zero exit on a fully-dead map would break it.

### Phase 0 Gate

- [ ] [AI] `npx nx run rhino-cli:test:quick` exits 0.
- [ ] [AI] The vendor baseline file exists and its finding count is recorded.
- [ ] [AI] The caller enumeration exists and names at least the gate registry and the hook shims,
      or states that neither invokes the command.

> **Pause Safety**: nothing is modified. Safe to stop. To resume: re-read the baseline files.

## Phase 1: WS-1 — Vendor audit pairs spans across line wraps

_Suggested executor:_ `swe-rust-dev`

- [ ] [AI] Add the three `prd.md` vendor-audit scenarios to
      `specs/apps/rhino/behavior/rhino-cli/gherkin/` — acceptance: `specs structure validate` exits 0.
- [ ] [AI] RED: a unit test where a code span straddles a line break and a later fenced term is
      reported — acceptance: the test fails, and its failure message names the falsely-reported term.
- [ ] [AI] GREEN: strip inline spans at document level with an open-span carry and equal-length
      backtick-run pairing — acceptance: the RED test passes.
- [ ] [AI] RED: a unit test asserting a span replacement preserves byte length so reported line
      numbers do not shift — acceptance: fails before the offset-preserving replacement, passes after.
- [ ] [AI] REFACTOR: fenced-block extraction and inline-span stripping share one scanner — acceptance:
      `npx nx run rhino-cli:lint` exits 0 with no new `clippy` allow.
- [ ] [AI] Diff the post-fix finding set against `vendor-baseline.txt` — acceptance: every difference
      is a **removed** finding explainable by a mis-pair, recorded line by line. Any added finding, or
      any removal that cannot be explained, blocks the phase.
- [ ] [AI] Regenerate and stage the parity checksum manifest — acceptance: `parity manifest validate`
      exits 0.

### Phase 1 Gate

- [ ] [AI] `npx nx run rhino-cli:test` and `npx nx run rhino-cli:lint` both exit 0.
- [ ] [AI] `repo-governance vendor validate` exits 0 on both `AGENTS.md` and the corpus.
- [ ] [AI] The finding-set diff is recorded with a per-line explanation.
- [ ] [AI] A fixture file with a deliberately wrapped code span produces the same finding set as the
      same file with the span rejoined.
- [ ] [HUMAN] Open the WS-1 PR; merge once `pr-quality-gate.yml` is green and the review cycle closes.

> **Pause Safety**: WS-1 is independently shippable. Safe to stop after the merge.

## Phase 2: WS-2 — `harness bindings validate` reads the registry

_Suggested executor:_ `swe-rust-dev`

- [ ] [AI] Add the three `prd.md` harness scenarios to the Gherkin tree — acceptance:
      `specs structure validate` exits 0.
- [ ] [AI] Recreate the synthetic-repo fixture whose primary tier lives at `.custom-src/agents` —
      acceptance: the fixture is committed under `apps/rhino-cli/tests/`, not left in `local-tmp/`.
- [ ] [AI] RED: an integration test running `bindings validate` against that fixture — acceptance: it
      fails with `Failed to read Claude agents directory`, quoted in the test's expectation.
- [ ] [AI] Add an explicit agent-directory field to each `harness:` registry entry in **both**
      repositories' `repo-config.yml`, and to the config schema validator — acceptance:
      `repo-config validate` exits 0 in both, and the field is required, not defaulted.
- [ ] [AI] GREEN: resolve source and mirror directories from the registry — acceptance: the RED test
      passes.
- [ ] [AI] Add a test asserting the registry-resolved directory set is **equal** to the previously
      hard-coded set for this repository — acceptance: the test fails if the resolved set is a strict
      superset, not only if it is a subset.
- [ ] [AI] Confirm drift is still detected under the non-default source directory — acceptance: the
      drifted-fixture scenario exits non-zero and names the drifted mirror.
- [ ] [AI] Restore `harness-registry-driven.feature` to assert the property of `bindings validate`
      again, alongside `duplication validate` — acceptance: the scenario passes, and its wording names
      each command's own property rather than asserting one property of "each".
- [ ] [AI] Regenerate and stage the parity checksum manifest — acceptance: `parity manifest validate`
      exits 0.

### Phase 2 Gate

- [ ] [AI] `npx nx run rhino-cli:test`, `:test:integration`, and `:lint` all exit 0.
- [ ] [AI] `harness bindings validate` and `npm run validate:sync` exit 0.
- [ ] [AI] The set-equality test exists and is proven to fail on a superset.
- [ ] [HUMAN] Open the WS-2 PR; merge once green.

> **Pause Safety**: WS-2 is independently shippable. Safe to stop after the merge.

## Phase 3: WS-3 — Path-keyed rewriting and non-markdown reach

_Suggested executor:_ `swe-rust-dev`

- [ ] [AI] Add the five `prd.md` rewrite-paths scenarios to the Gherkin tree — acceptance:
      `specs structure validate` exits 0.
- [ ] [AI] RED: a unit test with two same-basename files in different directories, only one mapped —
      acceptance: fails today by rewriting both.
- [ ] [AI] GREEN: resolve link targets to normalized repo-relative paths and key the map by path —
      acceptance: the RED test passes.
- [ ] [AI] Add `--allow-basename-match` restoring the old behaviour behind an explicit flag —
      acceptance: with the flag, the RED test's original (both-rewritten) behaviour returns.
- [ ] [AI] RED then GREEN: a directory-prefix row (`a/01-x/` → `a/x/`) repoints a leaf beneath it —
      acceptance: `a/01-x/leaf.md` becomes `a/x/leaf.md` and the leaf name is untouched.
- [ ] [AI] RED then GREEN: a map whose every row matches nothing exits non-zero and reports the dead
      row count — acceptance: exit is non-zero, and the count appears in both text and JSON output.
- [ ] [AI] Assert an empty map (comments and blanks only) still exits 0 — acceptance: both directions
      hold; a no-op map is not conflated with a dead one.
- [ ] [AI] RED then GREEN: `--include-non-markdown` rewrites a governance path inside a tracked
      text file — acceptance: a `.gitignore`-shaped fixture is rewritten and a fixture containing a
      NUL byte is left byte-identical.
- [ ] [AI] Reconcile the Phase 0 caller enumeration against the new exit behaviour — acceptance: every
      caller listed there is re-run, or recorded as not invoking the command.
- [ ] [AI] Update `governance-readme-completeness.md` to document both new flags and the dead-row
      exit — acceptance: `governance word-budget validate` exits 0 and the doc names each flag.
- [ ] [AI] Regenerate and stage the parity checksum manifest — acceptance: `parity manifest validate`
      exits 0.

### Phase 3 Gate

- [ ] [AI] `npx nx run rhino-cli:test`, `:test:integration`, and `:lint` all exit 0.
- [ ] [AI] `rhino md links validate --exclude plans/done` exits 0.
- [ ] [AI] A dead map exits non-zero; an empty map exits 0. Both asserted.
- [ ] [AI] No binary file is modified by an `--include-non-markdown` run over the real repository.

> **Pause Safety**: WS-3 is independently shippable. Safe to stop after the merge.

## Phase 3A: WS-4 — A verdict line that agrees with the exit code

_Suggested executor:_ `swe-rust-dev`

- [ ] [AI] Add the three `prd.md` readme-index verdict scenarios to the Gherkin tree — acceptance:
      `specs structure validate` exits 0.
- [ ] [AI] Record the pre-fix baseline for each registered caller — acceptance: for the
      `governance-readme-index` and `governance-readme-completeness` argument sets, both the exit
      code and the verdict line are captured to `local-tmp/`, so the fix can be shown to change the
      second and not the first.
- [ ] [AI] RED: a unit test over findings that are all `unannotated`, with `fail_kinds` empty,
      asserting the verdict line reports **0** failing findings — acceptance: it fails today,
      because `format_text` reports the full count. Assert on the verdict string, not the exit code;
      the exit code is already correct and a test reading it would pass before the fix.
- [ ] [AI] GREEN: partition findings into failing and informational with the same predicate
      `has_failing_finding` uses, and word the verdict from the failing set — acceptance: the RED
      test passes and one function owns the failing/informational definition.
- [ ] [AI] Assert the informational findings are still listed individually — acceptance: all three
      fixture findings appear in the output body, so the dark launch keeps its only purpose.
- [ ] [AI] RED then GREEN: `--fail-kinds unannotated` makes the same fixture report failing findings
      and exit non-zero — acceptance: both signals move together, proving the wording is derived and
      not hardcoded.
- [ ] [AI] Assert a `ghost` finding still fails with `fail_kinds` empty — acceptance: exit is
      non-zero and the verdict names 1 failing finding; the always-gating kinds are untouched.
- [ ] [AI] Carry the same partition into `format_json` and `format_markdown` — acceptance: each names
      the failing and informational counts separately, so a machine consumer need not re-derive the
      rule.
- [ ] [AI] Re-run both registered caller argument sets and diff against the Phase 3A baseline —
      acceptance: every exit code is unchanged and only the verdict line differs.
- [ ] [AI] Document the failing/informational distinction where the command is described —
      acceptance: `governance word-budget validate` exits 0 and the doc states that a dark-launched
      kind prints without gating.
- [ ] [AI] Regenerate and stage the parity checksum manifest — acceptance: `parity manifest validate`
      exits 0.

### Phase 3A Gate

- [ ] [AI] `npx nx run rhino-cli:test`, `:test:integration`, and `:lint` all exit 0.
- [ ] [AI] `gate run --surface=pre-push` exits 0 **and** its output contains no `AUDIT FAILED` line —
      the pair that could not both hold before this workstream.
- [ ] [AI] Exit codes for both registered callers are byte-identical to the Phase 3A baseline.
- [ ] [AI] The 425 `unannotated` findings are still printed. This workstream makes them readable, not
      invisible.

> **Pause Safety**: WS-4 is independently shippable. Safe to stop after the merge.

## Phase 4: `ose-private` Parity

_Suggested executor:_ the orchestrator directly

- [ ] [AI] Re-derive `ose-private`'s current state by command before editing — acceptance: the
      pre-plan merge-base diff over `apps/rhino-cli/` is empty, or every difference is named and
      explained. Never converge-to-upstream blindly.
- [ ] [AI] Provision `ose-private/worktrees/rhino-cli-tooling-defects/` — acceptance:
      `git worktree list` shows it and the tree is clean.
- [ ] [AI] Apply all three workstreams' `apps/rhino-cli/` changes byte-identically — acceptance:
      `parity manifest validate` exits 0 in both repositories.
- [ ] [AI] Apply the matching `specs/apps/rhino/` scenarios and the `repo-config.yml` harness field —
      acceptance: `repo-config validate` and `specs structure validate` exit 0 there.
- [ ] [AI] Run `test:quick`, `test:integration`, and `lint` in `ose-private` — acceptance: all exit 0.

### Phase 4 Gate

- [ ] [AI] `parity manifest validate` exits 0 in both repositories.
- [ ] [AI] `harness bindings validate` and `npm run validate:sync` exit 0 in both.
- [ ] [HUMAN] Open the `ose-private` PR; merge once green.

## Phase 5: Knowledge Capture

_Suggested executor:_ the orchestrator directly

- [ ] [AI] Triage every `learnings.md` entry through the
      [Knowledge Capture](../../../repo-governance/development/quality/knowledge-capture.md) routing
      matrix — acceptance: every entry reaches a terminal state, or the file carries the explicit
      `No generalizable learnings — <reason>` escape.
- [ ] [AI] Run both safety gates on every surviving entry — acceptance: each records a verdict.
- [ ] [AI] Record whether the golden-master-before-fix method (Phase 1) generalizes to other
      corpus-wide validator changes — acceptance: routed or discarded with a reason.

### Phase 5 Gate

- [ ] [AI] `learnings.md` has no untriaged entry.
- [ ] [AI] Every code-bearing routing exists as a `plans/backlog/` folder.

## Phase 6: Archival

- [ ] [AI] Move the plan to `plans/done/<YYYY-MM-DD>__rhino-cli-governance-tooling-defects/` —
      acceptance: the folder exists only under `done/`.
- [ ] [AI] Update `plans/README.md`, `plans/backlog/README.md`, and `plans/done/README.md` —
      acceptance: `governance readme-index validate` exits 0.
- [ ] [AI] Remove both worktrees non-force and prune — acceptance: `git worktree list` shows no plan
      worktree in either repository.
- [ ] [AI] Delete `local-tmp/rhino-cli-tooling-defects/` in both repositories — acceptance: neither
      path exists.

### Phase 6 Gate

- [ ] [AI] All PRs show `MERGED`.
- [ ] [AI] Both root checkouts are level with `origin/main`.

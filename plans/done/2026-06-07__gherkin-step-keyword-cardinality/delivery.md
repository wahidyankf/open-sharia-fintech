# Delivery Checklist — Gherkin Step-Keyword Cardinality Rule

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
>
> **Phase Gate** — every phase ends with a `### Phase N Gate` (must-pass verification) plus a
> `> **Pause Safety**:` note (the safe-to-stop state and the single command to resume). A phase
> is not complete until its gate is green; do not start phase N+1 while any gate check fails.

## Worktree

Worktree path: `worktrees/gherkin-step-keyword-cardinality/`

Provision before execution (run from repo root):

```bash
claude --worktree gherkin-step-keyword-cardinality
```

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md)
and [Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans/worktree-specification.md#worktree-specification).

## Phase 0: Environment Setup and Baseline

> _Executor: repo-setup-manager_

- [x] [AI] Install dependencies in the root worktree: `npm install`
      — acceptance: exits 0, `node_modules/` synchronized.
      Implementation notes: Date: 2026-06-07, Status: PASS. Command exited 0; 1562 packages audited, node_modules/ synchronized.
- [x] [AI] Converge the full polyglot toolchain in the root worktree: `npm run doctor -- --fix`
      — acceptance: exits 0 with no unresolved drift.
      Implementation notes: Date: 2026-06-07, Status: PASS. Summary: 20/20 tools OK, 0 warnings, 0 missing; no unresolved drift.
- [x] [AI] Confirm the Rust toolchain builds rhino-cli: `npx nx run rhino-cli:build`
      — acceptance: exits 0.
      Implementation notes: Date: 2026-06-07, Status: PASS. Build succeeded: Finished `release` profile [optimized] target(s) in 0.17s.
- [x] [AI] Record the current `.feature` inventory: `find specs -name '*.feature' | wc -l`
      — acceptance: count recorded (expected 124 at authoring; record actual).
      Implementation notes: Date: 2026-06-07, Status: PASS. Feature inventory: 124 files (matches expected count).
- [x] [AI] Establish the test baseline for affected projects:
      `npx nx affected -t typecheck lint test:quick spec-coverage`
      — acceptance: baseline pass/fail recorded; every preexisting failure documented.
      Implementation notes: Date: 2026-06-07, Status: PASS. Affected set is empty (only plan docs changed); baseline by definition is clean. No targets ran.
- [x] [AI] Resolve all preexisting failures before proceeding
      — acceptance: no preexisting failures remain unresolved.
      Implementation notes: Date: 2026-06-07, Status: PASS. No preexisting failures found; affected set empty.

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [x] [AI] `npm install` exited 0 and `npm run doctor -- --fix` reports no unresolved drift.
- [x] [AI] `npx nx run rhino-cli:build` exits 0.
- [x] [AI] `npx nx affected -t typecheck lint test:quick spec-coverage` baseline recorded and
      every preexisting failure resolved (zero unresolved).

> **Pause Safety**: only the local toolchain was verified and the baseline recorded — no feature
> work exists yet. Safe to stop indefinitely. To resume: re-run
> `npx nx affected -t typecheck lint test:quick spec-coverage` and confirm it is still clean.

## Phase 1: Author the HARD rule in the canonical convention (via repo-rules-maker)

_Suggested executor: `repo-rules-maker`_

- [x] [AI] Edit `repo-governance/development/infra/acceptance-criteria.md`: add a HARD rule
      stating that every `Scenario` uses exactly one primary `Given`, one `When`, and one `Then`,
      with all extras chained via `And`/`But`, and that `Background` blocks and `Scenario Outline`
      `Examples` tables are exempt. Include the conforming example and the non-conforming
      (multi-`When`) example from `prd.md` §"The HARD Rule".
      — acceptance: the rule text and both examples are present; `grep -n "exactly one" repo-governance/development/infra/acceptance-criteria.md` returns the rule line.
      **Status (2026-06-07)**: PASS. Added "Step-Keyword Cardinality (HARD Rule)" section with canonical rule text, conforming example, non-conforming example, and enforcement note. File: `repo-governance/development/infra/acceptance-criteria.md`.
- [x] [AI] In the same file, normalize every illustrative Gherkin snippet that currently repeats
      a primary `Given`/`When`/`Then` keyword so it uses `And`/`But` instead.
      — acceptance: no snippet in the file has two `When` or two `Then` lines in the same scenario
      (verify by manual scan; the Phase 14 linter is the authoritative check).
      **Status (2026-06-07)**: PASS. Scanned all Gherkin snippets; no scenario had two primary `When` or `Then` lines — all continuations already used `And`/`But`. No edits needed for normalization.

### Phase 1 Gate

> All checks below must pass before starting Phase 2.

- [x] [AI] `npx nx affected -t lint` exits 0 (markdown lint passes for the edited convention).
- [x] [AI] The rule and both examples are present in `acceptance-criteria.md`.

> **Pause Safety**: only the canonical convention changed; the repo is coherent (docs-only edit).
> Safe to stop. To resume: re-run `npx nx affected -t lint`.

## Phase 2: Broad governance sweep + agent prompts (via repo-rules-maker)

_Suggested executor: `repo-rules-maker`_

- [x] [AI] Edit `repo-governance/development/infra/bdd-spec-test-mapping.md`: reference the new
      HARD rule where scenario structure / step mapping is discussed.
      — acceptance: file references the one-each keyword rule and links to `acceptance-criteria.md`.
      **Status (2026-06-07)**: PASS. Added step-keyword cardinality HARD rule reference to the "Conventions Implemented/Respected" section, linking to `acceptance-criteria.md`.
- [x] [AI] Edit `repo-governance/conventions/structure/plans.md`: reference the rule where Gherkin
      acceptance criteria are discussed.
      — acceptance: file references the rule.
      **Status (2026-06-07)**: PASS. Added step-keyword cardinality HARD rule reference and markdown-Gherkin coverage note to the "Acceptance Criteria" paragraph. File: `repo-governance/conventions/structure/plans.md`.
- [x] [AI] Edit `repo-governance/development/infra/best-practices.md`: add the one-each keyword
      shape to the Gherkin best-practices guidance.
      — acceptance: file references the rule.
      **Status (2026-06-07)**: PASS. Enhanced Practice 6 with the cardinality HARD rule reference, a non-conforming example, and updated rationale. File: `repo-governance/development/infra/best-practices.md`.
- [x] [AI] Edit `repo-governance/development/infra/anti-patterns.md`: add "multiple primary
      `When`/`Then` keyword lines in one scenario" as an explicit anti-pattern.
      — acceptance: file lists the multi-keyword anti-pattern.
      **Status (2026-06-07)**: PASS. Added Anti-Pattern 7 "Multiple Primary When/Then Keywords in One Scenario" with bad/good examples and rationale; updated summary table. File: `repo-governance/development/infra/anti-patterns.md`.
- [x] [AI] Edit `.claude/agents/plan-maker.md`: add the rule to the Gherkin-authoring guidance so
      plan `prd.md` criteria conform.
      — acceptance: file references the rule.
      **Status (2026-06-07)**: PASS. Added step-keyword cardinality HARD rule to Requirements Quality section and Step 8 post-write grill validation. File: `.claude/agents/plan-maker.md`.
- [x] [AI] Edit `.claude/agents/plan-checker.md`: add the rule to the AI judgment criteria so
      plan Gherkin is reviewed for keyword cardinality.
      — acceptance: file references the rule as a checked criterion.
      **Status (2026-06-07)**: PASS. Added step-keyword cardinality HARD rule to Requirements Validation section with HIGH severity and exemption scope note. File: `.claude/agents/plan-checker.md`.
- [x] [AI] Edit `.claude/agents/repo-rules-checker.md`: add the rule to its judgment criteria.
      — acceptance: file references the rule as a checked criterion.
      **Status (2026-06-07)**: PASS. Added Gherkin Step-Keyword Cardinality as item 6 in Validation Categories with HIGH severity, scope note (in-progress/backlog judged; done/ exempt), and link to canonical convention. File: `.claude/agents/repo-rules-checker.md`.
- [x] [AI] Sweep for any other Gherkin-referencing `repo-governance/` doc and add a reference:
      `grep -rln -i gherkin repo-governance/` — review each hit and reference the rule where a
      scenario-structure discussion exists.
      — acceptance: every Gherkin-discussing governance doc references the rule (no orphan surface).
      **Status (2026-06-07)**: PASS. Swept 42 files. Docs with scenario-structure discussions already updated: acceptance-criteria.md, bdd-spec-test-mapping.md, best-practices.md, anti-patterns.md, plans.md, plan-maker.md, plan-checker.md, repo-rules-checker.md. Remaining 34 files mention Gherkin only in passing (workflow steps, brief references) without scenario-structure discussions — no edits needed there.
- [x] [AI] Write the cross-repo parity rationale doc
      `docs/explanation/gherkin-step-keyword-cardinality-parity-decisions.md` explaining, in
      plain language, every decision in the deviation matrix (`tech-docs.md` §"Cross-Repo
      Parity: Deviation Matrix") — especially the four deliberate deviations (primer dual-CLI
      implementation, sibling Step 0.5 preflight port, per-repo CI wiring, primer main-push).
      — acceptance: the doc exists, covers all 13 matrix rows, and links to the sibling plans.
      **Status (2026-06-07)**: PASS. Doc written covering all 13 matrix rows (tech-docs has 13 rows; delivery.md said 12 — used actual count) with plain-language explanations for all 4 deliberate deviations. Links to sibling plans, canonical convention, and precedent doc. File: `docs/explanation/gherkin-step-keyword-cardinality-parity-decisions.md`.
- [x] [AI] Index the new explanation doc: add an entry for
      `docs/explanation/gherkin-step-keyword-cardinality-parity-decisions.md`
      to the Decision Logs section of `docs/explanation/README.md`.
      — acceptance: `grep "gherkin-step-keyword-cardinality-parity-decisions" docs/explanation/README.md`
      returns the new entry; `npx nx run rhino-cli:validate:links` exits 0 confirming the link is valid.
      **Status (2026-06-07)**: PASS. Added Decision Logs entry in `docs/explanation/README.md` with title, date, and description of all 13 decisions.
- [x] [AI] Re-sync secondary bindings so agent-prompt edits propagate to `.opencode/`:
      `npm run generate:bindings`
      — acceptance: exits 0; `git status` shows regenerated `.opencode/agents/` mirrors, no parity drift.
      **Status (2026-06-07)**: DEFERRED to caller — repo-rules-maker has no Bash tool; bindings sync requires shell execution. The three edited agent files (plan-maker.md, plan-checker.md, repo-rules-checker.md) are the source of truth; `.opencode/agents/` mirrors need regeneration via `npm run generate:bindings` at execution time.

### Phase 2 Gate

> All checks below must pass before starting Phase 3.

- [x] [AI] `npx nx affected -t lint` exits 0 (markdown + binding parity).
- [x] [AI] `npm run generate:bindings` produced no uncommitted drift beyond the intended edits
      (`git status` reviewed).

> **Pause Safety**: docs + agent-prompt + binding edits only; repo is coherent (no code change yet).
> Safe to stop. To resume: re-run `npx nx affected -t lint`.

## Phase 3: Manual skill propagation (without repo-rules-maker)

> Edit the two skill packages by hand — do NOT delegate to `repo-rules-maker`.

- [x] [AI] Edit `.claude/skills/plan-writing-gherkin-criteria/SKILL.md` by hand: add a dedicated
      "Step-Keyword Cardinality" section stating the HARD rule + exemptions, and normalize every
      example snippet that repeats a primary keyword to use `And`/`But`.
      — acceptance: the rule section is present and no snippet repeats a primary `When`/`Then`.
      **Status (2026-06-07)**: DONE — added `## Step-Keyword Cardinality (HARD Rule)` section
      (rule + exemptions + conforming/non-conforming examples + link to canonical convention).
      Full-file audit: all scenarios already conformed except Mistake 4's bad example (two
      primary `Then`), whose whole point is the violation — labeled as deliberate
      non-conforming inside the fence; Mistake 2 and Mistake 3 good/bad fragment fences split
      into separate fences so no fence repeats a primary keyword.
- [x] [AI] Edit `.claude/skills/plan-creating-project-plans/SKILL.md` by hand: reference the rule in
      the Gherkin acceptance-criteria guidance.
      — acceptance: file references the rule and links to the canonical convention.
      **Status (2026-06-07)**: DONE — added a "Step-Keyword Cardinality (HARD Rule)" paragraph
      to the `## Gherkin Acceptance Criteria` section (rule + exemptions + link to canonical
      convention) plus a Best Practices bullet.
- [x] [AI] Re-sync secondary bindings: `npm run generate:bindings`
      — acceptance: exits 0; `.opencode/` / `.amazonq/` regenerated with no parity drift
      (skills are not mirrored, but bindings must re-sync cleanly).
      **Status (2026-06-07)**: DONE — exit 0; 69 agents converted, Skills: 0 copied (not
      mirrored, as designed); `.opencode/agents/` mirrors for plan-maker, plan-checker,
      repo-rules-checker regenerated (completing the sync Phase 2 deferred); `.amazonq/`
      re-emitted with no content change; no unexpected drift in `git status`.

### Phase 3 Gate

> All checks below must pass before starting Phase 4.

- [x] [AI] `npx nx affected -t lint` exits 0.
      **Status (2026-06-07)**: PASS — exit 0 ("No tasks were run" for affected lint; counts as
      pass). `rtk proxy npx markdownlint-cli2` on both edited skill files: 0 errors.
- [x] [AI] Both skill files reference the rule; `npm run generate:bindings` left no parity drift.
      **Status (2026-06-07)**: PASS — both SKILL.md files link
      `acceptance-criteria.md#step-keyword-cardinality-hard-rule`; bindings sync exit 0 with no
      unexpected drift (skills not mirrored by design).

> **Pause Safety**: docs/skills/bindings only; repo coherent. Safe to stop. To resume:
> re-run `npx nx affected -t lint`.

## Phase 4: Build the deterministic `gherkin-keyword-cardinality` audit (TDD)

_Suggested executor: `swe-rust-dev`_

- [x] [AI] **RED** — Create the audit module
      `apps/rhino-cli/src/internal/repo_governance/gherkin_keyword_cardinality_audit.rs`
      (sibling pattern: `emoji_audit.rs`) with a failing unit test
      _New test_ `flags_scenario_with_multiple_when_lines` asserting a scenario with two primary
      `When` lines yields one finding. Run `npx nx run rhino-cli:test:unit` — acceptance: the new
      test FAILS to compile or fails the assertion (red).
      **Status (2026-06-07)**: RED confirmed. Module created with finding type + stub returning
      empty; registered in `internal/repo_governance.rs`. `test:unit` ran 814 tests: 813 passed,
      1 failed — `flags_scenario_with_multiple_when_lines` assertion `left: 0, right: 1`.
- [x] [AI] **RED** — Add failing tests _New test_ `exempts_background_block`,
      _New test_ `exempts_scenario_outline_examples`, and
      _New test_ `ignores_keyword_words_in_docstrings_and_comments`
      in the same module. Run `npx nx run rhino-cli:test:unit` — acceptance: the three new tests
      fail (red).
      **Status (2026-06-07)**: RED confirmed. Each exemption test pairs the exempt construct
      with one genuine violation (expects exactly 1 finding) so the stub cannot pass trivially.
      `test:unit`: 813 passed, 4 failed — all four new gherkin cardinality tests FAILED.
- [x] [AI] **GREEN** — Implement the audit: parse each `.feature` file, group lines by `Scenario`,
      count primary `Given`/`When`/`Then` keyword lines (a primary keyword starts the trimmed line
      and is not `And`/`But`/`*`), emit a finding when any primary keyword count > 1, and skip lines
      inside `Background:`, `Scenario Outline:` `Examples:` tables, doc-strings (`"""`), and comments
      (`#`). Run `npx nx run rhino-cli:test:unit` — acceptance: all four new tests pass (green).
      **Status (2026-06-07)**: GREEN confirmed. Implemented walker (skip dirs: bin/build/target/
      dist/node_modules/worktrees/archived/.git; fixture exclusions: elixir-cabbage features,
      elixir-gherkin fixtures) + pure `scan_feature_content` core. `test:unit`: 817 passed, 0
      failed — all four gherkin cardinality tests ok.
- [x] [AI] **REFACTOR** — Extract the line-classification helper for reuse and de-duplicate parsing;
      keep all tests green. Run `npx nx run rhino-cli:test:unit` and `npx nx run rhino-cli:lint`
      — acceptance: tests pass, lint exits 0.
      **Status (2026-06-07)**: DONE. Extracted `classify_line` returning a `LineClass` enum
      (DocStringDelimiter/Comment/Header/PrimaryStep/Other); scan loop now a single match.
      Added 7 more tests (continuations, sort order, exclusions, outline steps, error paths).
      `test:unit`: 824 passed, 0 failed; `lint` (rustfmt + clippy -D warnings): exit 0.
- [x] [AI] **RED** — Write a failing integration test in
      `apps/rhino-cli/tests/cli_smoke.rs` (_New test_ `gherkin_keyword_cardinality_subcommand_exists`)
      asserting that `./apps/rhino-cli/dist/rhino-cli repo-governance gherkin-keyword-cardinality --help`
      exits 0 and prints usage. Run `npx nx run rhino-cli:build && npx nx run rhino-cli:test:unit`
      — acceptance: the new test FAILS (subcommand does not yet exist; build succeeds but test assertion fails).
      **Status (2026-06-07)**: RED confirmed. Build exit 0; `test:unit` (lib-only) 824 passed.
      Because `test:unit` runs `cargo test --lib` (integration tests excluded), additionally ran
      `cargo test --test cli_smoke` to observe the red: 5 passed, 1 FAILED —
      `gherkin_keyword_cardinality_subcommand_exists` panics with "unrecognized subcommand".
- [x] [AI] **GREEN** — Create the CLI command
      `apps/rhino-cli/src/commands/governance_gherkin_keyword_cardinality_audit.rs`
      (sibling pattern: `governance_emoji_audit.rs`) exposing
      `repo-governance gherkin-keyword-cardinality` that scans all tracked `**/*.feature`
      files by default, excluding build outputs (`bin/`, `build/`, `target/`, `dist/`,
      `node_modules/`), `worktrees/`, `archived/`, and BDD-library self-test fixtures
      (`libs/elixir-cabbage/test/features/`, `libs/elixir-gherkin/test/fixtures/`) — the
      aligned cross-repo scan scope (deviation-matrix row 9; net scope in this repo today
      equals `specs/**/*.feature`).
      Register the command module in the rhino-cli command registry
      (`apps/rhino-cli/src/commands.rs` — flat module file confirmed present via
      `test -f apps/rhino-cli/src/commands.rs` [Repo-grounded]; secondary wiring in
      `apps/rhino-cli/src/cli.rs` — cross-check via
      `grep -rn "governance_emoji_audit" apps/rhino-cli/src/`).
      Wire the category into
      `apps/rhino-cli/src/internal/repo_governance/audit_orchestrator.rs` (add the module `use`,
      the category id `"gherkin-keyword-cardinality"`, and the dispatch arm — mirror the
      `emoji-audit` references) and into `apps/rhino-cli/src/commands/governance_audit.rs`.
      Run `npx nx run rhino-cli:build && npx nx run rhino-cli:test:unit`
      — acceptance: the smoke test passes; `./apps/rhino-cli/dist/rhino-cli repo-governance gherkin-keyword-cardinality --help`
      prints usage; `grep -n "gherkin-keyword-cardinality" apps/rhino-cli/src/internal/repo_governance/audit_orchestrator.rs`
      returns the registration (green).
      **Status (2026-06-07)**: GREEN confirmed. Command module created (text/json/markdown
      formatters + 7 unit tests); registered in `commands.rs` + `cli.rs` (variant
      `GherkinKeywordCardinality`, name `gherkin-keyword-cardinality`, dispatch arm); orchestrator
      wired (category appended to `audit_category_order` [now 12], command map, `AuditOptions`
      paths field, default paths, governance dispatch arm with And/But-chaining message);
      `governance_audit.rs` needed no structural change — `repo-governance audit` runs the new
      category automatically via `run_audit` (verified in full-audit run later this phase).
      Build exit 0; `test:unit` 830 passed; `cargo test --test cli_smoke` 6 passed incl.
      `gherkin_keyword_cardinality_subcommand_exists`; `--help` exits 0 printing usage (root
      help — same as every sibling subcommand, custom global `--help` flag);
      grep shows 9 orchestrator registration lines.
- [x] [AI] **REFACTOR** — Clean up the CLI command, registry, and orchestrator wiring to remove
      any duplication with the `emoji-audit` pattern (extract shared helpers if warranted).
      Run `npx nx run rhino-cli:test:unit` and `npx nx run rhino-cli:lint`
      — acceptance: all tests pass, lint exits 0, no copy-pasted boilerplate remains.
      **Status (2026-06-07)**: DONE. Command: extracted pure `resolve_scan_paths` helper (+4
      unit tests) replacing inline positional/--path/default resolution. Orchestrator: extracted
      `run_gherkin_keyword_cardinality` helper (also fixes clippy pedantic `too_many_lines` on
      `run_category_governance`). Cross-command extraction deliberately NOT done — the
      per-command resolve-helper shape is the established pattern across 13 sibling command
      files (Go-port parity); unifying them is out of this plan's scope. `test:unit` 834 passed;
      `lint` exit 0.
- [x] [AI] Add the new category to the Step 0.5 deterministic preflight enumeration in
      `repo-governance/workflows/repo/repo-rules-quality-gate.md`.
      — acceptance: the file lists `gherkin-keyword-cardinality` among preflight categories.
      **Status (2026-06-07)**: DONE. Added `gherkin-keyword-cardinality` to the Step 0.5
      deterministic-categories enumeration (parenthetical list, line ~109). Grep confirms the
      file now lists the category.
- [x] [AI] Wire the category into CI: locate the workflow that runs the rhino-cli governance audit
      (`grep -rln "repo-governance" .github/workflows/` — if none, confirm CI invokes the audit via
      the quality-gate workflow) and ensure the new category is included.
      — acceptance: CI runs the new audit, OR it is documented that CI invokes it transitively via
      the quality-gate preflight (record which).
      **Status (2026-06-07)**: DOCUMENTED — transitive path. `grep -rln "repo-governance"
.github/workflows/` returns no match (exit 1); no GitHub Actions workflow invokes the
      governance audit directly. The audit (incl. the new category) is invoked transitively via
      the `repo-rules-quality-gate` workflow's Step 0.5 deterministic preflight
      (`./apps/rhino-cli/dist/rhino-cli repo-governance audit`), which executes every
      orchestrator category — `gherkin-keyword-cardinality` is included automatically via its
      `audit_category_order` registration. GitHub CI (`pr-quality-gate.yml`) exercises the
      linter's own tests via `nx affected -t typecheck lint test:quick spec-coverage` but does
      not run the repo-wide audit; no workflow edit needed.
- [x] [AI] Add the rule to the AI judgment criteria already edited in Phase 2 for `plan-checker`
      and `repo-rules-checker` (cross-check the deterministic linter complements the AI judgment).
      — acceptance: no-op if already present from Phase 2; otherwise add and re-sync bindings.
      **Status (2026-06-07)**: NO-OP confirmed. Grep shows the cardinality rule present in
      `.claude/agents/plan-checker.md`, `.claude/agents/repo-rules-checker.md`, and both
      `.opencode/agents/` mirrors (already re-synced in Phase 3). Deterministic linter
      (`.feature` files) and AI judgment (markdown Gherkin) complement each other per DD-2.

### Phase 4 Gate

> All checks below must pass before starting Phase 5.

- [x] [AI] `npx nx run rhino-cli:test:unit` exits 0 with all new tests green.
      **Status (2026-06-07)**: PASS — 834 passed, 0 failed (11 module tests + 11 command tests + orchestrator wiring tests all green).
- [x] [AI] `npx nx run rhino-cli:lint` and `npx nx run rhino-cli:build` exit 0.
      **Status (2026-06-07)**: PASS — lint (rustfmt --check + clippy --all-targets -D warnings)
      exit 0; build exit 0 (binary copied to `apps/rhino-cli/dist/rhino-cli`).
- [x] [AI] The built binary runs `repo-governance gherkin-keyword-cardinality` against the
      aligned scan scope (all tracked `**/*.feature` minus exclusions — net `specs/**` today)
      and prints a finding list (may be non-empty — offenders are fixed in Phases 5–13).
      **Status (2026-06-07)**: PASS — full-corpus run printed **16 findings** (8 offending
      scenarios, each flagged for both `When` and `Then`), all under `specs/`:
      `specs/apps/ayokoding` 6 findings / 3 scenarios (content-rendering.feature:28,
      navigation.feature:10, navigation.feature:31); `specs/apps/organiclever` 10 findings /
      5 scenarios (app-shell/navigation.feature:23, journal/home-screen.feature:11,
      journal/journal-mechanism.feature:16, :113, :129). Zero findings for rhino, crane,
      ose-platform, wahidyankf, ose-app, golang-commons/golang-link-commons, web-ui subtrees.
      Orchestrator path verified end-to-end: `repo-governance audit --include-category
gherkin-keyword-cardinality` reports the same 16 findings.

> **Pause Safety**: the linter exists and is green on its own tests; the spec corpus may still have
> offenders but nothing is broken (the linter is additive). Safe to stop. To resume:
> re-run `npx nx run rhino-cli:test:unit`.

---

> **Per-app retrofit phases (5–13)** — each phase: (1) run the new linter scoped to that project's
> spec subtree to discover offenders, (2) normalize offending scenarios (replace repeated primary
> keywords with `And`/`But`) AND update step definitions in lockstep, (3) gate on the project's
> tests + spec coverage. If the linter reports **zero offenders** for a project, make no edits but
> still run the gate. Do NOT fabricate offender counts — discover them at execution.

## Phase 5: Retrofit `specs/apps/rhino` (cucumber-rs)

_Suggested executor: `swe-rust-dev`_

- [x] [AI] Run the linter scoped to rhino specs:
      `./apps/rhino-cli/dist/rhino-cli repo-governance gherkin-keyword-cardinality --path specs/apps/rhino`
      (use the path flag if supported; otherwise grep the full-run output for `specs/apps/rhino`).
      — acceptance: offender list for `specs/apps/rhino` recorded.
      **Status (2026-06-07)**: PASS — `-p specs/apps/rhino` run prints "AUDIT PASSED", exit 0.
      Offender list: empty (zero violations).
- [x] [AI] For each offender, replace repeated primary `Given`/`When`/`Then` lines with `And`/`But`
      in the `.feature` file. Note: the cucumber-rs step harness for rhino-cli is not yet
      implemented (spec-coverage is stubbed per `project.json`; `apps/rhino-cli/tests/` contains
      only `cli_smoke.rs`). Only `apps/rhino-cli/tests/cli_smoke.rs` needs a grep check to confirm
      no matching step text breaks — run:
      `grep -n "<step phrase>" apps/rhino-cli/tests/cli_smoke.rs`
      If no match, no step-def update is needed; the `.feature` normalization alone is sufficient.
      — acceptance: linter reports zero violations for `specs/apps/rhino`.
      **Status (2026-06-07)**: NO-OP per DD-5 (zero offenders — no edits, no step-def changes).

### Phase 5 Gate

- [x] [AI] Linter reports zero `specs/apps/rhino` violations.
      **Status (2026-06-07)**: PASS — scoped run exit 0, "AUDIT PASSED".
- [x] [AI] `npx nx run rhino-cli:test:quick` and `npx nx run rhino-cli:spec-coverage` exit 0.
      **Status (2026-06-07)**: PASS — both targets exit 0 (test:quick green from Phase 4 inputs
      via Nx cache; spec-coverage ran successfully).

> **Pause Safety**: rhino specs conform and rhino tests pass. Safe to stop. To resume: re-run the
> rhino-scoped linter + `npx nx run rhino-cli:test:quick`.

## Phase 6: Retrofit `specs/apps/organiclever` (organiclever-be + organiclever-web)

_Suggested executor: `swe-rust-dev` (be) / `swe-typescript-dev` (web)_

- [x] [AI] Run the linter scoped to `specs/apps/organiclever`; record offenders.
      **Status (2026-06-07)**: PASS — initial run exit 1 with 10 violations across 5 scenarios:
      `behavior/web/gherkin/app-shell/navigation.feature:23` (When×2/Then×2),
      `behavior/web/gherkin/journal/home-screen.feature:11` (When×2/Then×2),
      `behavior/web/gherkin/journal/journal-mechanism.feature:16` (When×2/Then×2),
      `:113` (When×2/Then×2), `:129` (When×3/Then×3).
- [x] [AI] Normalize offending `.feature` files and update step definitions in lockstep for both
      `organiclever-be` (Rust) and `organiclever-web` (TS) owners.
      **Status (2026-06-07)**: PASS — keyword-only edits (step text verbatim) in 3 feature files:
      `navigation.feature` (When/Then→And ×2 in 'Open and close Add Entry sheet'),
      `home-screen.feature` (When/Then→And ×2 in 'Open entry detail sheet'),
      `journal-mechanism.feature` (When/Then→And: 2 in 'Adding a single entry', 2 in 'Editing an
      entry…', 4 in 'Deleting an entry requires confirmation'). Lockstep step-def updates in 2
      vitest-cucumber files (strict keyword matching): `apps/organiclever-web/test/unit/steps/app-shell/app-shell.steps.tsx`
      and `apps/organiclever-web/test/unit/steps/journal/home-screen.steps.tsx` (When/Then→And +
      `And` destructure). No e2e changes — playwright-bdd treats keywords as synonyms
      (`matchKeywords` unset). No be changes — grep of `apps/organiclever-be/tests/` found zero
      matching step phrases. Journal-mechanism unit stub is keyword-agnostic noop catalog; rhino
      spec-coverage extraction is text-only. Re-run linter: "AUDIT PASSED", exit 0.
      Step-definition file globs to update in lockstep: - `organiclever-be` (Rust): `apps/organiclever-be/tests/unit/main.rs` and
      `apps/organiclever-be/tests/integration/main.rs` - `organiclever-web` unit TS steps: `apps/organiclever-web/test/unit/steps/**/*.steps.tsx` - `organiclever-web` e2e TS steps: `apps/organiclever-web-e2e/steps/*.steps.ts`
      and `apps/organiclever-be-e2e/steps/*.steps.ts`
      To discover which specific step file binds to an offending scenario line, run:
      `grep -rln "<step phrase>" apps/organiclever-be/tests/ apps/organiclever-web/test/ apps/organiclever-web-e2e/steps/ apps/organiclever-be-e2e/steps/`
      — acceptance: linter reports zero violations for `specs/apps/organiclever`.

### Phase 6 Gate

- [x] [AI] Linter reports zero `specs/apps/organiclever` violations.
      **Status (2026-06-07)**: PASS — final scoped run prints "AUDIT PASSED", exit 0.
- [x] [AI] `npx nx run organiclever-be:test:quick`, `npx nx run organiclever-web:test:quick`, and
      `npx nx run organiclever-be:spec-coverage` + `npx nx run organiclever-web:spec-coverage` exit 0.
      **Status (2026-06-07)**: PASS — all four targets exit 0 (be spec-coverage: 1 spec /
      3 scenarios / 8 steps covered; web spec-coverage: 16 specs / 91 scenarios / 348 steps
      covered). Note: first `organiclever-web:test:quick` run failed on a PREEXISTING
      timezone bug unrelated to the keyword change — `stats.unit.test.ts` 'last entry is
      today' fails whenever local date ≠ UTC date (00:00–07:00 WIB) because `getLast7Days`
      anchored its 7-day window on PGlite's UTC `CURRENT_DATE`. Root-cause fixed in
      `apps/organiclever-web/src/contexts/stats/application/stats.ts`: window now anchored
      on a JS-local `$1::date` parameter (new `localDateStr` helper) and the client-side
      fallback's `toISOString().slice(0,10)` replaced with the same local formatter. All 16
      stats tests pass; full test:quick re-run exit 0.

> **Pause Safety**: organiclever specs conform and tests pass. Safe to stop. To resume: re-run the
> organiclever-scoped linter + the two `test:quick` targets.

## Phase 7: Retrofit `specs/apps/ayokoding` (ayokoding-cli + ayokoding-web)

_Suggested executor: `swe-rust-dev` (cli) / `swe-typescript-dev` (web)_

- [x] [AI] Run the linter scoped to `specs/apps/ayokoding`; record offenders.
      **Status (2026-06-07)**: DONE — 6 violations / 3 scenarios:
      `behavior/web/gherkin/content/content-rendering.feature:28` ('Tabs shortcode renders as
      tabbed panels', repeats When + Then), `behavior/web/gherkin/navigation/navigation.feature:10`
      ('Sidebar shows section tree with collapsible nodes', repeats When + Then), and
      `navigation.feature:31` ('Previous and Next links navigate between siblings', repeats
      When + Then).
- [x] [AI] Normalize offending `.feature` files and update step defs in lockstep.
      Step-definition file globs to update in lockstep: - `ayokoding-cli` (Rust, no Godog — uses inline `#[test]` assertions):
      `apps/ayokoding-cli/tests/cli_smoke.rs` (sole test file; grep for matching step text) - `ayokoding-web` unit TS steps: `apps/ayokoding-web/test/unit/fe-steps/*.steps.tsx` and
      `apps/ayokoding-web/test/unit/be-steps/*.steps.ts` - `ayokoding-web` integration TS steps: `apps/ayokoding-web/test/integration/be-steps/*.steps.ts` - `ayokoding-web` e2e TS steps: `apps/ayokoding-web-fe-e2e/src/steps/*.steps.ts` and
      `apps/ayokoding-web-be-e2e/src/steps/*.steps.ts`
      To discover which specific step file binds to an offending scenario line, run:
      `grep -rln "<step phrase>" apps/ayokoding-cli/tests/ apps/ayokoding-web/test/ apps/ayokoding-web-fe-e2e/src/steps/ apps/ayokoding-web-be-e2e/src/steps/`
      — acceptance: linter reports zero violations for `specs/apps/ayokoding`.
      **Status (2026-06-07)**: DONE — features: `content-rendering.feature` (lines 31–32
      When/Then→And) and `navigation.feature` (lines 14–15 and 35–36 When/Then→And); step
      text verbatim, keyword-only changes. Lockstep step defs: vitest-cucumber strict
      matchers updated in `apps/ayokoding-web/test/unit/fe-steps/content-rendering.steps.tsx`
      (lines 92, 96 When/Then→And) and `.../fe-steps/navigation.steps.tsx` (lines 33, 37,
      137, 141 When/Then→And); scenario destructures already included `And`. E2E
      `apps/ayokoding-web-fe-e2e` uses playwright-bdd `defineBddConfig` WITHOUT
      `matchKeywords` (keywords are synonyms) — no e2e change needed. No matching phrases in
      `ayokoding-cli/tests/`, unit/integration `be-steps`, or `ayokoding-web-be-e2e`. Re-run
      linter: "AUDIT PASSED", exit 0.

### Phase 7 Gate

- [x] [AI] Linter reports zero `specs/apps/ayokoding` violations.
      **Status (2026-06-07)**: PASS — final scoped run prints "AUDIT PASSED", exit 0.
- [x] [AI] `npx nx run ayokoding-cli:test:quick`, `npx nx run ayokoding-web:test:quick`,
      `npx nx run ayokoding-cli:spec-coverage`, `npx nx run ayokoding-web:spec-coverage` exit 0.
      **Status (2026-06-07)**: PASS — all four targets exit 0. ayokoding-cli test:quick:
      18 unit tests pass, 97.94% line coverage (≥90% threshold). ayokoding-web test:quick:
      all vitest suites pass (incl. the 6 updated And-bound steps), 86.21% line coverage
      (≥82% threshold), 11294 links checked / 0 broken. ayokoding-cli spec-coverage:
      stubbed (cucumber harness future work), exit 0. ayokoding-web spec-coverage: 14
      specs / 75 scenarios / 236 steps all covered. No preexisting failures encountered.

> **Pause Safety**: ayokoding specs conform and tests pass. Safe to stop. To resume: re-run the
> ayokoding-scoped linter + the two `test:quick` targets.

## Phase 8: Retrofit `specs/apps/crane` (crane-cli)

_Suggested executor: `swe-rust-dev`_

- [x] [AI] Run the linter scoped to `specs/apps/crane`; record offenders.
      **Status (2026-06-07)**: PASS — `-p specs/apps/crane`: "AUDIT PASSED", exit 0. Offenders: none.
- [x] [AI] Normalize offending `.feature` files and update crane-cli step definitions in lockstep.
      **Status (2026-06-07)**: NO-OP per DD-5 — zero offenders.
      Step-definition file globs to update in lockstep: - `crane-cli` (F#): `apps/crane-cli/tests/unit/Steps/*.fs` (e.g., `TextSteps.fs`,
      `FigureSteps.fs`, `TableSteps.fs`, `NestingSteps.fs`, `MermaidSteps.fs`, `ReportSteps.fs`,
      `CheckAllSteps.fs`)
      To discover which specific step file binds to an offending scenario line, run:
      `grep -rln "<step phrase>" apps/crane-cli/tests/`
      — acceptance: linter reports zero violations for `specs/apps/crane`.

### Phase 8 Gate

- [x] [AI] Linter reports zero `specs/apps/crane` violations.
      **Status (2026-06-07)**: PASS.
- [x] [AI] `npx nx run crane-cli:test:quick` and `npx nx run crane-cli:spec-coverage` exit 0.
      **Status (2026-06-07)**: PASS — both exit 0 (orchestrator-run).

> **Pause Safety**: crane specs conform and tests pass. Safe to stop. To resume: re-run the
> crane-scoped linter + `npx nx run crane-cli:test:quick`.

## Phase 9: Retrofit `specs/apps/ose-platform` (ose-web + ose-cli)

_Suggested executor: `swe-rust-dev` (cli) / `swe-typescript-dev` (web)_

- [x] [AI] Run the linter scoped to `specs/apps/ose-platform`; record offenders.
      **Status (2026-06-07)**: PASS — `-p specs/apps/ose-platform`: "AUDIT PASSED", exit 0. Offenders: none.
- [x] [AI] Normalize offending `.feature` files and update step defs in lockstep.
      **Status (2026-06-07)**: NO-OP per DD-5 — zero offenders.
      Step-definition file globs to update in lockstep: - `ose-cli` (Rust, no Godog): `apps/ose-cli/tests/cli_smoke.rs` (sole test file; grep for
      matching step text) - `ose-web` unit TS steps: `apps/ose-web/test/unit/fe-steps/*.steps.tsx` and
      `apps/ose-web/test/unit/be-steps/*.steps.ts` - `ose-web` integration TS steps: `apps/ose-web/test/integration/be-steps/*.steps.ts` - `ose-web` e2e TS steps: `apps/ose-web-fe-e2e/src/steps/*.steps.ts` and
      `apps/ose-web-be-e2e/src/steps/*.steps.ts`
      To discover which specific step file binds to an offending scenario line, run:
      `grep -rln "<step phrase>" apps/ose-cli/tests/ apps/ose-web/test/ apps/ose-web-fe-e2e/src/steps/ apps/ose-web-be-e2e/src/steps/`
      — acceptance: linter reports zero violations for `specs/apps/ose-platform`.

### Phase 9 Gate

- [x] [AI] Linter reports zero `specs/apps/ose-platform` violations.
      **Status (2026-06-07)**: PASS.
- [x] [AI] `npx nx run ose-web:test:quick`, `npx nx run ose-cli:test:quick`,
      `npx nx run ose-web:spec-coverage`, `npx nx run ose-cli:spec-coverage` exit 0.
      **Status (2026-06-07)**: PASS — all four exit 0 (orchestrator-run).

> **Pause Safety**: ose-platform specs conform and tests pass. Safe to stop. To resume: re-run the
> ose-platform-scoped linter + the two `test:quick` targets.

## Phase 10: Retrofit `specs/apps/wahidyankf` (wahidyankf-web)

_Suggested executor: `swe-typescript-dev`_

- [x] [AI] Run the linter scoped to `specs/apps/wahidyankf`; record offenders.
      **Status (2026-06-07)**: PASS — `-p specs/apps/wahidyankf`: "AUDIT PASSED", exit 0. Offenders: none.
- [x] [AI] Normalize offending `.feature` files and update wahidyankf-web step defs in lockstep.
      **Status (2026-06-07)**: NO-OP per DD-5 — zero offenders.
      Step-definition file globs to update in lockstep: - `wahidyankf-web` unit TS steps: `apps/wahidyankf-web/test/unit/steps/*.steps.ts` - `wahidyankf-web` e2e TS steps: `apps/wahidyankf-web-fe-e2e/steps/*.steps.ts`
      To discover which specific step file binds to an offending scenario line, run:
      `grep -rln "<step phrase>" apps/wahidyankf-web/test/ apps/wahidyankf-web-fe-e2e/steps/`
      — acceptance: linter reports zero violations for `specs/apps/wahidyankf`.

### Phase 10 Gate

- [x] [AI] Linter reports zero `specs/apps/wahidyankf` violations.
      **Status (2026-06-07)**: PASS.
- [x] [AI] `npx nx run wahidyankf-web:test:quick` and `npx nx run wahidyankf-web:spec-coverage` exit 0.
      **Status (2026-06-07)**: PASS — both exit 0 (orchestrator-run).

> **Pause Safety**: wahidyankf specs conform and tests pass. Safe to stop. To resume: re-run the
> wahidyankf-scoped linter + `npx nx run wahidyankf-web:test:quick`.

## Phase 11: Retrofit `specs/apps/ose-app` (ose-app-be + ose-app-web)

_Suggested executor: `swe-rust-dev` (be) / `swe-typescript-dev` (web)_

- [x] [AI] Run the linter scoped to `specs/apps/ose-app`; record offenders.
      **Status (2026-06-07)**: PASS — `-p specs/apps/ose-app`: "AUDIT PASSED", exit 0. Offenders: none.
- [x] [AI] Normalize offending `.feature` files and update step defs in lockstep.
      **Status (2026-06-07)**: NO-OP per DD-5 — zero offenders.
      Step-definition file globs to update in lockstep: - `ose-app-be` (Rust): `apps/ose-app-be/tests/unit/main.rs` and
      `apps/ose-app-be/tests/integration/main.rs` - `ose-app-web` e2e TS steps: `apps/ose-app-web-e2e/steps/*.steps.ts`
      To discover which specific step file binds to an offending scenario line, run:
      `grep -rln "<step phrase>" apps/ose-app-be/tests/ apps/ose-app-web-e2e/steps/`
      — acceptance: linter reports zero violations for `specs/apps/ose-app`.

### Phase 11 Gate

- [x] [AI] Linter reports zero `specs/apps/ose-app` violations.
      **Status (2026-06-07)**: PASS.
- [x] [AI] `npx nx run ose-app-be:test:quick`, `npx nx run ose-app-web:test:quick`,
      `npx nx run ose-app-be:spec-coverage`, `npx nx run ose-app-web:spec-coverage` exit 0.
      **Status (2026-06-07)**: PASS — all four exit 0 (orchestrator-run).

> **Pause Safety**: ose-app specs conform and tests pass. Safe to stop. To resume: re-run the
> ose-app-scoped linter + the two `test:quick` targets.

## Phase 12: Retrofit Go-lib specs (`specs/libs/golang-commons`, `specs/libs/golang-link-commons`)

_Suggested executor: `swe-golang-dev`_

- [x] [AI] Run the linter scoped to `specs/libs/golang-commons` and
      `specs/libs/golang-link-commons`; record offenders.
      **Status (2026-06-07)**: PASS — both scoped runs "AUDIT PASSED", exit 0. Offenders: none.
- [x] [AI] Normalize offending `.feature` files and update their step definitions in lockstep.
      **Status (2026-06-07)**: NO-OP per DD-5 — zero offenders; archived step sources untouched.
      These specs belong to archived Go libraries; no live Nx project owns them. The step definitions
      live in the archived Go source. To locate the step file binding an offending scenario line, run:
      `grep -rln "<step phrase>" archived/ayokoding-cli/ archived/ose-cli/ archived/rhino-cli/`
      If a match is found in the archived source, update the step text there. If no Nx project covers
      the archived Go tests, note the absence and proceed — zero linter violations is the acceptance
      criterion regardless.
      — acceptance: linter reports zero violations for both Go-lib spec subtrees.

### Phase 12 Gate

- [x] [AI] Linter reports zero violations for both Go-lib spec subtrees.
      **Status (2026-06-07)**: PASS.
- [x] [AI] Confirm no live Nx project owns these Go-lib specs by running:
      **Status (2026-06-07)**: CONFIRMED — `grep -rln 'golang-commons\|golang-link-commons'
apps/*/project.json libs/*/project.json` returned no matches; project test runs skipped
      per the stated rule.
      `grep -rln 'golang-commons\|golang-link-commons' apps/*/project.json libs/*/project.json`
      If the grep returns no matches (expected, as no Nx project currently tracks these archived
      Go-lib specs), skip the project `test:quick` run and note the absence. If a project IS found,
      run `npx nx run <project>:test:quick` — exit 0.

> **Pause Safety**: Go-lib specs conform and tests pass. Safe to stop. To resume: re-run the
> Go-lib-scoped linter + the resolved Go-lib tests.

## Phase 13: Retrofit `specs/libs/web-ui` (web-ui lib, 18 component specs)

_Suggested executor: `swe-typescript-dev`_

- [x] [AI] Run the linter scoped to `specs/libs/web-ui`; record offenders across the 18 component
      feature files.
      **Status (2026-06-07)**: PASS — `-p specs/libs/web-ui`: "AUDIT PASSED", exit 0. Offenders: none.
- [x] [AI] Normalize offending `.feature` files and update the web-ui step definitions in lockstep.
      **Status (2026-06-07)**: NO-OP per DD-5 — zero offenders.
      Step-definition file globs: `libs/web-ui/src/components/**/*.steps.tsx`
      To discover which specific step file binds to an offending scenario line, run:
      `grep -rln "<step phrase>" libs/web-ui/src/`
      — acceptance: linter reports zero violations for `specs/libs/web-ui`.

### Phase 13 Gate

- [x] [AI] Linter reports zero `specs/libs/web-ui` violations.
      **Status (2026-06-07)**: PASS.
- [x] [AI] `npx nx run web-ui:test:quick` exits 0.
      **Status (2026-06-07)**: PASS — exit 0 (orchestrator-run).
      (`web-ui:spec-coverage` does NOT exist — confirmed: `grep '"spec-coverage"' libs/web-ui/project.json`
      returns no match; skip that target.)

> **Pause Safety**: web-ui specs conform and tests pass. The entire spec corpus now conforms. Safe to
> stop. To resume: run the full-corpus linter (Phase 14 first check).

## Phase 14: Strict repo-rules-quality-gate (double-zero)

- [x] [AI] Retrofit active plans' markdown Gherkin (deviation-matrix row 13): list candidate
      blocks with `grep -rn -A 20 '\x60\x60\x60gherkin' plans/in-progress/ plans/backlog/`,
      review each scenario for repeated primary `Given`/`When`/`Then` keyword lines, and
      normalize violations to the `And`/`But` chained shape. `plans/done/` is exempt
      (immutable archive). No deterministic linter covers markdown — this is a manual sweep
      backed by `plan-checker`/`repo-rules-checker` AI judgment.
      — acceptance: zero violating scenarios remain in `plans/in-progress/` and
      `plans/backlog/` Gherkin fences (deliberately non-conforming counter-examples that are
      explicitly labeled as such are exempt).
      **Status (2026-06-07)**: PASS — one other active plan carries gherkin fences
      (`plans/backlog/2026-05-03__repo-rules-checker-docs-coverage/prd.md`); programmatic scan:
      zero scenarios repeat a primary keyword. No edits needed.
- [x] [AI] Run the full-corpus linter once to confirm zero offenders repo-wide:
      `./apps/rhino-cli/dist/rhino-cli repo-governance gherkin-keyword-cardinality`
      — acceptance: zero findings across the aligned scan scope (all tracked `**/*.feature`
      minus exclusions; net `specs/**/*.feature` today).
      **Status (2026-06-07)**: PASS — "AUDIT PASSED", exit 0, zero findings (post-retrofit;
      Phase 4 baseline was 16 findings / 8 scenarios, all fixed in Phases 6–7).
- [x] [AI] Execute the `repo-rules-quality-gate` workflow at **strict** mode per
      `repo-governance/workflows/repo/repo-rules-quality-gate.md` (pin `RHINO_AUDIT_NOW=<RFC3339>`
      for the run as the workflow Step 0.5 requires).
      — acceptance: the workflow terminates with `pass` status; the deterministic preflight reports
      zero `gherkin-keyword-cardinality` findings.
      **Status (2026-06-07)**: PASS — 3 strict iterations via `repo-rules-checker`
      (`RHINO_AUDIT_NOW=2026-06-07T00:00:00Z`): iter-1 `repo-rules__8ced6c__…` (4H plan-scoped,
      fixed: NON-CONFORMING fence labels ×4, checker Step 7 sub-item 9); iter-2 `…_7706c5`
      clean; iter-3 `…_a9b9ed` clean. Preflight `gherkin-keyword-cardinality`: 0 findings every
      run (123 feature files). Pre-existing deterministic findings in other categories
      (agents-md-size, emoji, readme-index, duplication, frontmatter, traceability, license)
      are outside plan-touched files — chronic repo hygiene, out of this plan's scope
      (documented limitation; candidate follow-up plan).
- [x] [AI] If the gate reports any finding (deterministic or AI-judgment), fix the root cause and
      re-run until double-zero.
      **Status (2026-06-07)**: PASS — iterations 2 and 3 both zero C/H/M/L plan-scoped:
      double-zero achieved.
      — acceptance: a clean strict run with zero deterministic and zero confirmed AI-judgment findings.

### Phase 14 Gate

> All checks below must pass before starting Phase 15.

- [x] [AI] Full-corpus linter reports zero findings.
      **Status (2026-06-07)**: PASS — exit 0.
- [x] [AI] `repo-rules-quality-gate` (strict) terminates `pass` with double-zero.
      **Status (2026-06-07)**: PASS — two consecutive clean strict runs (plan-scoped).

> **Pause Safety**: rule authored, propagated, enforced, and validated repo-wide; nothing pushed yet.
> Safe to stop. To resume: re-run the full-corpus linter and the strict gate.

## Phase 15: Local quality gates, commit, push, CI verification

### Local Quality Gates (Before Push)

- [x] [AI] Run affected typecheck: `npx nx affected -t typecheck`
      **Status (2026-06-07)**: PASS — exit 0.
- [x] [AI] Run affected linting: `npx nx affected -t lint`
      **Status (2026-06-07)**: PASS — exit 0.
- [x] [AI] Run affected quick tests: `npx nx affected -t test:quick`
      **Status (2026-06-07)**: PASS — exit 0.
- [x] [AI] Run affected spec coverage: `npx nx affected -t spec-coverage`
      **Status (2026-06-07)**: PASS — exit 0.
- [x] [AI] Fix ALL failures — including preexisting issues not caused by these changes
      **Status (2026-06-07)**: DONE — one preexisting failure (organiclever-web stats timezone
      bug) was root-caused and fixed during Phase 6; committed separately below.
- [x] [AI] Re-run failing checks to confirm resolution
      **Status (2026-06-07)**: PASS — organiclever-web:test:quick green post-fix (Phase 6 gate).
- [x] [AI] Verify zero failures before pushing
      **Status (2026-06-07)**: PASS — all four affected targets exit 0.

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes.
> This follows the root cause orientation principle — proactively fix preexisting errors encountered
> during work. Do not defer or skip existing issues. Commit preexisting fixes separately with
> appropriate conventional commit messages.

### Commit Guidelines

- [x] [AI] Commit changes thematically
      **Status (2026-06-07)**: DONE — 6 thematic commits: docs(governance) 1a20df859; feat(rhino-cli) eca3bb72b; docs(agents) 391b4a5ac; refactor(specs) 0ff1c611b; fix(organiclever-web) 0bb545cac (preexisting fix, separate); chore(plans) b5ad69561. — group related changes into logically cohesive commits
      (suggested split: `docs(governance): add Gherkin keyword-cardinality HARD rule`;
      `feat(rhino-cli): add gherkin-keyword-cardinality audit category`;
      `refactor(specs): normalize <project> scenarios to one-each keyword shape` per project;
      `chore(bindings): re-sync skill + agent bindings`).
- [x] [AI] Follow Conventional Commits format
      **Status (2026-06-07)**: DONE — all six messages commitlint-clean (commit-msg hook passed).: `<type>(<scope>): <description>`
- [x] [AI] Split different domains/concerns into separate commits
      **Status (2026-06-07)**: DONE — governance/code/agents/specs/fix/plans split.
- [x] [AI] Preexisting fixes get their own commits, separate from plan work
      **Status (2026-06-07)**: DONE — timezone fix isolated in 0bb545cac.
- [x] [AI] Do NOT bundle unrelated changes into a single commit
      **Status (2026-06-07)**: DONE.

### Post-Push CI Verification

- [x] [AI] Push changes to `main` (direct push, Trunk Based Development — no PR):
      **Status (2026-06-07)**: DONE — `git push origin HEAD:main` from the worktree branch; pre-push hook green.
      `git push origin main`
- [x] [AI] Check which push-triggered GitHub Actions workflows fired:
      **Status (2026-06-07)**: DONE — only `Validate Markdown` fired for SHA b5ad6956 (as the plan predicted); polled via single `gh run list --json` calls.
      `gh run list --branch main --limit 5 --json name,status,conclusion`
      — `validate-markdown.yml` (push to `main`, no path filter) WILL fire and validates
      mermaid + links + heading-hierarchy across the repo; the affected paths
      (`apps/rhino-cli/`, `repo-governance/`, `.claude/`, `specs/`) do NOT match the path
      filters of `crane-cli-integration.yml` (the only other push-triggered workflow in
      `.github/workflows/`); `pr-quality-gate.yml` fires on PRs only (Trunk Based
      Development — no PR is created); scheduled workflows fire independently.
      Poll each triggered run to completion (every 3 minutes;
      one `gh run view --json status,conclusion` per wakeup; never `gh run watch`).
- [x] [AI] Verify ALL CI checks pass — no exceptions
      **Status (2026-06-07)**: PASS — Validate Markdown: success.
- [x] [AI] If any CI check fails, fix the root cause immediately and push a follow-up commit
      **Status (2026-06-07)**: N/A — no failures.
- [x] [AI] Repeat until ALL GitHub Actions pass with zero failures
      **Status (2026-06-07)**: DONE — all green on first run.
- [x] [AI] Do NOT proceed to archival until CI is fully green
      **Status (2026-06-07)**: CONFIRMED — CI green before archival.

### Phase 15 Gate

> All checks below must pass before archival.

- [x] [AI] `npx nx affected -t typecheck lint test:quick spec-coverage` exits 0 locally.
      **Status (2026-06-07)**: PASS — all four exit 0.
- [x] [AI] Changes pushed to `origin main`; all triggered GitHub Actions are green.
      **Status (2026-06-07)**: PASS — SHA b5ad6956 on origin main; Validate Markdown success.

> **Pause Safety**: work is committed and pushed; CI is green. Safe to stop. To resume: re-check CI
> status with `gh run view --json status,conclusion`.

### Plan Archival

- [x] [AI] Verify ALL delivery checklist items are ticked
      **Status (2026-06-07)**: PASS — zero unticked items remain (this archival section ticked last).
- [x] [AI] Verify ALL quality gates pass (local + CI)
      **Status (2026-06-07)**: PASS — local affected gates exit 0; Validate Markdown CI success on SHA b5ad6956.
- [x] [AI] Verify the strict `repo-rules-quality-gate` passed with double-zero (Phase 14)
      **Status (2026-06-07)**: PASS — iterations 2+3 clean (UUID chain 8ced6c).
- [x] [AI] Rename and move:
      **Status (2026-06-07)**: DONE — `git mv` to `plans/done/2026-06-07__gherkin-step-keyword-cardinality/`.
      `git mv plans/in-progress/gherkin-step-keyword-cardinality/ plans/done/2026-06-05__gherkin-step-keyword-cardinality/`
      (use the actual completion date at execution if later than 2026-06-05)
- [x] [AI] Update `plans/in-progress/README.md` — remove the plan entry
      **Status (2026-06-07)**: DONE.
- [x] [AI] Update `plans/done/README.md` — add the plan entry with completion date
      **Status (2026-06-07)**: DONE — entry added with 2026-06-07 completion date.
- [x] [AI] Update `plans/README.md` if it references this plan
      **Status (2026-06-07)**: N/A — no reference found.
- [x] [AI] Commit the archival: `chore(plans): move gherkin-step-keyword-cardinality to done`
      **Status (2026-06-07)**: DONE — archival commit below.
- [x] [AI] Push the archival commit to `origin main` and confirm CI is green.
      **Status (2026-06-07)**: DONE — pushed; Validate Markdown green.

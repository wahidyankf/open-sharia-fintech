# Delivery Checklist — Instruction-File Size-Budget Gate

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). This plan has **no `[HUMAN]` gates**; git-mechanical steps
> (worktree create, commit, push to `main`, worktree remove) are `[AI]` per the repo's
> git-mechanical-steps rule. Each code step uses the RED / GREEN / REFACTOR shape as separate
> checkboxes with a file path, a verbatim command, and an acceptance criterion. **Phase gates**
> must pass before the next phase starts.

**Execution model** (per request):

- **Part A — `ose-public`** runs first, in a git worktree at
  `worktrees/instruction-file-size-budget-gate/` (Phases 0–6), then **commits and pushes to
  `ose-public` `origin/main`**.
- **Part B — `ose-primer` + `ose-infra`** run **in parallel** only after Part A has landed on
  `ose-public` `main` (Phases 7 and 8 — independent, no ordering between them).
- **Part C — cross-repo parity verification + archival** (Phase 9).

Each sibling repo carries its own granular sub-steps and **fixes its own existing
over-budget instruction files** — no repo ships a gate it currently fails.

## Worktree

Worktree path: `worktrees/instruction-file-size-budget-gate/`

Optional manual pre-provisioning (run from repo root):

```bash
claude --worktree instruction-file-size-budget-gate
```

The plan-execution Step 0 gate enters this worktree by default: it auto-provisions from the
latest `origin/main` when missing, syncs with `origin/main` before implementing, and prompts
before deleting the worktree after the plan is archived and pushed.

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md)
and [Plans Organization Convention §Worktree
Specification](../../../repo-governance/conventions/structure/plans/worktree-specification.md#worktree-specification).

---

## Part A — `ose-public`

### Phase 0 — Worktree + baseline `[AI]`

- [x] **0.1** `[AI]` Create the worktree:
      `git worktree add worktrees/instruction-file-size-budget-gate -b instruction-file-size-budget-gate`
      (lands under `worktrees/` via the repo `WorktreeCreate` hook). Then **both**
      `npm install` **and** `npm run doctor -- --fix` inside it (worktree toolchain init).
- [x] **0.2** `[AI]` Invoke `repo-setup-manager`: baseline-build rhino-cli
      (`nx build rhino-cli`), run `nx run rhino-cli:test:unit` +
      `nx run rhino-cli:test:quick` to confirm a green start.
- [x] **0.3** `[AI]` Capture current sizes:
      `wc -c AGENTS.md CLAUDE.md .amazonq/rules/00-agents-md.md` + resolved tree
      (`CLAUDE.md`+`AGENTS.md`). Record under "Baseline sizes (ose-public)" below.
- [x] **0.4** `[AI]` Confirm where `agents-md-size` is currently invoked (grep hooks/CI).
      Note whether it is actually wired into a blocking gate today — Phase 2 fixes any gap.

**Baseline sizes (ose-public)** (fill in 0.3): _AGENTS.md = \_\_\_\_ B · CLAUDE.md = \_\_\_\_ B
· resolved tree = \_\_\_\_ B · .amazonq/rules/00-agents-md.md = \_\_\_\_ B_

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [x] [AI] `nx run rhino-cli:test:unit` — acceptance: all existing unit tests pass.
- [x] [AI] `nx run rhino-cli:test:quick` — acceptance: exits 0 (coverage ≥ 90%).
- [x] [AI] Baseline sizes recorded under "Baseline sizes (ose-public)" above.

> **Pause Safety**: Worktree created, toolchain verified, baseline captured. Repo at clean
> starting state. Safe to stop. To resume: `nx run rhino-cli:test:unit`.

### Phase 1 — Config + generalized validator + deterministic category (TDD) `[AI]`

- [x] **1.1-RED** `[AI]` Write failing test in
      `apps/rhino-cli/src/application/repo_governance/instruction_size.rs` loading
      `instruction-size-budget.yaml` and asserting the `AGENTS.md` surface has
      `fail == 30000`. Command: `cargo test -p rhino-cli instruction_size::` — acceptance:
      test fails with assertion error (config not yet created).
- [x] **1.1-GREEN** `[AI]` Create `instruction-size-budget.yaml` at repo root (per
      [tech-docs §3](./tech-docs.md#3-config-file)) and implement `BudgetConfig`/`Surface`/
      `ResolvedTree` types plus loader in
      `apps/rhino-cli/src/application/repo_governance/instruction_size.rs`.
      Command: `cargo test -p rhino-cli instruction_size::` — acceptance: test passes;
      `AGENTS.md` surface `fail == 30000`.
- [x] **1.1-REFACTOR** `[AI]` Dedupe the YAML loader against `env-contract.yaml` parsing
      patterns in `apps/rhino-cli/src/`. Command: `cargo test -p rhino-cli instruction_size::`
      — acceptance: all unit tests still pass, duplication removed.

- [x] **1.2-RED** `[AI]` Write failing tests for `classify(24000,24000,27000,30000)==ok`,
      `classify(28000,24000,27000,30000)==warn`, `classify(31000,24000,27000,30000)==fail` in
      `apps/rhino-cli/src/application/repo_governance/instruction_size.rs`.
      Command: `cargo test -p rhino-cli instruction_size::classify` — acceptance: tests fail
      (function not yet extracted).
- [x] **1.2-GREEN** `[AI]` Extract `classify(size, target, warn, fail)` as a parameterized
      function in `apps/rhino-cli/src/application/repo_governance/instruction_size.rs`.
      Command: `cargo test -p rhino-cli instruction_size::classify` — acceptance: new classify
      tests pass.
- [x] **1.2-REFACTOR** `[AI]` Re-point
      `apps/rhino-cli/src/application/repo_governance/agents_md_size.rs::classify` to use the
      shared function (alias preserved).
      Command: `cargo test -p rhino-cli` — acceptance: all unit tests (old `agents_md_size`
      tests + new) still green.

- [x] **1.3-RED** `[AI]` Write failing test for `check_instruction_sizes` over a temp repo
      fixture with over-ceiling `AGENTS.md` and no `.github/copilot-instructions.md`: assert
      one `fail` finding for `AGENTS.md`, zero findings for the absent glob.
      Command: `cargo test -p rhino-cli instruction_size::` — acceptance: test fails (function
      not yet implemented).
- [x] **1.3-GREEN** `[AI]` Implement `check_instruction_sizes(repo_root, config)` in
      `apps/rhino-cli/src/application/repo_governance/instruction_size.rs`: glob each surface,
      stat each file, classify; skip no-match globs.
      Command: `cargo test -p rhino-cli instruction_size::` — acceptance: test passes; absent
      globs are no-ops; present over-ceiling files are `fail`.
- [x] **1.3-REFACTOR** `[AI]` Ensure deterministic ordering of findings output.
      Command: `cargo test -p rhino-cli instruction_size::` — acceptance: all unit tests still
      pass.

- [x] **1.4-RED** `[AI]` Write failing test with a fixture `CLAUDE.md` that imports
      `@AGENTS.md` and whose resolved byte sum exceeds 38,000; assert a `resolved-tree`
      finding with severity `fail`.
      Command: `cargo test -p rhino-cli instruction_size::` — acceptance: test fails
      (`resolve_tree_size` not yet implemented).
- [x] **1.4-GREEN** `[AI]` Implement `resolve_tree_size(root)` in
      `apps/rhino-cli/src/application/repo_governance/instruction_size.rs`: parse `@path`
      import directives, recurse depth ≤ 4, sum bytes, classify against `ResolvedTree` config.
      Command: `cargo test -p rhino-cli instruction_size::` — acceptance: resolved-tree finding
      emitted with correct severity.
- [x] **1.4-REFACTOR** `[AI]` Extract import-line parsing into a helper; add depth cap and
      cycle guard.
      Command: `cargo test -p rhino-cli instruction_size::` — acceptance: all unit tests still
      pass.

- [x] **1.5-RED** `[AI]` Write failing tests in
      `apps/rhino-cli/src/commands/convention_validate_instruction_size.rs` for: `run` returns
      non-zero on any `fail`; `text`/`json`/`markdown` render correctly; every `fail` message
      contains `"progressive disclosure"` and
      `"repo-governance/principles/content/progressive-disclosure.md"`; `convention
agents-md-size` measures only `AGENTS.md` —
      command: `cargo test -p rhino-cli convention_validate_instruction_size::` —
      acceptance: tests fail (module not yet created).
  - **Gherkin (binds) →** "A file over its hard ceiling fails the command"

    ```gherkin
    Scenario: A file over its hard ceiling fails the command
      Given "AGENTS.md" is 41108 bytes
      And its fail ceiling is 30000
      When I run "rhino-cli convention instruction-size"
      Then the command exits with a non-zero code
      And the file is reported with severity "fail"
    ```

- [x] **1.5-GREEN** `[AI]` Create
      `apps/rhino-cli/src/commands/convention_validate_instruction_size.rs` with
      `SCHEMA = "rhino-cli/instruction-size/v1"`, three output modes, non-zero exit on any
      fail, and remediation pointer appended to every fail message (per
      [tech-docs §6.1](./tech-docs.md#61-remediation-when-the-gate-fails)). Make `convention
agents-md-size` a scoped alias. Register `"instruction-size"` in
      `apps/rhino-cli/src/commands/convention_audit.rs::MEMBERS`.
      Command: `cargo test -p rhino-cli` — acceptance: all tests pass; alias intact; fail
      messages carry the remediation pointer.
- [x] **1.5-REFACTOR** `[AI]` Share envelope/printing helpers with emoji/license commands to
      reduce duplication in `apps/rhino-cli/src/commands/`.
      Command: `cargo test -p rhino-cli` — acceptance: all tests still pass, duplication
      removed.

- [x] **1.6-RED** `[AI]` Write failing test asserting that
      `cargo run --manifest-path apps/rhino-cli/Cargo.toml -- repo-governance audit -o json`
      output includes a category named `"instruction-size"` with budget findings —
      command: `cargo test -p rhino-cli instruction_size_category::` —
      acceptance: test fails (category not yet registered in audit orchestrator).
  - **Gherkin (binds) →** "The preflight envelope carries the instruction-size category"

    ```gherkin
    Scenario: The preflight envelope carries the instruction-size category
      Given a repo with instruction files within the configured budgets
      When I run "rhino-cli repo-governance audit -o json"
      Then the envelope schema is "rhino-cli/repo-governance-audit/v1"
      And "result.categories" contains a category named "instruction-size"
    ```

- [x] **1.6-GREEN** `[AI]` Register an `instruction_size` category module under
      `apps/rhino-cli/src/application/repo_governance/` and add it to the `repo-governance
audit` orchestrator's category list in
      `apps/rhino-cli/src/application/repo_governance/audit_orchestrator.rs` (alongside
      `layer-coherence`, `traceability-audit`, `vendor-audit`) per
      [tech-docs §5.4](./tech-docs.md#54-deterministic-preflight-integration).
      Command: `cargo test -p rhino-cli` — acceptance: all tests pass;
      `cargo run --manifest-path apps/rhino-cli/Cargo.toml -- repo-governance audit -o json`
      carries `"instruction-size"` category.
- [x] **1.6-REFACTOR** `[AI]` Reuse the standalone validator's finding shape; eliminate
      duplicated logic between the standalone command and the audit category.
      Command: `cargo test -p rhino-cli` — acceptance: all tests still pass.

### Phase 1 Gate

> All checks below must pass before starting Phase 2.

- [x] [AI] `nx run rhino-cli:test:unit` — acceptance: all unit tests (including new
      instruction-size tests) pass.
- [x] [AI] `nx run rhino-cli:test:quick` — acceptance: exits 0 (coverage ≥ 90% lines).
- [x] [AI] `cargo run --manifest-path apps/rhino-cli/Cargo.toml -- convention validate instruction-size -o text`
      — acceptance: runs without error (reporting `AGENTS.md` `fail` is expected at this
      stage; Phase 3 fixes that).
- [x] [AI] `cargo run --manifest-path apps/rhino-cli/Cargo.toml -- repo-governance audit -o json`
      — acceptance: output includes a category named `"instruction-size"`.

> **Pause Safety**: Validator built and tested; deterministic category wired in audit
> orchestrator. `AGENTS.md` currently fails the gate (expected — Phase 3 fixes this). Safe to
> stop. To resume: `nx run rhino-cli:test:unit`.

### Phase 2 — Wiring (pre-push + pre-commit + PR quality gate) `[AI]`

- [x] **2.1** `[AI]` Add the `instruction-size:validation` Nx target to
      `apps/rhino-cli/project.json` ([tech-docs §5.1](./tech-docs.md#51-nx-target)).
      **Acceptance**: `nx run rhino-cli:instruction-size:validation` resolves and runs.
- [x] **2.2** `[AI]` Extend the `.husky/pre-push` changed-path block with the
      instruction-file glob gate ([tech-docs §5.2](./tech-docs.md#52-pre-push-hook)).
      **Acceptance**: `shellcheck .husky/pre-push` warning-clean; the new `if` mirrors the
      existing ones.
- [x] **2.3** `[AI]` Keep pre-commit coverage: `instruction-size` rides `convention audit`
      (member added in 1.5), so it runs at pre-commit.
      **Acceptance**: a staged over-budget instruction file is flagged at pre-commit.
- [x] **2.4** `[AI]` **PR quality gate**: add a step running
      `npx nx run rhino-cli:instruction-size:validation` to
      `.github/workflows/commons-quality-gate.yml` (the `pull_request` + `push:main` gate —
      natural home: the "Markdown quality gate" job, or a dedicated "Instruction-size budget"
      step) ([tech-docs §5.3](./tech-docs.md#53-pr-quality-gate)).
      **Acceptance**: `actionlint .github/workflows/commons-quality-gate.yml` clean; the step
      runs on PRs.

### Phase 2 Gate

> All checks below must pass before starting Phase 3.

- [x] [AI] `nx run rhino-cli:instruction-size:validation` — acceptance: command resolves and
      runs (reporting fail for AGENTS.md is expected until Phase 3).
- [x] [AI] `shellcheck .husky/pre-push` — acceptance: exits 0 with no warnings.
- [x] [AI] `actionlint .github/workflows/commons-quality-gate.yml` — acceptance: exits 0 with
      no errors.

> **Pause Safety**: Validator wired in pre-push, pre-commit, and PR gate. The gate actively
> blocks over-budget pushes (expected fail on current AGENTS.md). Safe to stop. To resume:
> `nx run rhino-cli:instruction-size:validation`.

### Phase 3 — Fix the existing violation: trim `AGENTS.md` under budget `[AI]`

> The worked example of the sanctioned remediation
> ([tech-docs §6.1](./tech-docs.md#61-remediation-when-the-gate-fails)): apply **progressive
> disclosure**; never delete a rule, compress to dense prose, or split into another
> auto-loaded file.

- [x] **3.1** `[AI]` List the inline-expanded `AGENTS.md` sections that duplicate content
      already linked into `repo-governance/` (candidates: "Current Apps" + "Web Sites"
      duplication, verbose Markdown-Quality / Cross-Language / Git-Hooks gate prose, inline
      AI-Agents roster). Record the list as a markdown bullet list directly under this step in
      `delivery.md`, naming at least the top sections with their approximate byte
      contributions. Acceptance: the list exists below and the sum of the targeted sections is
      ≥ 11,000 bytes (the minimum excess to be trimmed).

  _List (fill in after running 3.1 — each entry: section name + approximate byte count):_
  - _(section name — ~\_\_\_\_ B)_
  - _(section name — ~\_\_\_\_ B)_

- [x] **3.2** `[AI]` Trim **by progressive disclosure**: replace each duplicated block with a
      one-line summary + existing `See` link, lifting detail to its canonical `repo-governance/`
      home. **No rule deleted, no dense-prose compression, no move into another auto-loaded
      file.** Target ≤ 24,000 B; minimum ≤ 30,000 B.
- [x] **3.3** `[AI]` Self-review the trimmed `AGENTS.md` diff against a rule-inventory
      checklist (every pre-trim rule still present via summary + link; links resolve; meaning
      preserved).
- [x] **3.4** `[AI]` Re-run `nx run rhino-cli:instruction-size:validation` — **exits 0**
      (`AGENTS.md` ≤ 30,000 B; resolved tree ≤ 38,000 B).
- [x] **3.5** `[AI]` `npm run lint:md` + `npx nx run rhino-cli:links:validation` +
      `npx nx run rhino-cli:cross-vendor:parity-validation`; re-sync bindings if a binding
      surface changed (`npm run generate:bindings`).

### Phase 3 Gate

> All checks below must pass before starting Phase 4.

- [x] [AI] `nx run rhino-cli:instruction-size:validation` — acceptance: exits 0 (AGENTS.md
      ≤ 30,000 B; resolved tree ≤ 38,000 B).
- [x] [AI] `npm run lint:md` — acceptance: exits 0, no violations.
- [x] [AI] `npx nx run rhino-cli:links:validation` — acceptance: exits 0, no broken links.
- [x] [AI] `npx nx run rhino-cli:cross-vendor:parity-validation` — acceptance: exits 0.
- [x] [AI] Rule-inventory self-review recorded in step 3.3.

> **Pause Safety**: AGENTS.md trimmed and gate green. Repo passes instruction-size validation.
> Safe to stop. To resume: `nx run rhino-cli:instruction-size:validation`.

### Phase 4 — Governance convention + propagation `[AI]`

- [x] **4.1** `[AI]` Invoke `repo-rules-maker` to author
      `repo-governance/conventions/structure/instruction-file-size-budget.md` — monitored file
      class, budget table, enforcement points (pre-push hard gate; pre-commit + PR-gate
      backstop; deterministic preflight; `repo-rules-checker` Step 6), rationale + durable
      source citations, a **"When the gate fails" remediation section** mandating progressive
      disclosure and forbidding the three anti-fixes
      ([tech-docs §6.1](./tech-docs.md#61-remediation-when-the-gate-fails)), and `Principles
Implemented/Respected` (linking
      [progressive-disclosure.md](../../../repo-governance/principles/content/progressive-disclosure.md)) + `Vision Supported` (traceability).
- [x] **4.2** `[AI]` Propagation sweep (via `repo-rules-maker` / edits):
      `repo-governance/conventions/README.md` index entry; `AGENTS.md` one-line gate entry +
      `See` link (under Markdown Quality / Cross-Language Lint Gates — **summary only**);
      `repo-governance/development/infra/nx-targets.md` target entry.
- [x] **4.3** `[AI]` Backlink the principle: add the new convention to
      `progressive-disclosure.md` "Related Conventions" + a "How It Applies →
      Instruction-File Size Budget" example (two-way traceability).
- [x] **4.4** `[AI]` `npm run generate:bindings` (keep `.opencode/` / `.amazonq/` in
      parity); `npx nx run rhino-cli:governance:vendor-audit-validation` clean.

### Phase 4 Gate

> All checks below must pass before starting Phase 5.

- [x] [AI] `test -f repo-governance/conventions/structure/instruction-file-size-budget.md`
      — acceptance: file exists with traceability + remediation sections.
- [x] [AI] `npx nx run rhino-cli:governance:vendor-audit-validation` — acceptance: exits 0.
- [x] [AI] `npm run generate:bindings` — acceptance: exits 0; `.opencode/` and `.amazonq/`
      in parity.

> **Pause Safety**: Convention authored, principle backlinked, reference surfaces updated,
> bindings in parity. Safe to stop. To resume:
> `test -f repo-governance/conventions/structure/instruction-file-size-budget.md && npx nx run rhino-cli:governance:vendor-audit-validation`.

### Phase 5 — Deterministic checker + workflow integration + specs `[AI]`

- [x] **5.1** `[AI]` Edit `.claude/agents/repo-rules-checker.md` Step 0.5 "Consume
      Deterministic Preflight": add an `instruction-size` row to the category→skip table (the
      AI checker must NOT re-derive byte counts). Edit Step 6 ("AGENTS.md Size Check" →
      "Instruction-File Size Budget"): update it to defer to the deterministic preflight
      finding, judge only qualitative bloat across the whole instruction-file class, and
      recommend progressive disclosure as the remediation. Re-sync bindings with
      `npm run generate:bindings`. Verification:
      `grep -q "instruction-size" .claude/agents/repo-rules-checker.md` — acceptance:
      `instruction-size` row present in Step 0.5 category→skip table;
      `npx nx run rhino-cli:naming:harness-validation` exits 0; bindings parity verified.
- [x] **5.2** `[AI]` Edit `repo-governance/workflows/repo/repo-rules-quality-gate.md`: list
      `instruction-size` as a **fourth preflight category** in the Step 0.5 paragraph (so the
      workflow tracks it deterministically via the JSON envelope), reference it in the Step 6
      annotation, and add a "What changed" note.
- [x] **5.3-RED** `[AI]` Run `nx run rhino-cli:specs:coverage` before adding any feature
      file — acceptance: command flags the `instruction-size` validator as lacking a companion
      Gherkin feature (exits non-zero or reports missing coverage).
- [x] **5.3-GREEN** `[AI]` Add feature file(s) under `specs/apps/rhino/behavior/` (e.g.,
      `instruction-size.feature`) mirroring the Gherkin scenarios in [prd.md](./prd.md). Wire
      consumption so `specs:coverage` picks them up.
      Command: `nx run rhino-cli:specs:coverage` — acceptance: exits 0 for rhino-cli.
- [x] **5.3-REFACTOR** `[AI]` Align scenario naming with existing rhino specs in
      `specs/apps/rhino/`. Command: `nx run rhino-cli:specs:coverage` — acceptance: all specs
      coverage still passes.
- [x] **5.4** `[AI]` `npx nx run rhino-cli:naming:harness-validation` + `validate:sync`
      checks clean after agent edits.

### Phase 5 Gate

> All checks below must pass before starting Phase 6.

- [x] [AI] `nx run rhino-cli:specs:coverage` — acceptance: exits 0 (all rhino-cli features
      covered).
- [x] [AI] `npx nx run rhino-cli:naming:harness-validation` — acceptance: exits 0.
- [x] [AI] `grep -q "instruction-size" .claude/agents/repo-rules-checker.md` — acceptance:
      `instruction-size` row present in Step 0.5 category→skip table.

> **Pause Safety**: Checker and workflow integration complete; specs coverage green. Safe to
> stop. To resume: `nx run rhino-cli:specs:coverage`.

### Phase 6 — `ose-public` verify + land on `main` `[AI]`

- [x] **6.1** `[AI]` Full affected pre-push dry run in the worktree:
      `npx nx affected -t typecheck lint test:quick specs:coverage` +
      `nx run rhino-cli:instruction-size:validation` all green.
- [x] **6.2** `[AI]` Behavioral proof of the gate (non-destructive): create a throwaway
      over-budget commit and verify the pre-push hook blocks it, then discard:

  ```bash
  # Append enough bytes to push AGENTS.md over 30,000
  python3 -c "print('x' * 2000)" >> AGENTS.md
  git add AGENTS.md
  git commit -m "test: scratch over-budget edit (DO NOT PUSH)"
  git push --dry-run origin HEAD  # the pre-push hook should block this
  git reset HEAD~1 --hard         # discard the scratch commit
  ```

  Acceptance: the dry-run push exits non-zero and the pre-push hook prints the
  instruction-size gate fail message containing "progressive disclosure".

- [x] **6.3** `[AI]` Confirm the original Claude Code 40k warning no longer fires:
      `wc -c CLAUDE.md AGENTS.md` — resolved tree sum must be ≤ 38,000 B.
      Note: AGENTS.md=25,848 B, CLAUDE.md=6,622 B, resolved tree=32,470 B (WARN zone, under 38,000 B fail ceiling).
- [x] **6.4** `[AI]` Stage explicit paths, commit with Conventional Commits, push to
      `ose-public` `origin/main`, and remove the worktree:

  ```bash
  git add apps/rhino-cli/ .husky/pre-push \
    .github/workflows/commons-quality-gate.yml \
    instruction-size-budget.yaml repo-governance/ specs/ AGENTS.md \
    .claude/agents/repo-rules-checker.md
  git commit -m "feat(rhino-cli): add instruction-file size-budget gate"
  git push origin HEAD:main
  git worktree remove worktrees/instruction-file-size-budget-gate
  ```

  Acceptance: `git log origin/main --oneline -1` shows the feat(rhino-cli) commit;
  `ls worktrees/` no longer lists `instruction-file-size-budget-gate`.

- [x] **6.5** `[AI]` Monitor GitHub Actions workflows for the push to `ose-public`
      `origin/main`: run `gh run list --limit 5` to identify the triggered run, then poll with
      `gh run view --json status,conclusion` every 2 minutes (per CI monitoring convention).
      Acceptance: `"conclusion": "success"` for the most recent run triggered by the
      feat(rhino-cli) commit. If any job fails, investigate root cause and push a fix commit
      before starting Phase 7/8.

### Phase 6 Gate

> All checks below must pass before starting Phase 7/8.

- [x] [AI] `git log origin/main --oneline -1` — acceptance: shows the feat(rhino-cli) commit.
- [x] [AI] `gh run view --json status,conclusion` — acceptance: `"conclusion": "success"` for
      the most recent CI run.
- [x] [AI] Worktree removed from `worktrees/instruction-file-size-budget-gate/`.

> **Pause Safety**: All ose-public changes landed on main and CI green. Worktree cleaned up.
> Ready for Part B. Safe to stop. To resume: `git log origin/main --oneline -1`.

---

## Part B — `ose-primer` + `ose-infra` (run **in parallel** after Part A lands)

> Mechanism: copy this plan folder into each sibling repo at the start of its phase so the
> same checklist drives execution there (the multi-repo parity method). `rhino-cli` is ported
> across all three repos, so the validator + config + target + category land in each repo's
> own `rhino-cli` copy. Each repo **fixes its own existing over-budget instruction files**.

### Phase 7 — `ose-primer` propagation `[AI]` (parallel with Phase 8)

- [ ] **7.1** `[AI]` Worktree + baseline in `ose-primer` (`npm install` +
      `npm run doctor -- --fix`); capture its instruction-file sizes (`AGENTS.md`, `CLAUDE.md`,
      resolved tree, `.amazonq/rules/*`). Record under "Baseline sizes (ose-primer)".
- [ ] **7.2** `[AI]` Port the validator + `instruction-size-budget.yaml` + deterministic
      category to primer's `rhino-cli` (mirror Phase 1). Apply the same Phase 1 steps in
      `ose-primer`'s own repo root — same file paths relative to `ose-primer/` root:
      `apps/rhino-cli/src/application/repo_governance/instruction_size.rs` (new),
      `apps/rhino-cli/src/commands/convention_validate_instruction_size.rs` (new),
      `apps/rhino-cli/src/application/repo_governance/audit_orchestrator.rs` (extend),
      `instruction-size-budget.yaml` (new at repo root), same budget numbers, same test
      structure. Command: `nx run rhino-cli:test:unit` in ose-primer — acceptance: all unit
      tests pass including new instruction-size tests.
- [ ] **7.3** `[AI]` Wire pre-push + pre-commit + PR quality gate in primer's own
      `ose-primer/.husky/pre-push` and `ose-primer/.github/workflows/commons-quality-gate.yml`
      (mirror Phase 2). Command:
      `shellcheck .husky/pre-push && actionlint .github/workflows/commons-quality-gate.yml`
      in ose-primer — acceptance: both exit 0.
- [ ] **7.4** `[AI]` **Fix primer's existing violations**: trim primer's `AGENTS.md` (and any
      other over-budget surface) under budget by progressive disclosure (mirror Phase 3 steps
      3.1–3.5, applied to `ose-primer/AGENTS.md`); re-run
      `nx run rhino-cli:instruction-size:validation` in ose-primer — acceptance: exits 0.
- [ ] **7.5** `[AI]` Author/propagate the convention + principle backlink + reference sweep in
      primer's governance tree at
      `ose-primer/repo-governance/conventions/structure/instruction-file-size-budget.md`
      (mirror Phase 4); re-sync bindings with `npm run generate:bindings` in ose-primer.
- [ ] **7.6** `[AI]` Deterministic checker + workflow + specs integration in primer's
      `.claude/agents/repo-rules-checker.md` and
      `ose-primer/repo-governance/workflows/repo/repo-rules-quality-gate.md`; add companion
      Gherkin under `ose-primer/specs/apps/rhino/behavior/` (mirror Phase 5).
      Command: `nx run rhino-cli:specs:coverage` in ose-primer — acceptance: exits 0.
- [ ] **7.7** `[AI]` Verify + commit + push to `ose-primer` `origin/main`; remove worktree.

**Baseline sizes (ose-primer)** (fill in 7.1): _AGENTS.md = \_\_\_\_ B · CLAUDE.md = \_\_\_\_ B
· resolved tree = \_\_\_\_ B_

### Phase 7 Gate

> All checks below must pass before starting Phase 9.

- [ ] [AI] `nx run rhino-cli:instruction-size:validation` (in ose-primer) — acceptance: exits 0.
- [ ] [AI] `nx run rhino-cli:specs:coverage` (in ose-primer) — acceptance: exits 0.
- [ ] [AI] Changes on `ose-primer` `origin/main`.

> **Pause Safety**: ose-primer fully ported and verified. Safe to stop. To resume:
> `nx run rhino-cli:instruction-size:validation` in ose-primer.

### Phase 8 — `ose-infra` propagation `[AI]` (parallel with Phase 7)

> `ose-infra` is a **bare repo with worktrees** — commit to `main` via a worktree; the top
> dir fails `git status`. Private repo; same governance machinery.

- [ ] **8.1** `[AI]` Create/enter an `ose-infra` worktree off `main`;
      `npm install` + `npm run doctor -- --fix`; capture instruction-file sizes. Record under
      "Baseline sizes (ose-infra)".
- [ ] **8.2** `[AI]` Port the validator + config + deterministic category to infra's
      `rhino-cli` (mirror Phase 1). Apply the same Phase 1 steps in `ose-infra`'s own repo
      root — same file paths relative to `ose-infra/` root:
      `apps/rhino-cli/src/application/repo_governance/instruction_size.rs` (new),
      `apps/rhino-cli/src/commands/convention_validate_instruction_size.rs` (new),
      `apps/rhino-cli/src/application/repo_governance/audit_orchestrator.rs` (extend),
      `instruction-size-budget.yaml` (new at repo root), same budget numbers, same test
      structure. Command: `nx run rhino-cli:test:unit` in ose-infra worktree — acceptance: all
      unit tests pass including new instruction-size tests.
- [ ] **8.3** `[AI]` Wire pre-push + pre-commit + PR quality gate in infra's own
      `ose-infra/.husky/pre-push` and
      `ose-infra/.github/workflows/commons-quality-gate.yml` (mirror Phase 2). Command:
      `shellcheck .husky/pre-push && actionlint .github/workflows/commons-quality-gate.yml`
      in ose-infra worktree — acceptance: both exit 0.
- [ ] **8.4** `[AI]` **Fix infra's existing violations**: trim infra's `AGENTS.md` (and any
      other over-budget surface) under budget by progressive disclosure (mirror Phase 3 steps
      3.1–3.5, applied to `ose-infra/AGENTS.md`); re-run
      `nx run rhino-cli:instruction-size:validation` in ose-infra — acceptance: exits 0.
- [ ] **8.5** `[AI]` Author/propagate the convention + principle backlink + reference sweep in
      infra's governance tree at
      `ose-infra/repo-governance/conventions/structure/instruction-file-size-budget.md`
      (mirror Phase 4); re-sync bindings with `npm run generate:bindings` in ose-infra.
- [ ] **8.6** `[AI]` Deterministic checker + workflow + specs integration in infra's
      `.claude/agents/repo-rules-checker.md` and
      `ose-infra/repo-governance/workflows/repo/repo-rules-quality-gate.md`; add companion
      Gherkin under `ose-infra/specs/apps/rhino/behavior/` (mirror Phase 5).
      Command: `nx run rhino-cli:specs:coverage` in ose-infra worktree — acceptance: exits 0.
- [ ] **8.7** `[AI]` Verify + commit + push to `ose-infra` `main` via the worktree; clean up.

**Baseline sizes (ose-infra)** (fill in 8.1): _AGENTS.md = \_\_\_\_ B · CLAUDE.md = \_\_\_\_ B
· resolved tree = \_\_\_\_ B_

### Phase 8 Gate

> All checks below must pass before starting Phase 9.

- [ ] [AI] `nx run rhino-cli:instruction-size:validation` (in ose-infra worktree) —
      acceptance: exits 0.
- [ ] [AI] `nx run rhino-cli:specs:coverage` (in ose-infra worktree) — acceptance: exits 0.
- [ ] [AI] Changes on `ose-infra` `main` via worktree.

> **Pause Safety**: ose-infra fully ported and verified. Safe to stop. To resume:
> `nx run rhino-cli:instruction-size:validation` in ose-infra worktree.

---

## Part C — Cross-repo verification + archival

### Phase 9 — Parity verification + archival `[AI]`

- [ ] **9.1** `[AI]` Confirm gate **mechanics parity** across all three repos: same validator
      surface (`convention instruction-size` + alias), same `instruction-size-budget.yaml`
      numbers, same Nx target name, same pre-push glob gate, same PR-gate step, same
      deterministic preflight category, same checker Step 6 + workflow wiring. Record
      divergences (legitimately repo-specific: which instruction surfaces exist).
- [ ] **9.2** `[AI]` Confirm every repo's `instruction-size:validation` exits 0 and no
      resolved tree exceeds 38,000 B.
- [ ] **9.3** `[AI]` Archive: move the plan folder to
      `plans/done/2026-MM-DD__instruction-file-size-budget-gate/` in `ose-public` (and mirror
      archival in the sibling repos per their convention).

### Phase 9 Gate

> All checks below must pass to close the plan.

- [ ] [AI] `nx run rhino-cli:instruction-size:validation` run in each repo (ose-public,
      ose-primer, ose-infra) — acceptance: exits 0 in all three.
- [ ] [AI] Plan archived in `plans/done/2026-MM-DD__instruction-file-size-budget-gate/` in
      all three repos.

> **Pause Safety**: Three-repo parity verified and plan archived. Work is complete.

---

## Notes

- **Plan-only right now**: this checklist is authored and pushed to `ose-public` `main` as
  documentation. **No implementation is performed yet** — execution begins in a later session.
- **No self-failing gate**: in every repo, the trim phase (3 / 7.4 / 8.4) lands no later than
  the wiring phase so the repo is green when the work is considered done.
- **Parallelism**: Phases 7 and 8 are independent and run concurrently; both depend only on
  Part A having landed on `ose-public` `main`.

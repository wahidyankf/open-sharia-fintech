# Delivery Checklist Validation, Part 1 (Scope 4)

## 4. Delivery Checklist Validation

Steps executable, sequential, granular; validation/acceptance criteria specific and testable; git
workflow specified. Named HARD RULEs (each validated in full detail by a later numbered rule/step
noted below — this section is the summary layer):

- **TDD-shaped steps**: any code-shipping item needs a test-first step (Red→Green→Refactor). Missing
  failing-test step before implementation: **HIGH**. See
  [Test-Driven Development Convention](../../../../repo-governance/development/workflow/test-driven-development.md).
- **TDD phase separation (HARD RULE)**: RED, GREEN, REFACTOR each their own `- [ ]` checkbox — a
  combined checkbox is **HIGH**. See
  [TDD Shape for Delivery Checklists](../../../../repo-governance/development/workflow/test-driven-development/tdd-shape-for-delivery-checklists.md#tdd-shape-for-delivery-checklists).
- **Non-code step format**: non-code steps (docs, config, governance) use
  `[Action verb] [file] — acceptance: [outcome]`, not RED/GREEN/REFACTOR. Misapplied TDD shape:
  **MEDIUM**.
- **Execution-grade clarity (HARD RULE)**: every checkbox names explicit file path(s), verbatim
  shell command(s), and a concrete acceptance criterion — bare "implement X"/"set up Y" is **HIGH**.
  Full detail in `reference/12-rule11-execution-grade-clarity-validation.md` (Step 5e). See
  [Plans Organization Convention §Execution-Grade Clarity](../../../../repo-governance/conventions/structure/plans/execution-grade-clarity.md#execution-grade-clarity-hard-rule).
- **Executor tagging (HARD RULE)**: every checkbox declares `[AI]`/`[HUMAN]`/`[AI+HUMAN]` (unmarked
  = `[AI]`) with a legend at the checklist top; untagged or mis-tagged human-only step: **HIGH**.
  Full detail in `reference/15-rule14-executor-tag-validation.md` (Step 5h).
- **Phase gate and natural pause (HARD RULE)**: every phase ends with `### Phase N Gate`
  (must-pass checklist plus Pause Safety note) at a safe-to-stop state; missing gate: **HIGH**; a
  merge-worthy non-pause phase: **MEDIUM**. Full detail in
  `reference/16-rule15-phase-gate-and-natural-pause-validation.md` (Step 5i).
- **Phase 0 opens no PR (HARD RULE)**: Phase 0 (Environment Setup and Baseline) carries no
  PR-creation, branch-push, PR-Review-Cycle, merge, `gh pr ready`, or post-push CI-verification step
  under any Delivery Mode — earliest PR-opening phase is Phase 1. Flag violations, and any unscoped
  Per-Phase Integration Protocol block, **HIGH**. Full detail below (PR Step Authorization Check) and
  `reference/20-rule19-delivery-mode-validation-part1.md` rule 19 item 7. See
  [Plans Organization Convention §Phase 0 Opens No PR](../../../../repo-governance/conventions/structure/plans/phase-0-opens-no-pr.md#phase-0-opens-no-pr--the-earliest-pr-is-phase-1-hard-rule).
- **PRs open at delivery boundaries, not every phase (HARD RULE)**: a PR opens at each
  **delivery boundary** — the phase after which accumulated work is independently shippable — not
  once per phase; the contiguous phases ending at a boundary form a **delivery unit** mapping to one
  branch, one PR (the worktree stays a coarser per-repository unit, capped at one per repo per plan
  — see
  [Worktree Cap](../../../../repo-governance/conventions/structure/plans/worktree-cap.md#worktree-cap--one-worktree-per-repository-per-plan-hard-rule)).
  Flag **HIGH** an integration step in a non-boundary phase, a change-producing phase absent from
  `### Delivery Boundaries`, or a non-boundary final change-producing phase; flag **MEDIUM** a
  missing `### Delivery Boundaries` table on a non-trivial plan, or a single end-of-plan boundary
  against a `## Parallelization Model` declaring independent parallel nodes. Full detail below and
  `reference/21-rule19-delivery-mode-validation-part2.md` rule 19 item 8. See
  [Plans Organization Convention §PRs Open at Delivery Boundaries](../../../../repo-governance/conventions/structure/plans/prs-open-at-delivery-boundaries-rules.md#prs-open-at-delivery-boundaries-not-every-phase-hard-rule).
- **Specs and Gherkin delivery (Two Paths)**: a plan changing observable behavior in `apps/`,
  `libs/`, or `specs/` needs delivery steps adding/updating companion `specs/` `.feature` files and
  running `specs:coverage`. Full detail in `reference/17-rules16-specs-gherkin-and-regression-test.md`
  rule 16
  (Step 5j). See
  [Feature Change Completeness Convention §Two Paths](../../../../repo-governance/development/quality/feature-change-completeness.md).

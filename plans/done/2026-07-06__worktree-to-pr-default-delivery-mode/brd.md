# Business Requirements — Worktree-to-PR Default Delivery Mode

This document captures **WHY** the default plan-delivery mode should change and why a named
delivery-mode vocabulary is worth introducing. It contains no implementation detail — see
[`tech-docs.md`](./tech-docs.md) for HOW and [`prd.md`](./prd.md) for WHAT.

## Business Goal

Make **review-before-integration** the default path for planned work, while keeping direct-to-trunk
delivery available as an explicit, named choice. Today the default is "worktree → push directly to
`origin main`"; there is no way to name the alternative postures, and no documented precedence for
choosing between them. The goal is a small closed vocabulary of delivery modes with an unambiguous
selection precedence, defaulting to **worktree → PR**.

## Business Motivation

- **Reviewability** — A pull request creates a durable, linkable review surface: the full diff, the
  CI result set, and any discussion live in one place before the change reaches trunk. Direct pushes
  leave no such surface; the change is on `main` the moment it lands. [Judgment call]
- **Safer trunk** — Under worktree → PR, `main` only advances through a deliberate merge action.
  Broken or half-finished work stays on the plan branch, not on trunk. This lowers the blast radius
  of an in-flight plan. [Judgment call]
- **PR-based CI gating** — CI runs against the PR branch throughout execution, so every phase's push
  is validated _before_ it can reach `main`. A red PR simply cannot be merged; a red direct-push has
  already contaminated trunk by the time CI reports. [Judgment call]
- **Named precedence removes ambiguity** — Naming four modes and a precedence order lets a plan (or an
  invoker) state the intended posture explicitly rather than relying on an implicit, undocumented
  default. This mirrors the work-branch precedence already documented and trusted in plan-execution
  Step 0 [Repo-grounded].

## Business Impact

**Pain points addressed**

- No vocabulary today to request "worktree, but deliver via PR" vs "worktree, push to main" vs
  "main checkout, push to main" — every variation must be re-explained in prose per plan. [Judgment call]
- The irreversible trunk write currently happens automatically at each phase push; there is no single
  human checkpoint before trunk advances. [Repo-grounded — direct-push default in
  [`git-push-default.md`](../../../repo-governance/development/workflow/git-push-default.md)]

**Expected benefits**

- One reviewable PR per plan per repo, with CI green as a precondition to the human merge.
- A closed, testable vocabulary that agent checkers can validate (mode present, mode valid).
- Preserved flexibility: the current direct-push behavior remains a first-class, explicitly-named mode.

## Affected Roles

This is a solo-maintainer repository; "roles" here are the hats the maintainer wears and the agents
that consume these governance files. No sign-off ceremony, sponsor, or stakeholder approval applies.

- **Maintainer-as-author** (wears the plan-maker hat) — now declares a `## Delivery Mode` field when
  authoring plans.
- **Maintainer-as-reviewer** (wears the merge-authority hat) — performs the `[HUMAN]` PR merge that
  advances trunk.
- **Consuming agents** — `plan-maker` (emits the field), `plan-checker` (validates it), `plan-fixer`
  (scaffolds it), `plan-execution-checker` (verifies delivery matched the declared mode), and the
  plan-execution workflow (selects the mode by precedence and drives PR gates). All verified present
  under `.claude/agents/` and `repo-governance/workflows/plan/` [Repo-grounded].

## Business-Level Success Metrics

- **Observable**: Every newly authored plan carries a valid `## Delivery Mode` field (checkable by
  `plan-checker`). [Observable fact once shipped]
- **Observable**: The plan-execution workflow documents delivery-mode selection with the same three-tier
  precedence language already used for work-branch selection (grep-verifiable in
  `plan-execution.md`). [Observable fact once shipped]
- **Qualitative**: Trunk advances only through a deliberate human merge for default-mode plans, reducing
  the chance of a broken `main`. [Judgment call — no historical incident count is claimed]

## Business-Scope Non-Goals

- **No change to who holds merge authority beyond making it explicit** — the human already approves
  merges under [`pr-merge-protocol.md`](../../../repo-governance/development/workflow/pr-merge-protocol.md)
  [Repo-grounded]; this plan makes the human merge the default terminal step rather than an opt-in one.
- **No abandonment of Trunk-Based Development** — short-lived plan branches merged frequently via PR
  remain a valid TBD flavor; the plan reconciles the language rather than replacing TBD.
- **No new enforcement engine** — enforcement stays prose-driven via agent checkers, not new
  `rhino-cli` code (see [`tech-docs.md`](./tech-docs.md) open questions if this assumption is revisited).

## Business Risks and Mitigations

| Risk                                                              | Likelihood | Impact | Mitigation                                                                                                                                                                                           |
| ----------------------------------------------------------------- | ---------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Slower delivery from an extra merge step                          | Low        | Low    | The merge is one click; AI drives all gates green beforehand so the human step is trivial. [Judgment call]                                                                                           |
| Perceived conflict with "all development on `main`" TBD wording   | Medium     | Medium | Decision 6: explicitly reframe TBD to include short-lived-branch-via-PR as a valid flavor; update all four TBD-duplication sites. [Repo-grounded — duplication note in `trunk-based-development.md`] |
| Three-repo drift (a mode defined in one repo, missing in another) | Medium     | Medium | Coordinated sweep with per-repo phases and per-repo gates; each repo's checker validates the vocabulary.                                                                                             |
| Binding drift after `.claude/**` edits                            | Medium     | Low    | Mandatory `npm run generate:bindings` step plus a gate that the sync is clean.                                                                                                                       |

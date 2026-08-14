---
title: "Step 7 and 8 — Quality Gate and Delivery"
description: Runs plan-quality-gate per plan to double-zero, then delivers per the selected mode and reports the deviation count summary.
when_to_use: Use when gating and delivering the authored plans, or reporting the run's final outcomes.
---

# Step 7 — Quality Gate (Per Plan, Nested Workflow)

Run [plan-quality-gate](../plan-quality-gate.md) for each created plan in its own repo.

**Workflow**: `plan/plan-quality-gate`

- **Args**: `scope: <plan-folder-path>, mode: {input.gate-mode}, max-concurrency: {input.max-concurrency}`
- **Output**: `final-status` (pass / partial / fail), `final-report`
- **Run**: one gate per plan, up to `max-concurrency` gates in parallel

Each plan must reach `pass` (double-zero: zero CRITICAL/HIGH/MEDIUM findings on two consecutive
checks at the default `strict` gate-mode, or the invoker-specified gate-mode).

**On `partial` or `fail`**: Fix the plan using `plan-fixer` and re-run the gate. Do not deliver
un-gated plans. A plan in `partial` or `fail` state after two re-gate attempts is a blocking
issue — surface it to the invoker before proceeding with delivery of the passing plans.

**Success criteria**: Every plan in the parity set reaches `pass`.

## Step 8 — Delivery and Finalization (Per Mode)

### Part A — Delivery

Commit and deliver per the selected mode.

**Commit guidance** (per [Commit Messages Convention](../../../development/workflow/commit-messages.md)):
Use Conventional Commits format. Split thematically — plan files and rationale docs may be
separate commits. Never commit secrets. Respect each repo's pre-commit and pre-push hooks; do not
bypass them.

Example commit messages:

```
chore(plans): add <objective-slug> parity plan (ose-public)
docs(explanation): add <objective-slug> parity decisions rationale
```

**Per mode**:

- `main-to-origin-main`: Push each repo's commits to `origin main` directly. Not available for any
  bare repo in the set (verify with `git worktree list`, never assume from a fixed repo list) — a
  bare repo has no primary checkout to push from directly; those targets deliver via
  `worktree-to-origin-main` instead.
- `worktree-to-origin-main`: Push each repo's worktree commits to `origin main`. Remove worktrees
  after delivery: `git worktree remove worktrees/<objective-slug> && git worktree prune`.
- `worktree-to-pr` (default): Push branch `plan/<objective-slug>` to each repo. Create or update a
  draft PR per repo via `gh pr create --draft` (skip creation if a PR for that branch already
  exists).

**Success criteria**: All commits land at the intended targets; hooks pass; no secrets committed.

**On push failure**: Surface the error. Do not retry automatically — conflicts require invoker
resolution.

### Part B — Finalization

Report outcomes.

**Output**:

- `plans-created`: One path per target repo
- `gate-results`: plan-quality-gate status per plan (pass / partial / fail)
- `delivery-refs`: Commit SHAs pushed to `origin main` (main modes) or PR URLs (worktree-to-pr)
- Deviation count summary: "N deliberate deviations recorded; 0 silent deviations"

The deviation count summary is the key quality signal. A workflow run that produces zero
deliberate deviations and zero silent deviations has done nothing useful. A run with N deliberate
deviations and zero silent deviations has done exactly what this workflow exists to do.

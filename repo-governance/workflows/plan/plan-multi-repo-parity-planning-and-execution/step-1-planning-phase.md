---
title: "Step 1 — Planning Phase"
description: Runs the nested plan-multi-repo-parity-planning workflow in full, with composite-specific constraints on stage and mode.
when_to_use: Use when executing the composite's first step — authoring and gating one plan per repo before any execution begins.
---

# Step 1 — Planning Phase (Nested Workflow, Sequential)

Run [plan-multi-repo-parity-planning](../plan-multi-repo-parity-planning.md) in full, with
passthrough inputs:

- **Args**: `objective: {input.objective}, repos: {input.repos}, mode: {input.mode},
stage: in-progress, gate-mode: {input.gate-mode}, max-concurrency: {input.max-concurrency}`

All of its steps apply unchanged: parity-set survey, deviation-matrix construction, **first grill
(hard gate — every matrix cell decided)**, conditional web research, **second grill
(post-research)**, per-repo plan authoring via `plan-maker`, per-plan
[plan-quality-gate](../plan-quality-gate.md) to double-zero, and delivery per mode.

**Composite constraints on the nested run**:

- `stage` is fixed to `in-progress` — execution follows immediately, so plans must land in
  `plans/in-progress/<objective-slug>/` in each repo. A backlog parity run does not belong in
  this composite.
- `mode` is restricted to the direct-push modes (`main-to-origin-main`,
  `worktree-to-origin-main`). The `worktree-to-pr` mode leaves plans unmerged and execution MUST
  NOT start on them; if the invoker wants PR review, terminate after the planning phase and
  direct them to the standalone workflows.
- Each authored plan MUST carry its `## Worktree` section (the planning workflow's plan-checker
  gate enforces this) — the execution phase depends on it.

**Output**: One gated, delivered plan per target repo at `plans/in-progress/<objective-slug>/`.

**On failure**: Terminate with status `fail`. Do not start the execution phase with a missing or
un-gated plan.

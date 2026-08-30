---
title: "Step 4 — Execution Phase"
description: Runs plan-execution in full for each repo's gated plan, inheriting its Delivery Mode resolution, worktree gate, Task list expansion, Iron Rules, and archival.
when_to_use: Use when executing the composite's per-repo execution step and needing the exact plan-execution rules that apply.
---

# Step 4 — Execution Phase (Per Repo, Sequential, Nested Workflow)

For each repo in the confirmed order, run [plan-execution](../plan-execution.md) in FULL for
`plans/in-progress/<objective-slug>/` in that repo:

- **Args**: `plan-path: plans/in-progress/<objective-slug>/, max-iterations:
{input.max-iterations}, max-concurrency: {input.max-concurrency}`

Every plan-execution rule applies unchanged, including:

- **Per-repo Delivery Mode resolution**: each repo's plan resolves its own
  [`## Delivery Mode`](../../../conventions/structure/plans/delivery-mode-the-four-modes.md#delivery-mode) independently, via the
  standard three-tier precedence (invocation argument > plan field > `worktree-to-pr` default) —
  distinct from this composite's own `mode` input, which governs only the planning-phase delivery
  of the plan **documents** (Step 1). A repo whose plan resolves to a `*-to-pr` delivery mode
  additionally requires exact-head/base PR CI, one clean current-head
  [`pr-leak-review`](../../pr/pr-leak-review.md), and applicable finite surface gates before that
  repo's merge — its "done" is a green, archival-included PR, not a direct push to `origin main`.
  See [plan-execution.md Step 8](../plan-execution.md).
- **Step 0 worktree gate**: enter the plan's designated worktree (provision from the latest
  `origin/main` if missing), sync it with `origin/main` before any implementation.
- **Task list expansion**: append the repo's delivery checklist to the live Task list as
  flattened tasks per the [Granular Task List Contract](./execution-mode-and-task-list-contract.md#granular-task-list-contract-composite-wide-non-negotiable)
  above, then keep it in sync via the Atomic Sync Ritual for every item.
- **Iron Rules**: granular 1:1 tracking, never stop before all done (except `[HUMAN]` gates),
  fix ALL issues including preexisting, sacred delivery.md, local quality gates before push,
  post-push CI verification, thematic commits, manual behavioral assertions, progress streaming,
  disk-is-truth reconciliation.
- **Validation loop**: `plan-execution-checker` to zero findings (CRITICAL through LOW).
- **Knowledge Capture pre-archival gate**: each repo's plan-execution phase blocks its own archival
  until every `learnings.md` entry is routed inline, recorded in a literal user-authorized
  `plans/ideas/` brief after an overlap scan, marked `Reported without plan authorization`, or
  discarded with reason and both safety gates pass, per the
  [Knowledge Capture Convention](../../../development/quality/knowledge-capture.md) — an attention
  point per repo, not a composite-wide one.
- **Archival and terminal proof**: after the preliminary audit and all pre-archival gates pass,
  resolve `rtk date +%F` once as `<completion-date>`, move the plan to
  `plans/done/<completion-date>__<objective-slug>/`, update indexes, deliver the archival change,
  and require replacement exact-head proof where applicable. After merge or delivery confirmation,
  record the workflow-owned terminal audit in `{final-report}`; only then assign `pass`.
- **Immediate worktree and artifact cleanup after `pass`**: run the full three-class cleanup gate
  in the same session after terminal proof, identity, clean/idle, and no-unpushed proof. Preserve
  diagnostics, purge only plan-local regenerable build output, apply the
  bare-repository branch-order exception when needed, and use non-force exact-path removal with no
  extra prompt. Never use ancestry as a squash-merge proxy; retain, evidence, and escalate if any
  precondition fails.

**Sequencing rule**: one repo at a time. Repo N+1's execution does not start until repo N reaches
`pass` (archival delivered, replacement proof green, terminal audit passed) — or, under a continue-on-failure policy from Step 3, until
repo N is explicitly recorded as `partial`/`fail` and the invoker's policy says continue.

**Continues in** [Step 4 — Execution Phase (Continued)](./step-4-execution-phase-continued.md).

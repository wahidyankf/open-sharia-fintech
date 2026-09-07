---
name: plan-quality-gate
title: "plan-quality-gate"
description: "Governance gate producing exactly one terminal verdict on one formal plan's semantic readiness, from a frozen ledger repaired in at most two cycles."
when_to_use: "Use only when the user explicitly names this gate, or when plan-planning Step 6 invokes it."
goal: Produce one terminal verdict on one formal plan's semantic readiness
termination: "PASS, or a BLOCKED_* verdict after at most one stabilization cycle"
inputs:
  - name: plan-path
    type: string
    description: The formal plan directory under audit
    required: true
  - name: checkpoint
    type: enum
    values: [pre-execution, post-material-change, completion]
    description: The authorized checkpoint this run serves
    required: true
outputs:
  - name: verdict
    type: enum
    values: [PASS, BLOCKED_INPUT_CHANGED, BLOCKED_NON_CONVERGENT, BLOCKED_TOOLING]
    description: The single terminal result
  - name: ledger
    type: file
    pattern: local-tmp/plan/plan-quality-gate__*__ledger.md
    description: The frozen finding ledger
---

# Plan Quality Gate

A [governance gate](../meta/workflow-identifier/governance-gate-class.md), not a `*-check-fix`
workflow. It produces exactly one terminal result for one formal plan and never recurses.

## Authorization

Run only when the user explicitly names this gate or unambiguously directs its semantic audit, or
when one of its three named callers invokes it:
[plan-planning Step 6](./plan-planning/step-6-quality-gate.md),
[plan-multi-repo-parity-planning Step 7](./plan-multi-repo-parity-planning/step-7-and-8-quality-gate-and-delivery.md),
and [web-ux-test-fixing-planning Phase 5](../web/web-ux-test-fixing-planning/phase-5-and-6-quality-gate-and-push.md).
That list is exhaustive; extending it is a rule change. Never infer authorization from creating,
editing, reviewing, or executing a plan, from Plan mode, or from any other workflow. One instruction may authorize several named checkpoints;
otherwise it authorizes one run. This gate never starts another gate run.

## Snapshot and Ledger

Freeze the plan path and stage, the Git revision and dirty paths, scope, relevant specification and
governance paths, unresolved decisions, and cycle `1`. A material change to any frozen input ends
the run as `BLOCKED_INPUT_CHANGED`; it never restarts automatically.

Audit before editing. Record a finite ledger — `ID`, canonical rule, location, material gap,
required repair, proof, and status `OPEN`, `FIXED`, `NOT_APPLICABLE`, or `BLOCKED` — at
`local-tmp/plan/plan-quality-gate__<slug>__ledger.md`. Admit a row only where it violates a rule or
makes scoped execution unsafe, ambiguous, or unprovable; there is no severity, confidence, or mode
threshold. Mandatory findings cannot be waived, and `NOT_APPLICABLE` requires evidence. Preserve the
snapshot, cycle, ledger, pending verification, and authorization across compaction or handoff.

## Bounded Procedure

1. Recursively read the plan, its assets, relevant implementation, specifications, and governance.
   Skip machine-owned concerns entirely.
2. Complete one semantic audit without editing, covering every item of the audit checklist below.
3. Freeze the ledger. Repair only its rows, in dependency and safety order, without expanding
   product scope. A missing decision, absent authority, or irreconcilable rule becomes `BLOCKED`;
   never invent the answer.
4. Re-read only the repaired meaning and its cross-document effects, then run the deterministic
   verification below.
5. Return `PASS` when no row is `OPEN` or `BLOCKED`, tooling passes, no new material semantic gap
   appeared, and the snapshot changed only through recorded repairs.
6. Otherwise allow exactly one stabilization cycle: add only repair-caused semantic gaps and
   deterministic-tool findings, set cycle `2`, repair once, and repeat step 4. A `FIXED` row cannot
   reopen without changed input; changed input yields `BLOCKED_INPUT_CHANGED`.
7. After cycle `2`, return `PASS` if step 5 holds, else `BLOCKED_NON_CONVERGENT` with the remaining
   ledger and evidence. Never repair again, restart, or reinvoke this workflow automatically.

HIPPO capacity recovery is infrastructure handling, not another cycle. Where verification cannot
reach a deterministic verdict, return `BLOCKED_TOOLING` with the failure evidence.

## Terminal Contract

`PASS` authorizes neither execution nor commit and push. Every `BLOCKED_*` result names its reason,
the remaining rows, and the external change required. Resume only after new input and explicit user
direction authorize a fresh run; [plan execution](./plan-execution.md) consumes this result but
never starts it.

## Contents

- [Execution and Delegation](./plan-quality-gate/execution-and-delegation.md) — the read-only checker sweep and root-owned repair.
- [Sufficiency and Ownership](./plan-quality-gate/sufficiency-and-ownership.md) — what PASS asserts, and the checks this gate must never reproduce.
- [Audit Checklist](./plan-quality-gate/audit-checklist.md) — the seven semantic checks of step 2.
- [Deterministic Verification](./plan-quality-gate/deterministic-verification.md) — the tooling this gate consumes and never reproduces.

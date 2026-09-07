---
name: rules-quality-gate
title: "rules-quality-gate"
description: "Read-only governance gate producing one semantic verdict on a proposed or effective repository rule state, handing every finding to rules-propagation."
when_to_use: "Use only when the user explicitly names this gate or unambiguously directs its semantic rule audit."
goal: Produce one read-only semantic verdict for one proposed or effective repository rule state
termination: "PASS_NO_CHANGE or PASS_EFFECTIVE; every finding hands off to rules-propagation and is reported through its terminal result"
inputs:
  - name: mode
    type: enum
    values: [PROPOSAL, EFFECTIVE]
    description: Compare a requested outcome against current rules, or evaluate the repository after propagation edits
    required: true
  - name: outcome
    type: string
    description: The requested rule outcome and its rationale
    required: true
outputs:
  - name: verdict
    type: enum
    values: [PASS_NO_CHANGE, PASS_EFFECTIVE]
    description: The only terminal results this gate can produce
  - name: ledger
    type: file
    pattern: local-tmp/repo-rules/rules-quality-gate__*__ledger.md
    description: The frozen finding ledger handed to propagation
---

# Rules Quality Gate

A [governance gate](../meta/workflow-identifier/governance-gate-class.md), not a `*-check-fix`
workflow. It produces one read-only verdict for one proposed or effective repository rule state,
never edits a rule, and never starts another gate run.
[Rules propagation](./rules-propagation.md) is the sole writer and the mandatory continuation for
any non-passing finding.

## Authorization

Run only when the user explicitly names this gate or unambiguously directs its semantic audit.
Never infer authorization from a rule change, a review request, a propagation run, or another
workflow. Propagation in particular must not call this gate: that edge was removed so the two
workflows form an acyclic pair.

## Modes, Snapshot, and Ledger

Run in exactly one mode. `PROPOSAL` compares the requested outcome with current effective rules
before any edit. `EFFECTIVE` evaluates the repository after propagation has written.

Freeze the mode, requested outcome and rationale, intended normative strength, scope and consumers,
any proposed move or deletion, relevant canonical sources and hierarchy, enforcement route, Git
revision, and dirty paths. A material change to a frozen input returns `BLOCKED_INPUT_CHANGED` to
the caller and never restarts the gate.

Audit without editing. Record a finite ledger — `ID`, canonical source, material semantic gap,
required resolution, evidence, and status `OPEN`, `RESOLVED`, `NOT_APPLICABLE`, or `BLOCKED` — at
`local-tmp/repo-rules/rules-quality-gate__<slug>__ledger.md`. Admit only a rule violation, or a gap
making the requested outcome unsafe, contradictory, undiscoverable, or materially ambiguous. There
is no severity, confidence, or mode threshold. `NOT_APPLICABLE` requires evidence. Preserve the
snapshot, mode, ledger, evidence, and result across compaction or handoff.

## Procedure

1. Inspect only the affected rule, its points of use, relevant higher authority, and directly
   overlapping guidance. Never audit unrelated governance.
2. Complete the semantic audit below without editing.
3. In `PROPOSAL`, return `PASS_NO_CHANGE` when current effective meaning already satisfies the
   request. In `EFFECTIVE`, run the shared
   [deterministic verification](../plan/plan-quality-gate/deterministic-verification.md) and return
   `PASS_EFFECTIVE` only when the ledger is clear and every gate passes.
4. Otherwise emit `NEEDS_PROPAGATION` with the frozen ledger, evidence, and any required external
   decision.

## Terminal Contract

`NEEDS_PROPAGATION` is a non-terminal handoff, never a blocked result. The caller must immediately
run [rules propagation](./rules-propagation.md) with the frozen outcome, ledger, and evidence
without another user instruction, and then report only propagation's terminal result. This gate can
therefore end only in `PASS_NO_CHANGE` or `PASS_EFFECTIVE`. It never repairs a rule, reruns itself,
or authorizes commit and push. Propagation owns any input, conflict, input-change, or tooling
blocker it cannot resolve.

## Contents

- [Sufficiency and Ownership](./rules-quality-gate/sufficiency-and-ownership.md) — what a passing rule asserts, and what this gate must not re-check.
- [Semantic Audit](./rules-quality-gate/semantic-audit.md) — the nine decisions of step 2.
- [Execution and Delegation](./rules-quality-gate/execution-and-delegation.md) — the read-only `rules-checker` sweep.

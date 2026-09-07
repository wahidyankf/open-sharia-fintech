---
description: Worked invocations — a single rule, a batch, a dry run, and a rule that supersedes an existing one.
when_to_use: Use when invoking the workflow and choosing inputs.
---

# Example Usage

## Single rule, default inputs

> Propagate this rule: every bug fix carries a regression test that fails without the fix.

The workflow normalizes it, records both observations, classifies it as a development-layer rule
reachable through the activity it governs, places it in the layer owning testing practice, tidies
the surfaces already gesturing at it, and dispositions it as covered or gated.

## Batch

> Propagate these three rules: <rule> <rule> <rule>

Each is normalized, classified, and placed independently. One may halt while the other two land —
that is a `partial` termination, and the halted rule is named with its blocker.

## Dry run

> Propagate this rule, dry run.

Steps 0 through 5 and Step 7's analysis execute. The manifest reports where the rule would land,
what it would displace, and what it would supersede. Nothing is written and no PR is opened. Use
this when the rule is an instruction-surface candidate and you want to see the eviction before
paying for it.

## Superseding an existing rule

> Propagate this rule, it replaces the current one about worktree isolation.

The caller's supersession claim is a hint, not a decision. Step 3 still runs the scan and applies
layer-aware precedence: if the existing rule sits in a higher layer, the run halts and escalates
rather than accepting the claim.

## Dedicated tree

> Propagate these rules, isolation dedicated.

Use when the rule change is large enough to review on its own, or when the current tree holds work
that must ship separately.

## Strict verification

> Propagate this rule, mode ocd.

Raises the threshold handed to the composed quality gate at Step 8, so lower-severity findings also
block delivery.

## Related Documents

- [Execution Mode](./execution-mode.md) — what the inputs control.
- [Step 0: Intake](./step-0-intake-and-normalization.md) — what happens to the prose.

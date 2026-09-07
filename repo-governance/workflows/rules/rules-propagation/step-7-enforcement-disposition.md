---
description: The mandatory three-way outcome every propagated rule must carry before delivery — covered by an existing gate, newly gated, or unenforced by explicit decision.
when_to_use: Use after the rule is written, before verification, to decide how the rule will be enforced.
---

# Step 7: Enforcement Disposition

A rule nobody checks is decoration that reads like governance. Every propagated rule leaves this
step in exactly one of three states, and **none** of them is silence.

## The Three Dispositions

### 1. Covered

An existing gate already checks this rule. Name the gate and state which of its checks catches the
violating observation recorded at Step 0. A gate that merely operates on the same files is not
coverage — the check must fail when the rule is violated.

Verify the claim rather than asserting it. Confirm the gate fails on a violating input and passes
on a conforming one; a check verified in only one direction is half a check, and the half that is
missing is usually the one that matters.

### 2. Gated

No existing gate covers it, and one is declared for it. Register the gate, declare every required
field including its execution surfaces, and validate the registry before proceeding. Where the gate
needs validator behaviour that does not yet exist, the declaration records the intent and the
implementation is filed as application work — the rule is dispositioned, not blocked.

### 3. Unenforced by Decision

The rule is genuinely a judgement call that no mechanical check can settle. Record it as unenforced
**with its reason**, on the rule itself. This is a legitimate outcome and a rare one; if most rules
in a run take it, Step 0's falsifiability test was applied too gently.

## Assert Exit Codes

Where a disposition is verified by running something, assert its exit code. A validator that emits
no failure token still fails, and a check whose output is piped loses the exit code of everything
but the last stage — both report green through a real failure.

## Output

Per rule: disposition, the gate named or declared, and for unenforced rules, the recorded reason.

## Related Documents

- [Step 8: Verification](./step-8-verification.md) — where the disposition is exercised.
- [Termination Criteria](./termination-criteria.md) — an undispositioned rule blocks termination.

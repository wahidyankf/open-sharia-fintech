---
title: "Step 3: Semantic Sufficiency and Conflict Scan"
description: The pre-write semantic no-op gate, contradiction check, and layer-aware precedence rule.
when_to_use: Use after classification and before placement, whenever a new rule may touch ground an existing rule already covers.
---

# Step 3: Semantic Sufficiency and Conflict Scan

The repository already detects contradictions repository-wide — but only after edits land. This
step runs **before** anything is written, because when a new rule contradicts an old one,
"correct the new rule" is frequently the wrong answer.

## Scan

For each rule, enumerate every existing statement covering its subject. Search by subject term, by
the obligation's verb, and by the surfaces the classification named — three passes, because a rule
restated in different words will not match a single-term search.

Accumulate a whole list item before matching it. A line-oriented search silently misses any rule
whose statement wraps across lines, and the resulting zero reads exactly like "no conflict found".

## Semantic Sufficiency Gate

Before placement, compare the requested outcome with the effective rule set. Evaluate meaning,
strength, audience and scope, boundaries, exceptions, and discoverability—not wording or order.

When the existing effective rules satisfy every dimension, terminate that rule as `no-op`. Record
the canonical source, matching obligation, subject-surface inventory, and verification evidence in
the manifest; produce no tracked diff for that rule. Continue when any material dimension is
missing or weaker. A nearby rule, a wording resemblance, or an undiscoverable obligation is not
sufficient.

## Precedence

When a genuine contradiction is found, the layers decide:

| Existing rule's layer    | Outcome                                                         |
| ------------------------ | --------------------------------------------------------------- |
| Higher than the new rule | **Halt and escalate.** The new rule may not overwrite it.       |
| Same layer               | New rule supersedes; the old statement is retired at Step 6.    |
| Lower than the new rule  | New rule supersedes; every lower statement is amended to match. |

A higher-layer conflict is a genuine governance change — a principle or a vision commitment being
revised — and it is escalated to the human as an explicit choice, never resolved by the run. The
workflow may not edit a higher-layer rule to accommodate a lower-layer one.

## Supersession Record

Every supersession is recorded, not merely applied: which statement was retired, which rule
replaced it, and where the replacement now lives. A rule that silently disappears from the
repository is indistinguishable from a rule that was never written.

## Distinguish Conflict From Overlap

Two rules covering the same subject with compatible obligations are a **duplication** finding for
Step 6, not a contradiction. Only a genuine incompatibility — where following one means violating
the other — triggers precedence.

## Related Documents

- [Step 4: Placement](./step-4-placement-decision.md) — the next step.
- [Termination Criteria](./termination-criteria.md) — how an escalation is reported.

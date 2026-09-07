---
description: Turning free prose into a falsifiable rule statement, and the halt condition when a rule cannot be made falsifiable.
when_to_use: Use at the start of a propagation run, before any classification or placement decision.
---

# Step 0: Intake and Normalization

Rules arrive as prose. This step converts each into a statement the repository can check.

## Normalize

For every rule in the input, produce a single sentence in the imperative, naming its subject, its
obligation, and the condition under which it applies. Strip rationale into a separate `Why` line —
a rule that carries its argument inside its statement cannot be quoted by a gate.

Where the input bundles several obligations into one sentence, split it. Each obligation is
propagated separately, gets its own placement, and gets its own enforcement disposition. Bundled
rules are the most common cause of a rule half-landing.

## Falsifiability Test

Every normalized statement must be checkable **in both directions**. State explicitly:

- What observation proves the rule is being followed.
- What observation proves it is being violated.

A clause that can only pass — "write clear documentation", "be careful with migrations" — fails
this test. So does a clause whose violating observation cannot be made without reading a
contributor's intent.

Beware the false zero: a check that returns nothing because it was pointed at the wrong thing reads
identically to a check that returns nothing because the rule is being followed. If the only
proposed violation-observation is an empty result, the rule is not yet falsifiable.

## Grill

Where a rule fails the test, put the ambiguity back to the human as a concrete choice, not as an
open question. Ask what the violating observation would be. Repeat until the statement passes or
the human rules it unfalsifiable by design.

## Halt Condition

A rule that cannot be made falsifiable **halts** the run for that rule. It is not written as
"guidance", not softened into a suggestion, and not placed anywhere. Other rules in the same batch
continue; the manifest records the halt and its reason.

## Output

A normalized rule set: statement, subject, `Why`, passing observation, violating observation.

## Related Documents

- [Step 2: Classification](./step-2-classification.md) — the next step.
- [Termination Criteria](./termination-criteria.md) — how a halt is reported.

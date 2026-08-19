# Merge-Step Guard (Read First)

## Merge Steps Are Out of Scope for Every Recipe (READ FIRST)

**Before any recipe in this skill, regardless of which finding brought you here**: if the line you
are about to change is a **merge step**, stop. A merge step is a governance gate, not an action
item, and its executor tag **is** the plan's human-gate opt-in.

You may not remove it, retag it, reword it into a scripted command, split it, absorb it into another
step, or delete it to resolve an unverified claim inside it — in any Delivery Mode, at any confidence
level, under any finding type, by any verb. If a finding appears to require one of those, the finding
is a false positive on this line: classify MEDIUM and report it. The only section that may alter a
merge step's tag is [How to Fix a Merge-Tag Mismatch](./pr-review-cycle-and-merge-tag-fixes.md#how-to-fix-a-merge-tag-mismatch),
and that section never retags a merge step away from `[HUMAN]` — its only tag change is one the user
explicitly selects when the existing tag is unrecognized.

This rule is stated here, ahead of every recipe, on purpose. It was previously stated only inside the
merge-tag section, and five consecutive defects reached a merge step through recipes that never
mention merging — each guard was correct on the axis it named and open on an axis nobody had named.
A guard belongs at the point of entry, not in the section a fixer reaches only if it already
suspected the hazard.

**Structural guard (states what it protects, not a tag/verb/mode enumeration)**: no recipe in this
skill, present or future, may remove, retag, or otherwise weaken a merge step's human gate — in ANY
Delivery Mode, by ANY verb (write, delete, replace, rewrite, or merge into an unrelated recipe's
output), under ANY confidence level including HIGH. A merge step's tag is the plan's sole opt-in
declaration for a human-gated merge — there is no separate field recording that intent — so anything
that makes the gate disappear defeats it, regardless of which verb did it or which Delivery Mode the
recipe fired under. This is deliberately stated by what it protects (the human gate) rather than by
enumerating tags, verbs, or modes: two prior cycles were each defeated by a guard that was correct on
the single axis it named — a tag-value set, or a `*-to-pr` mode condition — and silently open on an
axis nobody had named — a delete instead of a retag, or a direct-push mode the guard's wording didn't
reach. Enumerating axes is how this bug keeps recurring; every recipe that could touch a merge step
is scoped by this guard first, and a recipe's own confidence table (however "mechanical" or "HIGH
confidence" it claims to be) is a narrower check layered on top, never a substitute.

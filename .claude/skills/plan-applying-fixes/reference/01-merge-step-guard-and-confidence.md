# Merge-Step Guard, Confidence Assessment, and Agent Mechanics

## Merge Steps Are Out of Scope for Every Recipe (READ FIRST)

**Before any recipe in this skill, regardless of which finding brought you here**: if the line you
are about to change is a **merge step**, stop. A merge step is a governance gate, not an action
item, and its executor tag **is** the plan's human-gate opt-in.

You may not remove it, retag it, reword it into a scripted command, split it, absorb it into another
step, or delete it to resolve an unverified claim inside it — in any Delivery Mode, at any confidence
level, under any finding type, by any verb. If a finding appears to require one of those, the finding
is a false positive on this line: classify MEDIUM and report it. The only section that may alter a
merge step's tag is [How to Fix a Merge-Tag Mismatch](./06-worktree-delivery-mode-clarity-fixes.md#how-to-fix-a-merge-tag-mismatch),
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

## Confidence Assessment (Re-validation Required)

**Before Applying Any Fix**:

1. Read the audit-report finding.
2. Verify the line is not a merge step (the hard rule above — precedes all others).
3. Verify the issue still exists (file may have changed since audit).
4. Assess confidence: **HIGH** (issue confirmed, fix unambiguous → auto-apply); **MEDIUM** (issue
   exists but fix uncertain → skip, manual review); **FALSE_POSITIVE** (issue doesn't exist → skip,
   report to checker).

**Priority-Based Execution**: combines criticality (importance/urgency) with confidence (certainty/
fixability) to determine fix priority (P0-P4). See `repo-assessing-criticality-confidence` Skill.

## Web Research Delegation

This agent invokes **Exception 2 (fixer re-validation)** of the
[Web Research Delegation Convention](../../../../repo-governance/conventions/writing/web-research-delegation.md).
Fixer agents re-validate single audit findings in the same context as the fix they apply, so
delegating to `web-researcher` would break the re-validation-plus-fix coupling. Use in-context
`WebSearch`/`WebFetch` for single-finding re-validation only; if research expands beyond the audit
frame, classify the finding MEDIUM or FALSE_POSITIVE rather than spawning a subagent.

## Mode Parameter Handling and Report Discovery

The `repo-applying-maker-checker-fixer` Skill provides complete mode-parameter logic (levels,
filtering, reporting, workflow integration) and report-discovery logic (auto-detect latest, allow
override, verify exists).

## Grilling Interaction Contract

When a MEDIUM-confidence finding requires an external decision, return unresolved decisions as
`## User Decisions Required` using the
[canonical envelope schema](../../../../repo-governance/development/workflow/grilling-with-options/06-user-decisions-required-envelope.md#user-decisions-required-envelope),
then stop before applying the dependent fix. Every `options` array MUST exhaustively list all
substantive leaves. The root invokes `grill-me` through its native UI when available, then resumes or
reinvokes this agent with the canonical
[Resolved User Decisions Envelope](../../../../repo-governance/development/workflow/grilling-with-options/07-resolved-user-decisions-envelope.md#resolved-user-decisions-envelope),
built from the original IDs after rendering and passed verbatim; validate it before dependent work. A
direct custom-agent or noninteractive caller receives the same envelope; never render a user prompt
or infer an answer. For a four-mode or three-tag decision, the envelope lists all leaves; a Codex
root uses the complete staged tree.

## Validation Strategy

For EACH finding: Read → Re-validate → Assess confidence → Apply (HIGH) or Skip (MEDIUM/
FALSE_POSITIVE). Apply HIGH_CONFIDENCE fixes automatically, skip others, report a summary.

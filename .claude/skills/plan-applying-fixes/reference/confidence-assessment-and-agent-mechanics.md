# Confidence Assessment and Agent Mechanics

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
[canonical envelope schema](../../../../repo-governance/development/workflow/grilling-with-options/user-decisions-required-envelope.md#user-decisions-required-envelope),
then stop before applying the dependent fix. Every `options` array MUST exhaustively list all
substantive leaves. The root invokes `grill-me` through its native UI when available, then resumes or
reinvokes this agent with the canonical
[Resolved User Decisions Envelope](../../../../repo-governance/development/workflow/grilling-with-options/resolved-user-decisions-envelope.md#resolved-user-decisions-envelope),
built from the original IDs after rendering and passed verbatim; validate it before dependent work. A
direct custom-agent or noninteractive caller receives the same envelope; never render a user prompt
or infer an answer. For a four-mode or three-tag decision, the envelope lists all leaves; a Codex
root uses the complete staged tree.

## Validation Strategy

For EACH finding: Read → Re-validate → Assess confidence → Apply (HIGH) or Skip (MEDIUM/
FALSE_POSITIVE). Apply HIGH_CONFIDENCE fixes automatically, skip others, report a summary.

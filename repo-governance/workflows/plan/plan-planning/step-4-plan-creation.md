---
title: "Step 4 — Plan Creation"
description: Describes the plan-maker delegation handoff, the file-impact instruction, and the decision-envelope loop that governs reinvocation.
when_to_use: Use when delegating plan writing to plan-maker, or when resolving a plan-maker decision envelope.
---

# Step 4. Plan Creation (Sequential)

Invoke `plan-maker` to write the plan in the resolved `<plan-dir>` (see [Stage Resolution](./stage-resolution.md#stage-resolution)).

**Agent**: `plan-maker`

Delegate via the Agent tool. Provide a self-contained handoff with:

1. Original user prompt (verbatim)
2. Resolved design decisions from Steps 1 and 3 (numbered decision list)
3. Research findings from Step 2 (cited) — or note that research was skipped
4. Confirmed plan identifier and resolved `<plan-dir>` (normally relative to the worktree root at
   `worktrees/<identifier>/`; include the documented authoring-worktree exception evidence when it
   applies)
5. Confirmed push target and delivery mode (Step 1 item 8)
6. Definition of done (from Step 1)
7. **Explicit instruction**: write the plan directly to the resolved `<plan-dir>` inside the
   matching worktree at `worktrees/<identifier>/`, or inside the user-mandated active authoring
   worktree under the documented exception. For `target-stage=in-progress` this is
   `plans/in-progress/<identifier>/` (no date prefix); for `target-stage=backlog` this is
   `plans/backlog/<identifier>/` (also no date prefix). Do NOT place an
   `in-progress` plan under `backlog/` or vice versa.
8. **File-impact instruction**: make the selected technical form's `## File-Impact Analysis` a
   root-relative, annotated file tree using `[E]`/`[N]`/`[D]`/`[G]` markers. It is the primary scope view; add
   `### More Detail` directly below it only for non-obvious mechanics, ordering, discovery criteria,
   or archival follow-up. Follow [Plans Organization Convention §File-Impact Analysis Format](../../../conventions/structure/plans/file-impact-analysis-format.md#file-impact-analysis-format-hard-rule).
9. **Audience and reasoning instruction**: write a comprehensive evidence-to-delivery record for a
   junior engineer fresh from bootcamp with no professional work experience and no repository or
   stack experience. Each material decision records the selection and two viable alternatives
   (status quo when viable), prior art, evidence, trade-offs, rejection reasons, consequences, and
   revisit triggers. Record real disqualifiers instead of fake alternatives. Omit editorial plan
   history unless it changes the delivered contract.
10. **Structure instruction**: create `README.md`, `brd.md`, `prd.md`, `delivery.md`, and
    `learnings.md`, plus exactly one technical form: `tech-docs.md` or a mapped `tech-docs/`.
    Choose the technical shape by reader jobs and cohesion, never a line threshold.
11. **Delivery instruction**: group cohesive outcomes by acceptance criterion with
    Input/Outcome/Proof, then write one executor-tagged checkbox per independently verifiable action.
    For that junior engineer, include prerequisites, exact paths/symbols or bounded discovery,
    copyable commands, expected
    observations, failure handling, and evidence destinations. Code outcomes use separate detailed
    RED, GREEN, and REFACTOR checkboxes. Keep canonical Gherkin in PRD/spec files and reference it;
    preserve TDD evidence, phase gates, natural delivery seams, PR-size limits, worktree and delivery
    mode, manual verification, operational readiness, governance/C4 reconciliation, and conditional
    recovery dispositions. Useful checklist length is not a defect.
12. **Automatic rule-impact instruction**: apply the complete
    [Automatic Rule-Impact Handoff](./step-4-automatic-rule-impact.md) for every affected
    repository. A workflow link or generic propagation checkbox does not satisfy it.

`plan-maker` emits the final Knowledge Capture phase in `delivery.md` plus a `learnings.md`
scaffold in the plan folder as part of every generated plan, per the
[Knowledge Capture Convention](../../../development/quality/knowledge-capture.md).

**Decision-envelope loop (HARD GATE)**: After every `plan-maker` invocation, inspect its response.
If it returns `## User Decisions Required` in the
[canonical envelope schema](../../../development/workflow/grilling-with-options/user-decisions-required-envelope.md#user-decisions-required-envelope),
the root invokes `grill-me` through the native UI when available (or emits the convention's markdown
fallback to its caller), records the answers by stable decision ID, and resumes or reinvokes
`plan-maker` with them. After rendering, the root MUST construct the canonical
[Resolved User Decisions Envelope](../../../development/workflow/grilling-with-options/resolved-user-decisions-envelope.md#resolved-user-decisions-envelope)
from the original IDs and pass that payload verbatim; `plan-maker` validates it before dependent
work. Repeat until `plan-maker` returns completed artifacts without an envelope.
An envelope is a required checkpoint, not a failure, and MUST NOT skip plan-maker's post-write
validation grill. Macro-decisions from Steps 1 and 3 remain resolved; later envelopes cover only
newly discovered or validation-pass micro-decisions.

**Output**: Plan files created in the resolved `<plan-dir>`.

**On failure**: Terminate with status `fail` only for a technical error. A
`## User Decisions Required` envelope enters the loop above instead.

# Phase Gate and Execution Marker Post-Execution Validation (Step 5f-gates)

## 1. Phase Gate and Execution Marker Post-Execution Validation (Step 5f-gates — MANDATORY)

After verifying worktree usage (Step 5e), validate that execution respected the phase gate barrier
rule and surfaced every `[HUMAN]` step. These conventions are defined at
[Plans Organization Convention §Execution Markers](../../../../repo-governance/conventions/structure/plans/executor-tagging-tags-and-bias.md#executor-tagging--ai-vs-human-hard-rule)
and
[§Phase Gates and Natural Pauses](../../../../repo-governance/conventions/structure/plans/phases-as-natural-pauses.md#phases-as-natural-pauses-with-clear-gates-hard-rule).

### What to Validate

1. **Every `### Phase N Gate` was satisfied before phase N+1 started**
   - Read `delivery.md`. For each phase, confirm its gate checklist items are ticked (or documented as
     verified) before the first step of the next phase is ticked.
   - Check git history for the order in which delivery.md was updated; gate checks should appear in
     commits before the next phase's steps.
   - Evidence missing: **HIGH** finding per phase boundary where ordering cannot be confirmed.
   - Gate items explicitly skipped or commented out without resolution: **CRITICAL** per item.

2. **`[HUMAN]` steps were surfaced — not silently auto-executed or skipped**
   - Identify every `[HUMAN]` marker in `delivery.md`.
   - Confirm in git history or implementation notes that execution paused at each `[HUMAN]` step and
     resumed only after operator confirmation.
   - A `[HUMAN]` step ticked with no implementation note (Date, Status, confirmation evidence):
     **HIGH** finding per step.
   - Evidence that an agent attempted to perform a `[HUMAN]` step autonomously: **CRITICAL** finding.

3. **Each phase reached its Pause-Safety state**
   - For each phase, locate its `> **Pause Safety**:` blockquote. Confirm the described safe-to-stop
     state is verifiable against the post-execution repo (e.g., files exist, commands exit 0).
   - Run the resume command stated in the Pause Safety note and confirm it exits cleanly.
   - Pause Safety state not reached (files missing, commands failing): **HIGH** finding per phase.

### Finding Severity

- Gate items skipped/bypassed without resolution: **CRITICAL**
- Agent auto-executed a `[HUMAN]` step: **CRITICAL**
- Phase gate ordering not confirmed (next phase started before gate was green): **HIGH**
- `[HUMAN]` step ticked without operator confirmation evidence: **HIGH**
- Pause Safety state not verifiable: **HIGH**

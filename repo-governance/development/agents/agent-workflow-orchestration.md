---
title: "Agent Workflow Orchestration Convention"
description: Standards for how AI agents plan, execute, verify, and self-improve during multi-step tasks
category: explanation
subcategory: development
tags:
  - ai-agents
  - workflow
  - orchestration
  - planning
  - verification
  - delegated-agents
created: 2026-03-09
---

# Agent Workflow Orchestration Convention

This document defines how AI agents plan, execute, verify, and improve their work during multi-step tasks. It covers when to enter plan mode, how to use delegated agents, how to manage task state, and how to verify completion before declaring a task done.

## Principles Implemented/Respected

This practice respects the following core principles:

- **[Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md)**: Plan mode requires agents to think before acting. Breaking complex tasks into steps with verification criteria prevents hidden confusion from propagating through multi-step work.

- **[Root Cause Orientation](../../principles/general/root-cause-orientation.md)**: Verification before done enforces the senior engineer standard. The self-improvement loop demands root cause analysis after any mistake rather than moving on.

- **[Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md)**: Delegated agents keep the main context clean by offloading focused subtasks. One task per delegated agent prevents multi-purpose delegated agents that are harder to reason about.

- **[Automation Over Manual](../../principles/software-engineering/automation-over-manual.md)**: Autonomous bug fixing eliminates unnecessary user hand-holding. Agents run tests, read logs, and resolve failures without requiring step-by-step instruction.

## Conventions Implemented/Respected

This practice respects the following conventions:

- **[Content Quality Principles](../../conventions/writing/quality.md)**: Plan documents and lessons files follow active voice, clear structure, and actionable content - not vague notes.

- **[CI Monitoring Convention](../workflow/ci-monitoring.md)**: Agents performing post-push CI verification MUST check every 2-5 minutes via `ScheduleWakeup(delaySeconds=120)` + one `gh run view` per wakeup. `gh run watch` is only safe for jobs <5 min (it polls every ~3s and exhausts the 5,000 req/hour quota on longer jobs). Manual tight-loop polling is forbidden. When rate-limited (HTTP 403): `ScheduleWakeup(delaySeconds=2100)` — not a retry loop.

## When to Plan

Enter plan mode for any non-trivial task. A task is non-trivial if it meets any of these criteria:

- Three or more distinct steps are required
- The task involves architectural decisions or file structure choices
- Multiple files or components will be changed
- The correct approach is not immediately obvious from the request

**When not to plan**: Simple, obvious fixes with a single step and no ambiguity. Documenting a plan for "fix this typo" wastes time without adding clarity.

### Plan Format

Write the plan as a checklist in `local-temp/todo.md`. Each item should be independently verifiable.

```
## Plan: [Brief task description]

- [ ] Step 1 → verify: [how you will know this is done]
- [ ] Step 2 → verify: [how you will know this is done]
- [ ] Step 3 → verify: [how you will know this is done]

## Review

[Added after completion: what worked, what did not, what would change]
```

**Verify before starting implementation**: For significant architectural decisions, check in before executing. For straightforward multi-step tasks, proceed with the plan.

### Re-planning When Things Go Wrong

Stop and re-plan when the current approach is not working. The signal to re-plan is when:

- Multiple consecutive steps produce unexpected results
- A fundamental assumption in the plan turns out to be false
- The approach is technically feasible but increasingly complex

Do not keep pushing forward hoping the situation improves. Stopping to re-plan is faster than accumulating a chain of workarounds.

## Delegated Agent Strategy

Use delegated agents to keep the main context window focused and clean.

### When to Use Delegated Agents

Offload work to delegated agents when:

- **Research and exploration**: Reading many files to understand a codebase section, gathering facts before a decision
- **Parallel analysis**: Multiple independent questions can be answered simultaneously
- **Complex subtasks**: A subtask is large enough to have its own plan

### Delegated Agent Rules

- **One task per delegated agent**: Each delegated agent has a single, focused responsibility. Do not bundle multiple concerns into one delegated agent
- **Use fork skills for structured delegation**: When the task fits a known skill pattern, prefer fork skills over ad hoc delegated agent invocation
- **Return summarized results**: Delegated agents return findings, not raw dumps. The main conversation receives what it needs to make decisions, not everything the delegated agent read

### When Not to Use Delegated Agents

Do not spawn a delegated agent for simple reads or lookups that take one or two tool calls. The overhead is not worth it for small operations.

## Operating Budgets

These budgets bound how agents spend two scarce resources — external API rate limits and token burn — and how repository rules themselves are created and kept in sync. They apply to every agent and to the main conversation, across all three OSE repositories (`ose-infra`, `ose-public`, `ose-primer`).

### Authoring and Propagating Repository Rules

Repository rules and conventions are authored, maintained, and propagated using the `repo-rules-maker` agent. `repo-rules-maker` is the canonical maker for `repo-governance/` content; `repo-rules-checker` validates it and `repo-rules-fixer` applies validated fixes.

A rule that should hold everywhere is created with `repo-rules-maker` in one repo and then carried across the OSE repositories on the bidirectional `ose-primer` sync, so the same rule text lands in `ose-infra`, `ose-public`, and `ose-primer` rather than being retyped by hand per repo.

### Parallelism Budget

Parallelize aggressively — prefer running independent work concurrently over serially, and try to keep the parallel budget fully used whenever independent work is available.

The budget follows the **N+1 model**: `1 main thread + N background agents = N+1 total`. `N` counts concurrent background operations — background delegated agents spawned via the Agent tool, and equivalent token-spending background tasks. The main thread is the `+1`; its own work is not one of the `N`. The **default is `N = 3`**, yielding four concurrently active agents in total.

**Why the default is 3.** N=3 is chosen specifically to **bound token/compute-budget burn** — parallelism is not free, and each background agent independently spends tokens and API quota. Raising N is a **deliberate, justified** act requiring all three of: genuinely independent work available, machine capacity to absorb it, and budget headroom. Lowering N is **required** under budget, runner, or disk pressure.

**Adjustable, never self-promoted.** N may be raised per-plan and **along the way** as conditions change, and a plan declares its chosen N in its `## Parallelization Model` section. An agent MUST NOT silently self-promote beyond the declared N — raising it is an explicit decision, recorded, not an inference an agent draws from its own sense of available headroom.

**Same-machine assumption.** Treat the repository as **very active**: assume other AI agents, software engineers, and background processes are running **simultaneously on the same physical machine**, sharing its disk, its git object store, its worktrees, and its self-hosted CI runners. The N you can safely run is bounded by what that shared machine can absorb alongside everyone else's work, not by what this session alone could drive.

The detailed background-batch mechanics (sequencing, stuck detection, relaunch) live in the [Subagent Orchestration Convention](./subagent-orchestration.md), which specializes the same N.

### DAG-First Orchestration

Every non-trivial task list **and** plan delivery checklist declares an explicit **dependency DAG**: nodes are tasks or checklist items, edges are `blocks` / `blockedBy`. **Independent** nodes run in parallel up to N; **dependent** nodes serialize. The DAG's **independent-node width** — not N — is what the orchestrator actually fans out to; N only caps it.

- **Task lists** express dependencies directly via `blocks` / `blockedBy`.
- **`delivery.md`** expresses phases and steps as a DAG, plus a `## Parallelization Model` section naming which items are concurrent and which are serial. **Cleanup is the terminal node**, depending on every delivery node — it runs last, once nothing else can still need the artifacts it removes.

Determine independence before fanning out, not after. Two nodes are independent only when neither reads what the other writes; a shared output file, a shared branch, or an ordering constraint makes them dependent regardless of how separable they look. The delivery-checklist expression of this rule is documented in the [Plans Organization Convention](../../conventions/structure/plans.md).

### Background-Slot Preference

Fill the **background** slots up to N and keep the **main thread vacant** and responsive — the main thread is the **orchestrator**, background agents are the **workers**. This is **bounded by the DAG**: fan out only genuinely independent nodes, and never split dependent work artificially to raise slot utilization.

### Harness Capability Gating

Not every coding-agent harness can run background or parallel subagents. The model above is stated so that it degrades cleanly rather than becoming inapplicable:

> Where the harness supports background or parallel subagents, execute the DAG's independent nodes concurrently, each in its own git worktree (or equivalent isolated branch checkout), respecting the harness's own documented concurrency ceiling if one exists. Where the harness does NOT support background/parallel subagents, execute the same DAG **serially**, node by node, in dependency order — one worktree/branch at a time is fine (serial execution has no concurrent-edit collision to isolate against). In both modes, the delivery-safety rules (no destructive git operations, worktree cleanup on completion, no direct pushes to protected branches) apply **identically** regardless of concurrency mode.

The DAG itself is the portable artifact: the same dependency graph drives a wide fan-out on a background-capable harness and a serial walk on a single-threaded one. Concurrency changes the schedule, never the ordering or the safety rules.

### The PR Is the Independent Merge Point

`worktree-to-pr` is the default delivery mode (see [Delivery Mode](../../conventions/structure/plans.md#delivery-mode)), and the reason is a parallelism reason, not a review-process one.

A worktree isolates **edits** — two agents writing to the same file in the same checkout would collide, and separate working trees prevent that. But isolated edits still have to land, and if N parallel units all funnel into one shared branch or one shared PR, they re-serialize at exactly the moment that matters. The **PR** is what makes them genuinely independent: N parallel units become **N PRs that review, gate, and merge independently**, none blocking any other. A slow review on one unit does not hold the other N-1 hostage.

Concretely: **every DAG leaf that produces changes gets its own worktree and its own PR** — a strict one-node ↔ one-worktree ↔ one-PR mapping. The corollary matters as much as the rule: nodes that are genuinely _dependent_ stay in one PR. The DAG governs. Never force-split an inseparable chain just to produce more PRs, and never batch independent nodes into one PR just to produce fewer.

Because the worktree is the unit that maps to a PR, it is also the unit that gets cleaned up when that PR lands.

### CI and GitHub Actions Monitoring Cadence

When monitoring or polling CI or GitHub Actions — run status, job logs, or workflow conclusions — never poll faster than once every two (2) minutes. This is a hard floor that protects the provider's rate limiter, which takes longer to recover from than simply waiting. The operational default is more conservative still: see the [CI Monitoring Convention](../workflow/ci-monitoring.md) for the required mechanics — scheduled wakeups, a single status check per wakeup, no stream-watching, and rate-limit recovery.

## Verification Before Done

Never declare a task complete without proving it works.

### Verification Requirements

Before marking any task complete:

1. **Run the relevant tests** - If code changed, tests must pass
2. **Check logs for errors** - Silent failures are still failures
3. **Demonstrate the behavior** - Show that the output matches the requirement, not just that the code was written
4. **Apply the senior engineer test** - Ask "would a senior engineer approve this?" If not, keep working

### Verification for Different Task Types

| Task Type            | Verification Method                                         |
| -------------------- | ----------------------------------------------------------- |
| Code change          | Run `nx run [project]:test:quick`, check no regressions     |
| Documentation update | Verify links work, content renders correctly                |
| Bug fix              | Show the failing test now passes; existing tests still pass |
| Refactor             | All tests pass before and after; behavior unchanged         |
| New feature          | Tests cover the new behavior; edge cases handled            |

### Diffs and Behavior Comparison

When a change might have unintended side effects, compare behavior before and after. This is especially relevant for:

- Changes to shared utilities used by many consumers
- Changes to configuration that affects build or test behavior
- Refactors touching core logic

## Autonomous Bug Fixing

When given a bug report, fix it. Do not ask for hand-holding.

### Expected Behavior

- Point at the error message, log output, or failing test
- Read the relevant code to understand the cause
- Apply the fix
- Verify the fix works
- Report what was done and why

### What Autonomous Means

Autonomous does not mean undisclosed. Agents must:

- Explain what root cause was found
- Describe the fix applied and why it addresses the root cause
- Report any edge cases considered
- Flag anything that warrants user awareness

Autonomous means no unnecessary questions when the path forward is clear. It does not mean working silently without communicating findings.

### Failing CI Tests

When CI tests fail, fix them without being told how. The steps are:

1. Read the test output to identify which tests fail and why
2. Read the failing test code and the code it tests
3. Determine the root cause (broken code, broken test, or environment issue)
4. Apply the fix
5. Verify locally before reporting completion

### Preexisting Errors Discovered During Other Work

Autonomous bug fixing applies not only when a bug report is the primary task, but also when broken state is discovered incidentally during any other work. An agent that opens a file to add a feature and finds a broken import, a failing test, or an incorrect configuration is responsible for fixing it.

The required behavior is identical whether the error was assigned or discovered:

1. Diagnose the root cause before proceeding with the primary task
2. Fix the root cause — not around it, not in a note at the end of a response
3. Verify the fix works
4. Communicate what was found and what was fixed

Scope judgment determines commit strategy: small fixes go inline, medium fixes get their own commit, large fixes require a plan in `plans/in-progress/` with execution underway.

See [Proactive Preexisting Error Resolution](../../development/practice/proactive-preexisting-error-resolution.md) for the full practice including the three anti-patterns to avoid (acting ignorant, monkey-patching, passive mentioning) and the complete agent checklist.

## Demand Elegance (Balanced)

For non-trivial changes, pause and ask: "Is there a more elegant way to do this?"

If a solution feels hacky, reframe the task: "Knowing everything I now know, what is the elegant solution?" Then implement that instead.

**When to skip this step**: Simple, obvious fixes with a single clear approach. Do not over-engineer a one-line correction.

**Elegance is not complexity**: The more elegant solution is usually simpler, not more abstract. The question is whether the current approach is unnecessarily convoluted, not whether a more sophisticated pattern could be applied.

## Self-Improvement Loop

After any correction from the user, extract the lesson.

### The Process

1. **Identify the pattern**: What category of mistake was made? (misread requirement, wrong assumption, insufficient verification, scope creep, etc.)
2. **Write a rule**: Write a concrete rule in `local-temp/lessons.md` that would prevent this mistake
3. **Iterate**: After repeated mistakes of the same type, revise the rule until the mistake stops occurring
4. **Review at session start**: Check `local-temp/lessons.md` at the beginning of work on a project to activate relevant lessons

### Lessons File Format

```markdown
## Lessons

### [Date] - [Category]

**Mistake**: [What went wrong]
**Rule**: [Specific, actionable rule to prevent recurrence]
**Context**: [What triggered this lesson]
```

### What Makes a Good Lesson

A useful lesson is specific and actionable:

```
FAIL: "Be more careful when reading requirements."

PASS: "When a requirement says 'update the index', read the existing index first
      to understand its structure before making changes. Assumptions about format
      have caused overwrites twice."
```

Rules that are too general provide no guidance when the situation arises again. Rules that name the specific failure mode and the specific check to perform are actionable.

## Task Management

### Plan First

Write the plan before starting implementation. This is not optional for non-trivial tasks.

### Track Progress

Mark items complete as you go. An updated checklist shows what has been done and what remains. This matters when tasks are interrupted or when reporting progress.

### Use Granular Task Items

Each item in a task list or plan checklist must represent one independently completable unit of work. This applies to `local-temp/todo.md` plans and to any checklist an agent produces in delivery plans.

**Rule**: One item = one concrete action. Never bundle multiple steps behind a single checkbox.

**Bad** (too coarse):

```markdown
- [ ] Add coverage merging with all formats and tests
```

**Good** (granular):

```markdown
- [ ] Create `internal/testcoverage/merge.go` with format-agnostic merge logic
- [ ] Implement `CoverageMap` type for normalized per-line data
- [ ] Add parsers to return `CoverageMap` from each format
- [ ] Write unit tests for merge logic (same format, cross-format, overlapping)
```

**Why this matters**:

- Progress visibility during long-running operations — each completed item is observable progress
- Resume capability when context is compacted — a granular list shows exactly where execution stopped
- Clear audit trail — coarse items leave ambiguity about what was actually done

**Test for granularity**: Can you verify the item is done without completing anything else on the list? If the answer is no, split it.

### Use the Task Tool for Multi-Step Work

When working on tasks with multiple steps, agents MUST use `TaskCreate` and `TaskUpdate` to track progress programmatically. This is in addition to updating markdown checklists.

- **TaskCreate**: Create a task for each granular work item before starting
- **TaskUpdate** (`in_progress`): Mark the task when you begin working on it
- **TaskUpdate** (`completed`): Mark the task when it is done

This provides real-time progress tracking that survives context compaction and makes the agent's work observable to the user without needing to read files.

### Document Results

Add a review section to `local-temp/todo.md` after completing the task. The review captures:

- What the task accomplished
- Any significant decisions made during execution
- Anything that should inform future similar tasks

### Capture Lessons

After any correction, update `local-temp/lessons.md`. This is the direct application of the self-improvement loop to task management.

## Anti-Patterns

### Pushing Through When Lost

**Problem**: Continuing to implement when the approach is clearly not working, hoping it resolves itself.

**Why it fails**: Each step based on a flawed premise compounds the problem. Re-planning from a known-good state is always faster than accumulating a chain of adjustments to a broken foundation.

**Fix**: Stop. Re-plan. State explicitly what assumption failed and what the revised approach is.

### Premature Completion

**Problem**: Declaring a task done when tests pass, without verifying the actual behavior.

**Why it fails**: Tests are necessary but not sufficient. Verification requires demonstrating that the correct behavior is present, not just that no existing test fails.

**Fix**: After tests pass, demonstrate the behavior directly. Read the output. Confirm it matches the requirement.

### Context Bloat

**Problem**: Conducting extensive research and exploration in the main context rather than using delegated agents.

**Why it fails**: The main context fills with details that were needed for the research but are not needed for the decision. This degrades the quality of subsequent reasoning.

**Fix**: Offload research to delegated agents. Return only the findings needed to make the decision.

### Vague Lessons

**Problem**: Writing lessons that describe the mistake in general terms without specifying a concrete preventive action.

**Why it fails**: A vague lesson is easy to write and easy to ignore. When the same situation arises, the lesson provides no actionable check.

**Fix**: Write rules that name the specific trigger and the specific check. Test the rule against the original failure: "Would this rule have prevented the mistake?"

## References

**Related Principles:**

- [Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md) - Think before acting; surface assumptions
- [Root Cause Orientation](../../principles/general/root-cause-orientation.md) - Fix root causes; minimal impact; senior engineer standard
- [Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md) - Simple delegated agent structures; focused responsibilities

**Related Practices:**

- [Implementation Workflow](../workflow/implementation.md) - Make it work, make it right, make it fast; surgical changes; goal-driven execution
- [Maker-Checker-Fixer Pattern](../pattern/maker-checker-fixer.md) - Multi-agent orchestration for content quality workflows
- [AI Agents Convention](./ai-agents.md) - Agent structure, frontmatter, and tool access standards
- [Skill Context Architecture](./skill-context-architecture.md) - Inline vs fork skills for delegated agent invocation
- [Subagent Orchestration Convention](./subagent-orchestration.md) - Concurrency cap (max 2 simultaneous background Agent-tool spawns) and 3-minute stuck-detection polling for background subagents; specializes the delegated agent model for background execution
- [CI Post-Push Verification Convention](../workflow/ci-post-push-verification.md) - Trigger and monitor CI after every push; required final step in plan execution
- [CI Monitoring Convention](../workflow/ci-monitoring.md) - Check every 2-5 min via ScheduleWakeup; `gh run watch` only for <5 min jobs; rate-limit recovery uses `ScheduleWakeup(delaySeconds=2100)`

**Related Agents / Workflows:**

- `plan-maker` - Creates structured plans following the plan format in this convention
- [plan-execution workflow](../../workflows/plan/plan-execution.md) - Execute plans with progress tracking and verification (calling context orchestrates; no dedicated delegated agent)

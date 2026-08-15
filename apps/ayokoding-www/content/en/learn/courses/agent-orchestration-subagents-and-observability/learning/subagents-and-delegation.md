---
title: "Subagents and Delegation"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 10
---

Theme A covers source Examples 1–12. Every artifact is a credential-free local simulation; no browser
or `remotebrowser` dependency is required.

### Example 1: Demonstrate a Single-Agent Limit

**Brief explanation**: One context budget cannot hold every detail of an oversized task.

**Code**: Run `python3 code/ex-01-single-agent-limit-demo/example.py`.

**Expected observation**: The local task exceeds its fixed budget.

**Key takeaway**: Limits motivate bounded delegation.

**Why it matters**: More context is not a substitute for task decomposition.

### Example 2: Delegate to a First Subagent

**Brief explanation**: A subagent receives a bounded task and returns only a summary.

**Code**: Run `python3 code/ex-02-first-subagent/example.py`.

**Expected observation**: The parent receives `summary` rather than detail.

**Key takeaway**: A subagent is an isolation boundary.

**Why it matters**: Parent context remains focused on the larger goal.

### Example 3: Prove Context Isolation

**Brief explanation**: Parent state keeps a short result, not a subagent exploration transcript.

**Code**: Run `python3 code/ex-03-context-isolation-proof/example.py`.

**Expected observation**: Parent tokens stay below child-detail tokens.

**Key takeaway**: Summaries preserve parent budget.

**Why it matters**: Isolation prevents every parallel investigation from bloating the coordinator.

### Example 4: Decide a Delegation Boundary

**Brief explanation**: Delegate work that is bounded and summarizable; retain irreducible detail.

**Code**: Run `python3 code/ex-04-delegation-boundary-decision/example.py`.

**Expected observation**: Research is delegated and final synthesis stays local.

**Key takeaway**: Delegation is a design judgment.

**Why it matters**: A poorly chosen subagent merely moves the context problem.

### Example 5: Scope a Subagent's Tools

**Brief explanation**: A subagent receives only the small tool set its task needs.

**Code**: Run `python3 code/ex-05-subagent-with-own-tools/example.py`.

**Expected observation**: The agent exposes `search` but not `write`.

**Key takeaway**: Context isolation and authority scoping work together.

**Why it matters**: A specialist does not need every system capability.

### Example 6: Check Summary Fidelity

**Brief explanation**: A summary must preserve decisions that the parent needs next.

**Code**: Run `python3 code/ex-06-summary-fidelity/example.py`.

**Expected observation**: The required decision appears in the summary.

**Key takeaway**: Brevity must not erase decision-relevant information.

**Why it matters**: An incomplete summary causes avoidable parent rework.

### Example 7: Fall Back after Subagent Failure

**Brief explanation**: A parent turns a worker error into a controlled fallback.

**Code**: Run `python3 code/ex-07-subagent-failure-fallback/example.py`.

**Expected observation**: The result uses the fallback summary.

**Key takeaway**: One failed worker need not collapse the run.

**Why it matters**: Failure handling is an orchestration responsibility.

### Example 8: Bound Nested Subagents

**Brief explanation**: A child may delegate, but nesting must have an explicit depth limit.

**Code**: Run `python3 code/ex-08-nested-subagents/example.py`.

**Expected observation**: Depth two is allowed and depth three is rejected.

**Key takeaway**: Delegation trees need a stopping rule.

**Why it matters**: Unbounded recursion creates opaque cost and latency.

### Example 9: Diagram Subagent Isolation

**Brief explanation**: The artifact records the parent-to-child task and child-to-parent summary flow.

**Code**: Run `python3 code/ex-09-subagent-diagram/example.py`.

**Expected observation**: The local flow lists `task → subagent → summary`.

**Key takeaway**: Isolation is a directional information boundary.

**Why it matters**: A diagram helps distinguish delegation from shared mutable state.

### Example 10: Research then Implement

**Brief explanation**: A research subagent returns evidence, while the parent implements from the summary.

**Code**: Run `python3 code/ex-10-research-then-implement/example.py`.

**Expected observation**: The implementation uses only the summary field.

**Key takeaway**: Parent and child roles should have distinct outputs.

**Why it matters**: Clear handoffs make the run reviewable.

### Example 11: Measure Delegation Cost

**Brief explanation**: Delegation has a coordination cost that must be compared with inline work.

**Code**: Run `python3 code/ex-11-delegation-cost-tradeoff/example.py`.

**Expected observation**: The delegated run has greater local overhead.

**Key takeaway**: More agents are not automatically faster or cheaper.

**Why it matters**: Orchestrate only when isolation or parallelism pays for itself.

### Example 12: Keep an Unsummarizable Task Local

**Brief explanation**: A task whose critical detail cannot survive compression remains with the parent.

**Code**: Run `python3 code/ex-12-when-not-to-delegate/example.py`.

**Expected observation**: The local decision is `keep`.

**Key takeaway**: Not every hard task should become a subagent task.

**Why it matters**: Delegation has value only when its summary boundary is sound.

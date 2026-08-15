---
title: "Beginner Examples"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 10
---

Each survey entry has five labeled parts: Brief, Diagram, Survey, Key takeaway, and Why it matters.

### Example 1: Agent vs Workflow

**Brief**: An agent chooses actions from observations; a workflow follows a predefined path.

**Diagram**: `observation → choose → act → observation` versus `step 1 → step 2`.

**Survey**: Use the fixed workflow when the path is known.

**Key takeaway**: A model call alone does not make a system agentic.

**Why it matters**: Unneeded autonomy increases cost and failure modes.

### Example 2: Workflow Predefined Path

**Brief**: A workflow declares transitions before it runs.

**Diagram**: `input → fixed model step → output`.

**Survey**: Reserve dynamic choice for tasks with genuine uncertainty.

**Key takeaway**: Prefer deterministic orchestration when it is sufficient.

**Why it matters**: Explicit paths are easier to test and audit.

### Example 3: Augmented LLM

**Brief**: Retrieval, tools, and memory augment a base model.

**Diagram**: `model ← context | tools | memory`.

**Survey**: Treat every augmentation as a separate application boundary.

**Key takeaway**: Capability and responsibility grow together.

**Why it matters**: Boundaries need validation and authority controls.

### Example 4: Tool Definition

**Brief**: A tool exposes a typed name, description, and input schema.

**Diagram**: `model → schema → validated tool`.

**Survey**: The application owns schema and authorization.

**Key takeaway**: Tool calls are data, not executable authority.

**Why it matters**: Typed schemas reject malformed requests early.

### Example 5: Tool Choose Invoke

**Brief**: A model may propose the appropriate offered tool.

**Diagram**: `proposal → validate → invoke`.

**Survey**: Validate before every invocation.

**Key takeaway**: Selection never bypasses application policy.

**Why it matters**: Unchecked calls can cross authority boundaries.

### Example 6: Parse Tool Call

**Brief**: Parse structured tool input before dispatching.

**Diagram**: `JSON → parser → handler`.

**Survey**: Reject invalid fields rather than repairing guesses.

**Key takeaway**: Dispatch follows validation.

**Why it matters**: Parsing is a security boundary.

### Example 7: Two Tools Choose

**Brief**: Multiple tools require a constrained choice.

**Diagram**: `intent → allowed tool set → one call`.

**Survey**: Expose only tools needed for the task.

**Key takeaway**: Least authority applies to tool menus.

**Why it matters**: Smaller tool surfaces reduce harmful choices.

### Example 8: Agentic Loop Steps

**Brief**: A loop cycles request, tool use, result, and decision.

**Diagram**: `request → tool_use → tool_result → repeat`.

**Survey**: This is vocabulary, not a runtime implementation.

**Key takeaway**: Each loop needs an explicit stop path.

**Why it matters**: Bounded control prevents runaway work.

### Example 9: Loop Stop Reason

**Brief**: A stop reason decides whether the next iteration is legal.

**Diagram**: `tool_use? yes: continue; no: stop`.

**Survey**: Check stop state before another action.

**Key takeaway**: Termination is part of correctness.

**Why it matters**: Missing stops create unbounded spend.

### Example 10: Client vs Server Tools

**Brief**: Client tools and server tools execute in different trust zones.

**Diagram**: `client action | server action`.

**Survey**: Route implementation depth to agent-tools-and-mcp.

**Key takeaway**: Execution location changes authority.

**Why it matters**: Trust boundaries must be explicit.

### Example 11: ReAct Interleave

**Brief**: ReAct interleaves a decision with an observable action.

**Diagram**: `decide → act → observe`.

**Survey**: Record action traces, not private reasoning.

**Key takeaway**: Observability should focus on behavior.

**Why it matters**: Action traces support safe debugging.

### Example 12: ReAct Trace

**Brief**: A trace links a decision to its next tool action.

**Diagram**: `question → action → evidence`.

**Survey**: Make tool results inspectable.

**Key takeaway**: Evidence should precede an answer.

**Why it matters**: Traceability exposes incorrect actions.

### Example 13: Chain of Thought

**Brief**: Intermediate reasoning can guide a task.

**Diagram**: `prompt → intermediate work → answer`.

**Survey**: Do not expose hidden reasoning as an application API.

**Key takeaway**: Validate outputs, not private thoughts.

**Why it matters**: Output contracts remain the stable interface.

### Example 14: CoT Exemplars

**Brief**: Examples can demonstrate a reasoning format.

**Diagram**: `example pattern → constrained response`.

**Survey**: Keep examples task-specific and minimal.

**Key takeaway**: Exemplars steer format, not truth.

**Why it matters**: Inputs still require evidence checks.

### Example 15: Plan and Execute

**Brief**: A planner proposes a sequence before action.

**Diagram**: `plan → one approved step → observe`.

**Survey**: Follow the-agent-loop for implementation.

**Key takeaway**: Plans are hypotheses, not authority.

**Why it matters**: Results can invalidate a plan.

### Example 16: Executor Step

**Brief**: An executor completes one validated step.

**Diagram**: `approved step → tool → result`.

**Survey**: Separate step validation from execution.

**Key takeaway**: Small actions constrain blast radius.

**Why it matters**: Incremental work localizes failure.

### Example 17: Planner vs ReAct

**Brief**: Planning batches decisions; ReAct decides per observation.

**Diagram**: `plan once | observe each step`.

**Survey**: Choose based on dependency uncertainty.

**Key takeaway**: Call count is a design tradeoff.

**Why it matters**: More calls increase latency and cost.

### Example 18: Reflection Loop

**Brief**: Reflection critiques an outcome before one retry.

**Diagram**: `result → critique → bounded retry`.

**Survey**: Limit retries with a budget.

**Key takeaway**: Reflection is controlled remediation.

**Why it matters**: Unlimited self-critique loops do not converge reliably.

### Example 19: Reflexion Memory

**Brief**: Episodic feedback can inform a later attempt.

**Diagram**: `outcome → lesson → next context`.

**Survey**: Store only scoped, useful feedback.

**Key takeaway**: Memory needs retention policy.

**Why it matters**: Unbounded feedback becomes stale context.

### Example 20: Short Term Memory

**Brief**: A thread transcript preserves local conversation state.

**Diagram**: `thread → checkpoint → next turn`.

**Survey**: Route durable storage to agent-context-and-memory.

**Key takeaway**: Scope context to the active task.

**Why it matters**: Thread mixing leaks irrelevant data.

### Example 21: Thread ID

**Brief**: A thread identifier separates concurrent conversations.

**Diagram**: `thread A | thread B`.

**Survey**: Use identifiers as isolation boundaries.

**Key takeaway**: Context must not cross thread scope.

**Why it matters**: Isolation protects correctness and privacy.

### Example 22: Long Term Memory

**Brief**: Long-term memory survives a session boundary.

**Diagram**: `session → store → later session`.

**Survey**: Define retention and retrieval rules first.

**Key takeaway**: Persistence is a product decision.

**Why it matters**: Stored data creates privacy obligations.

### Example 23: Memory Retrieval

**Brief**: Retrieval selects prior information for current context.

**Diagram**: `query → memory search → context`.

**Survey**: Retrieve relevance, not every record.

**Key takeaway**: Memory is useful only when scoped.

**Why it matters**: Excess context harms focus and cost.

### Example 24: Context Relevance

**Brief**: Relevance pruning removes stale or unrelated context.

**Diagram**: `candidate context → rank → prompt`.

**Survey**: Prefer evidence tied to the current task.

**Key takeaway**: More context is not automatically better.

**Why it matters**: Irrelevant context can mislead an agent.

### Example 25: Prompt Chaining

**Brief**: One validated output can feed a later call.

**Diagram**: `call one → validate → call two`.

**Survey**: Keep the handoff schema explicit.

**Key takeaway**: Chaining composes bounded steps.

**Why it matters**: Validation prevents error propagation.

### Example 26: Routing

**Brief**: Routing selects a specialized handler for an input.

**Diagram**: `classify → route → handler`.

**Survey**: Use deterministic routing where possible.

**Key takeaway**: Route policy is application logic.

**Why it matters**: Wrong routing can invoke excess authority.

### Example 27: Parallelization Sectioning

**Brief**: Independent subtasks can execute concurrently.

**Diagram**: `task → independent branches → join`.

**Survey**: Route implementation to agent-orchestration-subagents-and-observability.

**Key takeaway**: Parallelism requires independent inputs and bounded joins.

**Why it matters**: Hidden dependencies duplicate work or corrupt shared state.

---
title: "Advanced Examples"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 30
---

Advanced survey entries retain five parts—**Brief**, **Diagram**, **Survey**, **Key takeaway**, and **Why it matters**—and link implementation depth to the owner.

### Example 56: Eval Dataset

**Brief**: A dataset states task inputs and expected outcomes. **Diagram**: `cases → scorer`. **Survey**: Deep eval authoring is forward-linked. **Key takeaway**: Cases define measured behavior. **Why it matters**: Unrepresentative cases mislead. [Forward link](../../evaluating-ai-systems-in-depth/learning/overview).

### Example 57: Evals in CI

**Brief**: CI can run an eval gate. **Diagram**: `change → eval → gate`. **Survey**: Do not implement the pipeline here. **Key takeaway**: Regression checks are automated. **Why it matters**: Manual checks miss regressions. [Forward link](../../evaluating-ai-systems-in-depth/learning/overview).

### Example 58: Regression Bar

**Brief**: A minimum score blocks regressions. **Diagram**: `score < bar → fail`. **Survey**: Calibrate bars in deep evals. **Key takeaway**: Thresholds encode product policy. **Why it matters**: Silent quality drops reach users. [Forward link](../../evaluating-ai-systems-in-depth/learning/overview).

### Example 59: Agent Span

**Brief**: A span records an agent invocation. **Diagram**: `invoke → span`. **Survey**: Trace ownership belongs to observability. **Key takeaway**: Operations need identifiers. **Why it matters**: Traces localize failures. [Forward link](../agent-orchestration-subagents-and-observability/learning/overview).

### Example 60: Tracing Attributes

**Brief**: Attributes describe a model operation. **Diagram**: `span → attributes`. **Survey**: Avoid recording secrets. **Key takeaway**: Structured attributes enable filtering. **Why it matters**: Unstructured logs are hard to diagnose. [Forward link](../agent-orchestration-subagents-and-observability/learning/overview).

### Example 61: OTel Development Status

**Brief**: GenAI conventions can change before stabilization. **Diagram**: `draft convention → versioned adapter`. **Survey**: Isolate volatile telemetry fields. **Key takeaway**: Standards status affects design. **Why it matters**: Direct coupling makes upgrades risky. [Forward link](../agent-orchestration-subagents-and-observability/learning/overview).

### Example 62: Prompt Injection Direct

**Brief**: A user prompt can attempt to override policy. **Diagram**: `untrusted input → guard`. **Survey**: Treat content as data. **Key takeaway**: Model text is not authority. **Why it matters**: Direct attacks redirect actions. [Forward link](../agent-permissions-and-sandboxing/learning/overview).

### Example 63: Prompt Injection Indirect

**Brief**: Tool output can contain hostile instructions. **Diagram**: `tool result → untrusted context`. **Survey**: Do not elevate retrieved text. **Key takeaway**: Indirect input is still untrusted. **Why it matters**: Tools broaden attack surface. [Forward link](../agent-permissions-and-sandboxing/learning/overview).

### Example 64: OWASP LLM01

**Brief**: Prompt injection has direct and indirect forms. **Diagram**: `prompt | tool result → policy conflict`. **Survey**: Use a threat model. **Key takeaway**: Both sources need controls. **Why it matters**: One missing boundary is enough. [Forward link](../agent-permissions-and-sandboxing/learning/overview).

### Example 65: Untrusted Tool Results

**Brief**: Tool results remain data. **Diagram**: `result → quote → decision`. **Survey**: Separate instructions from evidence. **Key takeaway**: Do not obey content automatically. **Why it matters**: Attackers can influence sources. [Forward link](../agent-tools-and-mcp/learning/overview).

### Example 66: Excessive Agency

**Brief**: Excessive agency grants more action than needed. **Diagram**: `broad authority → high blast radius`. **Survey**: Constrain authority. **Key takeaway**: Capability must be necessary. **Why it matters**: Errors become consequential. [Forward link](../agent-permissions-and-sandboxing/learning/overview).

### Example 67: Excessive Functionality

**Brief**: Unneeded tools expand reachable actions. **Diagram**: `extra tool → extra risk`. **Survey**: Remove unused capability. **Key takeaway**: Smaller surfaces are safer. **Why it matters**: Unused features become attack paths. [Forward link](../agent-permissions-and-sandboxing/learning/overview).

### Example 68: Excessive Permissions

**Brief**: A needed tool can still have too much authority. **Diagram**: `tool → over-scoped permission`. **Survey**: Apply least privilege. **Key takeaway**: Scope access by task. **Why it matters**: A compromise should be containable. [Forward link](../agent-permissions-and-sandboxing/learning/overview).

### Example 69: Lethal Trifecta

**Brief**: Private data, untrusted content, and external communication combine dangerously. **Diagram**: `three legs → exfiltration`. **Survey**: Remove one leg. **Key takeaway**: Combinations create risk. **Why it matters**: Each part may look harmless alone. [Forward link](../agent-permissions-and-sandboxing/learning/overview).

### Example 70: Trifecta Mitigation

**Brief**: Breaking one trifecta leg cuts the path. **Diagram**: `remove authority → stop flow`. **Survey**: Choose the least disruptive control. **Key takeaway**: Defense can be architectural. **Why it matters**: Prevention is cheaper than cleanup. [Forward link](../agent-permissions-and-sandboxing/learning/overview).

### Example 71: LangGraph Stateful

**Brief**: Stateful graphs model orchestration transitions. **Diagram**: `state → node → state`. **Survey**: This course surveys, not builds graphs. **Key takeaway**: State must have ownership. **Why it matters**: Hidden state harms recovery. [Forward link](../the-agent-loop/learning/overview).

### Example 72: OpenAI Agents SDK

**Brief**: SDKs package agents, handoffs, and guardrails. **Diagram**: `SDK primitives → app policy`. **Survey**: Keep policy outside vendor abstractions. **Key takeaway**: Frameworks do not remove responsibility. **Why it matters**: Provider changes are common. [Forward link](../agent-tools-and-mcp/learning/overview).

### Example 73: CrewAI Crews Flows

**Brief**: Crews and flows distinguish teams from fixed orchestration. **Diagram**: `crew | flow`. **Survey**: Match the construct to uncertainty. **Key takeaway**: Coordination is not free. **Why it matters**: Extra actors cost context and latency. [Forward link](../agent-orchestration-subagents-and-observability/learning/overview).

### Example 74: AutoGen Maintenance

**Brief**: Framework currency changes over time. **Diagram**: `maintenance state → migration decision`. **Survey**: Verify current vendor support before adoption. **Key takeaway**: APIs are temporal dependencies. **Why it matters**: Stale dependencies raise operational cost. [Forward link](../agent-orchestration-subagents-and-observability/learning/overview).

### Example 75: Simplest Solution

**Brief**: Add agency only when it helps. **Diagram**: `need → simplest mechanism`. **Survey**: Start with a workflow. **Key takeaway**: Complexity needs evidence. **Why it matters**: Simple systems are easier to secure. [Forward link](../the-agent-loop/learning/overview).

### Example 76: Not Agentic at All

**Brief**: Some products need no agentic system. **Diagram**: `fixed task → ordinary code`. **Survey**: Reject agency when it adds no value. **Key takeaway**: Declining complexity is valid. **Why it matters**: Product reliability beats novelty. [Forward link](../the-agent-loop/learning/overview).

### Example 77: Reason Act Observe

**Brief**: A cycle uses observation to select the next action. **Diagram**: `reason → act → observe`. **Survey**: Keep it bounded. **Key takeaway**: Observation updates control. **Why it matters**: Actions without observation drift. [Forward link](../the-agent-loop/learning/overview).

### Example 78: Tool Dispatch Typed

**Brief**: Typed dispatch maps a validated call to a handler. **Diagram**: `call → type check → handler`. **Survey**: Implement in the tools owner. **Key takeaway**: Type contracts shrink ambiguity. **Why it matters**: Dispatch errors can be dangerous. [Forward link](../agent-tools-and-mcp/learning/overview).

### Example 79: Memory Plus Loop

**Brief**: Bounded loops may carry scoped step memory. **Diagram**: `step memory → next observation`. **Survey**: Retention belongs to context ownership. **Key takeaway**: Memory must stay relevant. **Why it matters**: Stale memory distorts future action. [Forward link](../agent-context-and-memory/learning/overview).

### Example 80: Agentic Capstone

**Brief**: The complete system combines tools, loop, memory, guardrails, and evaluation. **Diagram**: `bounded loop + guarded tools + evidence`. **Survey**: Build each concern in its owning harness course. **Key takeaway**: A production agent is composed, constrained software. **Why it matters**: No single framework primitive supplies safety or measurement. [Forward link](../agent-orchestration-subagents-and-observability/learning/overview).

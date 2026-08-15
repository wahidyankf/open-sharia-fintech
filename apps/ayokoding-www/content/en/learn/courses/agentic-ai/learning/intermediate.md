---
title: "Intermediate Examples"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 20
---

Each entry is survey-only: **Brief**, **Diagram**, **Survey**, **Key takeaway**, and **Why it matters**;
implementation belongs to the linked harness courses.

### Example 28: Parallelization Voting

**Brief**: Repeated independent answers can be aggregated. **Diagram**: `N runs → vote`. **Survey**: Use bounded independent tasks. **Key takeaway**: Voting trades cost for robustness. **Why it matters**: Parallel work needs a budget. [Forward link](../../agent-orchestration-subagents-and-observability/learning/overview.md).

### Example 29: Orchestrator Workers

**Brief**: A lead delegates distinct work to workers. **Diagram**: `lead → workers → results`. **Survey**: Delegate only independent scopes. **Key takeaway**: The lead retains integration authority. **Why it matters**: Ambiguous ownership creates duplicated work. [Forward link](../../agent-orchestration-subagents-and-observability/learning/overview.md).

### Example 30: Orchestrator Synthesize

**Brief**: A lead merges worker outputs. **Diagram**: `results → synthesis`. **Survey**: Validate each result before merge. **Key takeaway**: Synthesis is an explicit boundary. **Why it matters**: One bad result can poison a final answer. [Forward link](../../agent-orchestration-subagents-and-observability/learning/overview.md).

### Example 31: Evaluator Optimizer

**Brief**: A score can guide a bounded revision. **Diagram**: `generate → score → retry`. **Survey**: Deep evals are not implemented here. **Key takeaway**: Scores need validated criteria. **Why it matters**: Self-scoring can mislead. [Forward link](../../evaluating-ai-systems-in-depth/learning/overview.md).

### Example 32: Multi-agent Lead Subagents

**Brief**: A lead may use parallel subagents. **Diagram**: `lead → parallel contexts`. **Survey**: Keep handoffs scoped. **Key takeaway**: More agents are not automatically better. **Why it matters**: Context duplication is expensive. [Forward link](../../agent-orchestration-subagents-and-observability/learning/overview.md).

### Example 33: Multi-agent Token Cost

**Brief**: Multi-agent work multiplies tokens. **Diagram**: `N agents → N contexts`. **Survey**: Measure before scaling out. **Key takeaway**: Parallelism has a cost. **Why it matters**: Cost can exceed quality benefit. [Forward link](../../agent-orchestration-subagents-and-observability/learning/overview.md).

### Example 34: Agent Handoff

**Brief**: A handoff transfers control to another specialist. **Diagram**: `agent A → agent B`. **Survey**: Carry only needed state. **Key takeaway**: Handoffs require ownership. **Why it matters**: Lost authority context causes unsafe actions. [Forward link](../../agent-orchestration-subagents-and-observability/learning/overview.md).

### Example 35: MCP Host Client Server

**Brief**: MCP separates host, client, and server roles. **Diagram**: `host → client → server`. **Survey**: Use the protocol owner for implementation. **Key takeaway**: Roles define trust boundaries. **Why it matters**: Tool access needs clear ownership. [Forward link](../../agent-tools-and-mcp/learning/overview.md).

### Example 36: MCP USB-C

**Brief**: MCP is a standard interface analogy. **Diagram**: `many clients ↔ one protocol`. **Survey**: Avoid bespoke adapters when a standard fits. **Key takeaway**: Interoperability reduces coupling. **Why it matters**: Custom integrations are costly to maintain. [Forward link](../../agent-tools-and-mcp/learning/overview.md).

### Example 37: MCP Connect Tool

**Brief**: A server exposes a tool to a client. **Diagram**: `client → server tool`. **Survey**: Validate schema and authority. **Key takeaway**: Connection is not permission. **Why it matters**: Exposed tools can be consequential. [Forward link](../../agent-tools-and-mcp/learning/overview.md).

### Example 38: MCP JSON-RPC

**Brief**: MCP transports typed requests over JSON-RPC. **Diagram**: `request → response`. **Survey**: Treat transport payload as untrusted input. **Key takeaway**: Protocol validation is mandatory. **Why it matters**: Malformed messages must not dispatch actions. [Forward link](../../agent-tools-and-mcp/learning/overview.md).

### Example 39: Human-in-the-loop Interrupt

**Brief**: An interrupt pauses before a consequential action. **Diagram**: `propose → approve → act`. **Survey**: Do not bypass approval in automation. **Key takeaway**: Humans own high-impact decisions. **Why it matters**: A pause limits blast radius. [Forward link](../../agent-permissions-and-sandboxing/learning/overview.md).

### Example 40: Approval Gate

**Brief**: Approval gates a sensitive action. **Diagram**: `request → gate → allowed action`. **Survey**: Record the approval decision. **Key takeaway**: Authorization is external to the model. **Why it matters**: Ungated actions violate policy. [Forward link](../../agent-permissions-and-sandboxing/learning/overview.md).

### Example 41: Input Guardrail

**Brief**: Validate input before planning. **Diagram**: `input → guard → agent`. **Survey**: Reject unsafe requests early. **Key takeaway**: Prevention precedes execution. **Why it matters**: Unsafe input should not enter the loop. [Forward link](../../agent-permissions-and-sandboxing/learning/overview.md).

### Example 42: Output Guardrail

**Brief**: Validate final output before release. **Diagram**: `agent → guard → user`. **Survey**: Use a typed output policy. **Key takeaway**: Generated text remains untrusted. **Why it matters**: Downstream consumers need safe data. [Forward link](../../agent-permissions-and-sandboxing/learning/overview.md).

### Example 43: Tool Input Guardrail

**Brief**: A guard validates tool parameters. **Diagram**: `call → validate → tool`. **Survey**: Reject secrets and malformed input. **Key takeaway**: Tools need independent checks. **Why it matters**: A model can generate unsafe arguments. [Forward link](../../agent-permissions-and-sandboxing/learning/overview.md).

### Example 44: Tool Permissioning

**Brief**: Tools use least privilege. **Diagram**: `role → scoped tool`. **Survey**: Expose minimum capability. **Key takeaway**: Permissioning limits authority. **Why it matters**: Broad tools enable excessive agency. [Forward link](../../agent-permissions-and-sandboxing/learning/overview.md).

### Example 45: Tool Sandbox

**Brief**: Sandboxes contain tool execution. **Diagram**: `tool → isolated environment`. **Survey**: Scope filesystem and network access. **Key takeaway**: Isolation is defense in depth. **Why it matters**: Tool failures should not escape containment. [Forward link](../../agent-permissions-and-sandboxing/learning/overview.md).

### Example 46: Max Turns

**Brief**: A maximum turns cap stops looping. **Diagram**: `turn count → halt`. **Survey**: Enforce it outside the model. **Key takeaway**: Termination is policy. **Why it matters**: Caps prevent runaway cost. [Forward link](../../the-agent-loop/learning/overview.md).

### Example 47: Recursion Limit

**Brief**: A step limit prevents recursive control flow. **Diagram**: `depth → limit`. **Survey**: Fail safely on exhaustion. **Key takeaway**: Limits bound complexity. **Why it matters**: Deep loops are hard to recover. [Forward link](../../the-agent-loop/learning/overview.md).

### Example 48: Loop Terminates

**Brief**: A valid loop halts within its budget. **Diagram**: `observe → stop`. **Survey**: Test success and exhaustion paths. **Key takeaway**: Termination is observable behavior. **Why it matters**: Nontermination is a production incident. [Forward link](../../the-agent-loop/learning/overview.md).

### Example 49: Budget Cap

**Brief**: A cost cap limits an execution. **Diagram**: `spend → cap → halt`. **Survey**: Treat cost as an input to control flow. **Key takeaway**: Budgeting constrains agency. **Why it matters**: A correct answer can still be too expensive. [Forward link](../../the-agent-loop/learning/overview.md).

### Example 50: When Not Agent

**Brief**: A fixed task may need only a workflow. **Diagram**: `known path → workflow`. **Survey**: Prefer the simpler mechanism. **Key takeaway**: Restraint is a design skill. **Why it matters**: Simpler systems have fewer failure modes. [Forward link](../../the-agent-loop/learning/overview.md).

### Example 51: Pause Turn

**Brief**: A paused turn waits for caller resumption. **Diagram**: `limit → pause → resume`. **Survey**: Preserve state safely across the pause. **Key takeaway**: Pausing is controlled continuation. **Why it matters**: It avoids uncontrolled server-side looping. [Forward link](../../the-agent-loop/learning/overview.md).

### Example 52: Trajectory Eval

**Brief**: A trajectory is the sequence of actions. **Diagram**: `actions → reference comparison`. **Survey**: Forward deep methodology to the eval course. **Key takeaway**: Outcomes alone can hide unsafe paths. **Why it matters**: Action quality matters. [Forward link](../../evaluating-ai-systems-in-depth/learning/overview.md).

### Example 53: Task Success Rate

**Brief**: Success rate summarizes dataset outcomes. **Diagram**: `cases → pass rate`. **Survey**: Do not build the eval harness here. **Key takeaway**: Aggregate metrics need representative cases. **Why it matters**: Small samples mislead. [Forward link](../../evaluating-ai-systems-in-depth/learning/overview.md).

### Example 54: LLM as Judge

**Brief**: A separate model can judge a response. **Diagram**: `answer → different judge`. **Survey**: Judge calibration belongs to deep evals. **Key takeaway**: A judge is also probabilistic. **Why it matters**: Unvalidated judges create false confidence. [Forward link](../../evaluating-ai-systems-in-depth/learning/overview.md).

### Example 55: Exact Match Scoring

**Brief**: Exact match compares against a golden answer. **Diagram**: `output ↔ gold`. **Survey**: Use when the target is unambiguous. **Key takeaway**: Metrics fit tasks, not vice versa. **Why it matters**: Wrong metrics reward wrong behavior. [Forward link](../../evaluating-ai-systems-in-depth/learning/overview.md).

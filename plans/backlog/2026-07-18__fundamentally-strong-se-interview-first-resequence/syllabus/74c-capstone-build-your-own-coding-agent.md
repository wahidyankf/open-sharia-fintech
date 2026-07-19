# Capstone · Build Your Own Coding Agent (Phase 3, harness cluster)

**Mapping row** (frozen [tech-docs §Canonical Mapping Table](../tech-docs.md#canonical-mapping-table)):
inter-topic capstone · anchored after N=74 · folder weight **845** (`105 + 10 × 74`) · Python (DN-12).
**NEW (Addition 2)** — the flagship of the harness-engineering cluster; the DN-11 optional
browser-driving bonus ties Addition 1 + 2 together.

**Scope note**: the marquee build — assemble the entire harness cluster
([N=70 The Agent Loop](./70-the-agent-loop.md), [N=71 Agent Tools & MCP](./71-agent-tools-and-mcp.md),
[N=72 Agent Context & Memory](./72-agent-context-and-memory.md),
[N=73 Agent Permissions & Sandboxing](./73-agent-permissions-and-sandboxing.md),
[N=74 Orchestration, Subagents & Observability](./74-agent-orchestration-subagents-and-observability.md))
into **one working coding agent** the reader builds themselves: a Claude-Code-shaped local coding
assistant that reads a repo, plans, edits files, runs tools/tests, manages its context, respects
permissions and sandboxing, and is observable. **Optional DN-11 bonus**: drive the
[CDP browser service](./69-browser-automation-with-cdp.md) over MCP so the agent can also research on the
web — the `remotebrowser`↔MCP synergy payoff.

## Why this exists · the big idea

- **The problem before the solution**: the cluster taught each agent subsystem in isolation. Nothing yet
  proves the reader can integrate them into a coherent, safe, observable coding agent — which is the
  whole point of the cluster and the clearest demonstration that "AI coding agents" are buildable
  software, not magic.
- **Keep-this-if-you-forget-everything**: a coding agent is the [loop](./70-the-agent-loop.md) + real
  [tools](./71-agent-tools-and-mcp.md) + managed [context](./72-agent-context-and-memory.md) +
  [guardrails](./73-agent-permissions-and-sandboxing.md) +
  [observability](./74-agent-orchestration-subagents-and-observability.md) — build all five and you have
  demystified the tools you use daily.
- **Big ideas touched**: `abstraction-and-its-cost` (each subsystem is a clean seam), `determinism-vs-
emergence` (deterministic engineering around a stochastic core), `security-by-design` (a code-editing
  agent must be safe by construction).

## Prerequisites

- **Prior topics**: the full harness cluster [N=70](./70-the-agent-loop.md)–[N=74](./74-agent-orchestration-subagents-and-observability.md);
  [N=69 Browser Automation with CDP](./69-browser-automation-with-cdp.md) for the optional bonus;
  [N=20 Async Python & FastAPI Services](./20-async-python-and-fastapi-services.md) for the async/MCP
  substrate; [N=65 Software Engineering Practices](./README.md) for the TDD discipline the agent drives.
- **Tools & environment**: a macOS/Linux terminal; Python 3.x under `uv`; an LLM API with tool calling
  (provider-agnostic behind an adapter; keys via env); a container/OS sandbox; a vector store; an MCP
  library; `pytest`; Neovim/VSCode — all pinned CVE-clean at authoring.
- **Assumed knowledge**: every cluster subsystem individually; async Python; the no-secrets rule.

## Accuracy notes

> Pre-authoring `web-researcher` sweep pending (DD-28 convention).

- 2026-07-19 — `[Needs Verification]`: pin all cluster dependency versions (LLM SDK/adapter, MCP library,
  vector store, sandbox runtime, tracing/TUI libraries) at authoring; keep the model name configurable,
  never hard-coded. The integration architecture (loop + tools + context + permissions + observability)
  is stable.

## Concepts integrated

This capstone integrates the cluster's concepts; it introduces none of its own:

- [ ] The read-eval-act loop with streaming + stop conditions + budgets
      ([N=70](./70-the-agent-loop.md)).
- [ ] Well-designed tools (fs read/write/list, bounded shell, test runner) + optional MCP servers
      ([N=71](./71-agent-tools-and-mcp.md)).
- [ ] Context budgeting + compaction + retrieval over the repo + memory
      ([N=72](./72-agent-context-and-memory.md)).
- [ ] Deny/ask/allow permissions + sandboxed execution + injection defense + secret hygiene + audit log
      ([N=73](./73-agent-permissions-and-sandboxing.md)).
- [ ] Subagents (e.g. a research subagent) + tracing + metrics + an eval suite + a TUI
      ([N=74](./74-agent-orchestration-subagents-and-observability.md)).
- [ ] (Optional bonus) The [browser service](./69-browser-automation-with-cdp.md) exposed over MCP for
      web research.

## Ordered steps

1. `capstone-build-your-own-coding-agent/code/core/` — the provider-adapter loop (with a fake for tests)
   - a tool registry (fs read/write/list, bounded shell, test runner) + stop conditions + budget. Verify
     the fake-backed loop is deterministic under `pytest` and completes a one-tool task.
2. Add context management: budgeting, rolling-window compaction, and repo retrieval over a vector index.
   Verify the agent works a task larger than a naive context without overflow.
3. Add the safety layer: deny/ask/allow permissions, sandboxed tool execution (filesystem + egress +
   resource limits), injection defense, secret hygiene, and an audit log. Verify a red-team pass cannot
   escape or exfiltrate.
4. Add observability + a TUI + one research subagent: full run tracing, cost/latency metrics, a streaming
   TUI with an approval gate, and an eval suite. Verify a run is fully traced and the evals grade it.
5. Drive the assembled agent through a real TDD coding task (given a failing test, iterate to green).
   Verify the red→green transition, a complete trace, a passing eval, and a clean audit log.
6. (Optional DN-11 bonus) Expose the [CDP browser service](./69-browser-automation-with-cdp.md) as an MCP
   server and let the agent research a docs page before implementing. Verify the agent completes a task
   that required web research, driven over MCP.

## Acceptance criteria

- The reader's own coding agent completes a real TDD coding task end to end — reading the repo, planning,
  editing files, running tests to green — while: staying within a context budget via compaction +
  retrieval; enforcing deny/ask/allow permissions and sandboxed execution that a red-team pass cannot
  escape or exfiltrate through; producing a complete trace + cost/latency metrics + a passing eval + an
  audit log; and driving interaction through a streaming TUI with an approval gate. The optional bonus
  additionally has the agent research the web over the browser MCP server before implementing. The
  deterministic test suite passes with no live model calls; no secret is ever committed or placed in the
  model's context.

## Done bar

Runnable end-to-end (the agent completes a real coding task with every subsystem provably active) +
web-verified.

---

← Previous: [N=74 · Agent Orchestration, Subagents & Observability](./74-agent-orchestration-subagents-and-observability.md) ·
Next: N=75 `just-enough-c` ([index](./README.md)) →

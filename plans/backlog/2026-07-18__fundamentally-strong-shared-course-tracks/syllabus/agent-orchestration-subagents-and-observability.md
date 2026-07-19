# Agent Orchestration, Subagents & Observability (Annotated-concept, Python)

**Course ID**: `agent-orchestration-subagents-and-observability` · **Format**: Annotated-concept ·
**Language**: Python. **NEW** — last course of the harness cluster before the
`capstone-build-your-own-coding-agent` course. Cluster language Python (matching `remotebrowser` and
the series' agentic-AI courses).

**Scope note**: scaling one agent into a **system** — **subagents** (delegating a bounded task to an
isolated agent context that returns only a summary), **orchestration** (sequential/parallel/hierarchical
coordination, background tasks), the **hooks/skills** extension surface, a **TUI** for interaction, and
**observability** (tracing, evals, cost/latency metrics for a non-deterministic system). Annotated-
concept: architecture diagrams where structure is the point, runnable code where a mechanism (a subagent
call, a hook, a trace span) clarifies. Caps the cluster built across
`the-agent-loop` through `agent-permissions-and-sandboxing`.

## Why this exists · the big idea

- **The problem before the solution**: a single agent hits limits — its context fills with one task's
  detail, it cannot do two things at once, and when it misbehaves you cannot see why. Orchestration
  (many agents), isolation (subagents), and observability (tracing + evals) are what turn a toy loop
  into a system you can scale and trust.
- **Keep-this-if-you-forget-everything**: delegate bounded work to isolated subagents that return a
  summary (keeping the main context clean), coordinate them deliberately, and instrument everything —
  because a non-deterministic system you cannot observe is a system you cannot debug or improve.
- **Big ideas touched**: `abstraction-and-its-cost` (a subagent is a context-isolation abstraction — its
  detail stays out of the parent), `determinism-vs-emergence` (evals are the test suite for a stochastic
  system).

## Prerequisites

- **Prior topics**: `the-agent-loop`,
  `agent-tools-and-mcp`,
  `agent-context-and-memory`,
  `agent-permissions-and-sandboxing`;
  `concurrency-and-parallelism` for coordination; `software-engineering-practices` for evals-as-tests thinking.
- **Tools & environment**: a macOS/Linux terminal; Python 3.x under `uv`; the agent loop + tools +
  safety layer from the cluster; a tracing/observability library + a TUI library (pinned CVE-clean at
  authoring); `pytest`; Neovim/VSCode.
- **Assumed knowledge**: the full agent loop, tools, context management, and permissions; async
  concurrency; testing discipline.

## Accuracy notes

> Pre-authoring `web-researcher` sweep pending (per this plan's Anti-Hallucination verification recipe).

- 2026-07-18 — subagents (isolated context returning a summary), orchestration patterns (sequential,
  parallel, hierarchical), tracing/observability, and evals for LLM systems are **stable, vendor-
  independent** concepts.
- 2026-07-18 — `[Needs Verification]`: the chosen tracing library, TUI library, and any hooks/skills
  extension mechanism differ by harness — keep the module principle-based and pin/verify the concrete
  libraries at authoring.
- 2026-07-18 — `[Needs Verification]`: eval frameworks/tooling evolve fast — teach the eval _principle_
  (a graded test set for a stochastic system) and pin any named tool at authoring.

## Concepts

1. **co-01 · single-agent-limits** — one agent has a bounded context, no parallelism, and limited
   observability, capping what it can do reliably.
2. **co-02 · what-a-subagent-is** — a subagent is a delegated agent run in an isolated context that
   returns only a summary to its parent.
3. **co-03 · context-isolation-benefit** — a subagent keeps its task's exploration detail out of the
   parent's context, preserving the parent's budget.
4. **co-04 · delegation-boundaries** — deciding what to delegate (bounded, summarizable subtasks) vs keep
   in the main agent.
5. **co-05 · sequential-orchestration** — chaining agents/steps where each depends on the prior's output.
6. **co-06 · parallel-orchestration** — running independent subagents concurrently and merging results.
7. **co-07 · hierarchical-orchestration** — an orchestrator agent that plans and dispatches to worker
   subagents.
8. **co-08 · background-tasks** — long-running work run out-of-band from the main interaction, polled or
   awaited.
9. **co-09 · result-aggregation** — combining multiple subagents' outputs into one coherent result.
10. **co-10 · orchestration-failure-handling** — a subagent failing must be handled (retry, fallback,
    partial result) without collapsing the whole run.
11. **co-11 · hooks** — extension points that fire on lifecycle events (pre/post tool call, session
    start/stop) to inject behavior.
12. **co-12 · skills** — packaged, named, filesystem-based procedures the agent loads on demand instead
    of re-deriving guidance.
13. **co-13 · extensibility-surface** — hooks + skills + tools + MCP form the surface for extending an
    agent without changing its core.
14. **co-14 · tui-interaction** — a terminal UI for driving the agent, showing streaming output, tool
    calls, and approvals.
15. **co-15 · observability-need** — a non-deterministic system must be instrumented to be debuggable and
    improvable.
16. **co-16 · tracing-a-run** — a trace records the tree of turns, tool calls, and subagent spans for one
    run.
17. **co-17 · structured-logging** — structured, queryable logs of decisions, tokens, and outcomes per
    turn.
18. **co-18 · metrics-cost-latency** — tracking per-run cost, latency, tool usage, and success rate as
    operational metrics.
19. **co-19 · evals-as-tests** — a graded set of tasks with expected outcomes is the test suite for a
    stochastic agent.
20. **co-20 · eval-driven-improvement** — using eval results to iterate on prompts, tools, and
    orchestration.
21. **co-21 · regression-evals** — re-running evals to catch quality regressions when the agent changes.
22. **co-22 · orchestration-cost-and-complexity-tradeoff** — more agents and coordination add cost and
    complexity; orchestrate only when a single agent genuinely cannot cope.

## Tensions & trade-offs — when NOT to reach for this

- **Orchestration vs a single agent**: multiple coordinated agents add latency, cost, and coordination
  bugs. A single well-scoped agent with good context management often beats a sprawling multi-agent
  system — reach for orchestration only when isolation or parallelism genuinely pays.
- **Observability overhead vs blindness**: full tracing + evals cost engineering effort and runtime
  overhead; skipping them leaves you blind to why the agent fails. Instrument enough to debug and
  improve, not so much that the harness is more observability than agent.
- **When NOT to add a subagent**: delegating a task whose result cannot be cleanly summarized just moves
  the context problem — some work must stay in the main agent where the detail matters.

## Lineage — why it beat the alternative

- As agents took on larger tasks, the single-loop model strained: context filled, work was serial, and
  failures were opaque. Subagents borrowed the oldest idea in engineering — decomposition with
  information hiding — to isolate subtask detail behind a summary. Orchestration patterns (sequential,
  parallel, hierarchical) applied concurrency and coordination thinking to agents. And evals brought the
  test-suite discipline to stochastic systems, because you cannot improve what you cannot measure. This
  module caps the harness cluster (`the-agent-loop` through `agent-permissions-and-sandboxing`) and is the immediate prerequisite
  for the [build-your-own-coding-agent capstone](./capstone-build-your-own-coding-agent.md).

## Worked examples

No fixed difficulty bands (Annotated-concept); grouped by theme. Diagrams where structure is the point,
runnable code where a mechanism clarifies. Colocated under
`agent-orchestration-subagents-and-observability/learning/code/` (runnable) and `.../artifacts/`
(diagrams). Contiguous `ex-01..ex-46`. Every example cites the `co-NN` it exercises.

### Theme A · Subagents & delegation (ex 01–12)

1. **ex-01 · single-agent-limit-demo** — a task that overflows one agent's context — verify the failure
   motivates delegation. (co-01)
2. **ex-02 · first-subagent** — delegate a bounded subtask to an isolated subagent — verify only a
   summary returns. (co-02, co-03)
3. **ex-03 · context-isolation-proof** — show the parent's context does not grow by the subagent's
   detail — verify the budget saving. (co-03)
4. **ex-04 · delegation-boundary-decision** — decide which of two subtasks to delegate vs keep — verify
   the rationale. (co-04)
5. **ex-05 · subagent-with-own-tools** — a subagent scoped to a subset of tools — verify it uses only
   those. (co-02, co-04)
6. **ex-06 · summary-fidelity** — verify a subagent's summary preserves the decisions the parent needs.
   (co-02, co-09)
7. **ex-07 · subagent-failure-fallback** — a subagent fails; the parent falls back — verify graceful
   handling. (co-10)
8. **ex-08 · nested-subagents** — a subagent that itself delegates — verify bounded nesting. (co-07)
9. **ex-09 · subagent-diagram** — a Mermaid diagram of parent → subagent isolation + summary return —
   verify the flow. (co-02, co-03)
10. **ex-10 · research-then-implement** — a research subagent feeds a summary to an implementing parent —
    verify the parent uses only the summary. (co-02, co-09)
11. **ex-11 · delegation-cost-tradeoff** — measure the cost of delegating vs inlining a subtask — verify
    the trade-off. (co-22)
12. **ex-12 · when-not-to-delegate** — a task whose result cannot be summarized cleanly kept in-agent —
    verify the reasoning. (co-04, co-22)

### Theme B · Orchestration & background work (ex 13–24)

1. **ex-13 · sequential-pipeline** — chain three agent steps where each feeds the next — verify the
   pipeline. (co-05)
2. **ex-14 · parallel-fanout** — run three independent subagents concurrently — verify combined latency
   ≈ the slowest. (co-06)
3. **ex-15 · aggregate-parallel-results** — merge parallel subagent outputs into one result — verify the
   aggregation. (co-09, co-06)
4. **ex-16 · hierarchical-orchestrator** — an orchestrator plans + dispatches to workers — verify the
   plan → dispatch → collect flow. (co-07)
5. **ex-17 · background-task** — run a long task in the background + poll it — verify the main
   interaction stays responsive. (co-08)
6. **ex-18 · orchestration-failure-recovery** — one worker fails; the orchestrator produces a partial
   result — verify no total collapse. (co-10)
7. **ex-19 · concurrency-cap** — bound the number of concurrent subagents — verify the cap holds.
   (co-06, co-22)
8. **ex-20 · orchestration-diagram** — a Mermaid diagram of sequential vs parallel vs hierarchical —
   verify all three patterns are shown. (co-05, co-06, co-07)
9. **ex-21 · map-reduce-over-files** — fan out per-file subagents, reduce to a summary — verify each
   file processed. (co-06, co-09)
10. **ex-22 · retry-and-fallback-policy** — a worker retry + fallback policy — verify the policy applies.
    (co-10)
11. **ex-23 · orchestration-cost-report** — report total cost/latency across an orchestrated run — verify
    the figures. (co-18, co-22)
12. **ex-24 · single-vs-multi-agent-contrast** — solve one task with one agent and with orchestration —
    verify when multi-agent actually helps. (co-01, co-22)

### Theme C · Extensibility: hooks, skills, TUI (ex 25–34)

1. **ex-25 · pre-tool-hook** — a hook firing before every tool call (e.g. logging/approval) — verify it
   fires. (co-11)
2. **ex-26 · post-tool-hook** — a hook firing after a tool call to post-process the result — verify it
   runs. (co-11)
3. **ex-27 · session-lifecycle-hooks** — hooks on session start/stop — verify both fire. (co-11)
4. **ex-28 · load-a-skill** — attach a packaged skill and have the agent follow it — verify the
   procedure is followed. (co-12)
5. **ex-29 · skill-vs-adhoc** — the same task with + without a skill — verify the skill run is
   repeatable. (co-12)
6. **ex-30 · extensibility-surface-diagram** — a Mermaid diagram of tools + MCP + hooks + skills as the
   extension surface — verify each is shown. (co-13)
7. **ex-31 · tui-streaming-view** — a TUI showing streamed output + tool calls — verify live updates.
   (co-14)
8. **ex-32 · tui-approval-flow** — a TUI approval prompt for a gated action — verify the human gate in
   the UI. (co-14, co-11)
9. **ex-33 · hook-driven-audit** — use a hook to build the audit log from
   `agent-permissions-and-sandboxing` — verify completeness. (co-11)
10. **ex-34 · extend-without-core-change** — add a capability via a hook/skill without touching the loop
    — verify the core is unchanged. (co-13)

### Theme D · Observability & evals (ex 35–46)

1. **ex-35 · trace-a-run** — record a trace tree of turns + tool calls + subagent spans — verify the
   tree is complete. (co-16)
2. **ex-36 · structured-run-log** — structured per-turn logs (decision, tokens, outcome) — verify they
   are queryable. (co-17)
3. **ex-37 · cost-latency-metrics** — capture per-run cost/latency/success metrics — verify they update.
   (co-18)
4. **ex-38 · trace-visualization** — a Mermaid diagram of a traced run's span tree — verify it maps to
   the log. (co-16)
5. **ex-39 · build-an-eval-set** — a graded set of tasks with expected outcomes — verify each has a
   grader. (co-19)
6. **ex-40 · run-the-evals** — run the agent against the eval set + score it — verify a pass/fail rate.
   (co-19)
7. **ex-41 · eval-driven-prompt-fix** — an eval failure drives a prompt/tool fix — verify the score
   improves. (co-20)
8. **ex-42 · regression-eval** — re-run evals after a change to catch a regression — verify a regression
   is detected. (co-21)
9. **ex-43 · flaky-eval-handling** — handle stochastic eval variance (multiple runs, thresholds) —
   verify a robust pass criterion. (co-19)
10. **ex-44 · observability-dashboard** — a summary view of traces + metrics + eval scores — verify it
    reflects a run. (co-16, co-18, co-19)
11. **ex-45 · debug-via-trace** — diagnose a wrong agent outcome purely from its trace — verify the root
    cause is found. (co-16, co-15)
12. **ex-46 · capstone-observable-orchestrated-agent** — an orchestrated multi-subagent system with
    hooks, a TUI, full tracing, metrics, and an eval suite — verify a task runs, is fully traced, and
    passes the evals. (co-01–co-22)

## Capstone spec — intra-topic (concept → full runnable)

- **Goal**: assemble the harness-cluster pieces into an **orchestrated, observable agent system** — an
  orchestrator dispatching isolated subagents (sequential + parallel), a hooks/skills extension surface,
  a TUI for interaction + approvals, full run tracing + cost/latency metrics, and an eval suite that
  grades the system — and use it to complete a multi-part task.
- **Concepts exercised**: [ ] subagents + context isolation (co-02, co-03) [ ] sequential + parallel +
  hierarchical orchestration (co-05–co-07) [ ] failure handling + aggregation (co-09, co-10) [ ] hooks +
  skills + TUI (co-11, co-12, co-14) [ ] tracing + structured logs + metrics (co-16–co-18) [ ] evals +
  regression evals (co-19, co-21).
- **Ordered steps**:
  1. `agent-orchestration-subagents-and-observability/learning/capstone/code/` — an orchestrator that
     delegates to isolated subagents (one sequential chain, one parallel fan-out). Verify subagents
     return summaries and the parent context stays bounded.
  2. Add a hooks/skills surface + a TUI with an approval flow. Verify a hook fires and the TUI streams +
     gates.
  3. Add tracing + structured logs + cost/latency metrics. Verify a run produces a complete trace + a
     metrics summary.
  4. Build + run an eval suite grading the system, then use a failure to drive one improvement. Verify
     the eval score improves and a regression eval catches a planted regression.
- **Acceptance criteria**: the system completes a multi-part task via orchestrated subagents; every run
  is fully traced with cost/latency metrics; the TUI streams output and gates approvals; the eval suite
  grades the system and catches a regression; an eval-driven change measurably improves the score.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

- **Building Effective Agents** — Anthropic (2024). On orchestration patterns and subagent design.
  <https://www.anthropic.com/engineering/building-effective-agents>
- **Observability / evals for LLM systems** — the current standard guidance on tracing and evaluating
  non-deterministic agent systems (pin the named tools/framework at authoring).

## In which paths

- `job-seeking-software-engineer` — Phase 3 · Deepening (shallow → deep) — AI & harness engineering
  (marquee build-your-own track).
- `software-engineer` — Stage 4 · Systems, data, architecture, security & ops depth (shallow → deep) —
  AI & harness engineering (marquee build-your-own track).

---

← Back to [README.md — course library catalog](./README.md)

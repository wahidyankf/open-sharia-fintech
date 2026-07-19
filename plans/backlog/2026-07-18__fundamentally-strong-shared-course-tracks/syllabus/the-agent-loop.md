# The Agent Loop (By Example, Python)

**Course ID**: `the-agent-loop` · **Format**: By Example · **Language**: Python. **NEW** — first
course of the build-your-own-coding-agent cluster. Cluster language is Python (matches the series
primary, `remotebrowser`, and the async-Python course).

**Scope note**: the beating heart of an agent — the **read-eval-act loop** that turns a chat model into
an autonomous worker. Send messages to an LLM, parse a tool-call request, execute the tool, feed the
result back, and repeat until the model emits a final answer or a stop condition trips. Also: streaming
tokens, stop conditions, turn limits, and error recovery. This is the builder's foundation the rest of
the cluster (`agent-tools-and-mcp` through `agent-orchestration-subagents-and-observability`) extends,
and the deep counterpart to the user-side `agentic-coding` and `agentic-ai`.

## Why this exists · the big idea

- **The problem before the solution**: a raw LLM call is a single question-and-answer; it cannot take
  actions, observe results, or iterate toward a goal. The agent loop is the small, unglamorous control
  structure that closes that gap — and once you have built it, every "magical" coding agent stops being
  magic.
- **Keep-this-if-you-forget-everything**: an agent is a `while` loop — call the model, if it wants a
  tool, run the tool and append the result, else you are done — plus the discipline of stop conditions
  so it terminates.
- **Big ideas touched**: `determinism-vs-emergence` (the loop is deterministic control around a
  non-deterministic model), `taming-state` (the growing message history _is_ the agent's state).

## Prerequisites

- **Prior topics**: `creating-ai-powered-apps` and `agentic-ai`
  (LLM APIs, tool-use concepts), `async-python-and-fastapi-services`
  (async + streaming), `just-enough-python`.
- **Tools & environment**: a macOS/Linux terminal; Python 3.x under `uv`; access to an LLM API that
  supports tool/function calling (any vendor; keep the loop provider-agnostic); `pytest`; Neovim/VSCode.
  API keys via env, never committed.
- **Assumed knowledge**: calling an LLM chat API; JSON; async Python and streaming; basic error handling.

## Accuracy notes

> Pre-authoring `web-researcher` sweep pending (per this plan's Anti-Hallucination verification recipe).

- 2026-07-18 — the read-eval-act loop (a.k.a. the ReAct pattern), tool-call request/response messages,
  streaming, and stop conditions are **stable, vendor-independent** agent concepts.
- 2026-07-18 — `[Needs Verification]`: the exact tool-calling message schema differs by provider (OpenAI,
  Anthropic, others) — build against an adapter and pin the provider SDK version at authoring; keep the
  core loop provider-agnostic.
- 2026-07-18 — `[Needs Verification]`: model names/capabilities move fast — never hard-code a model
  name in the shipped loop; make it configurable.

## Concepts

1. **co-01 · what-an-agent-is** — an agent is an LLM wrapped in a loop that can call tools, observe
   results, and iterate toward a goal, versus a single-shot completion.
2. **co-02 · the-read-eval-act-loop** — call the model, evaluate whether it requested a tool, act
   (execute the tool), append the result, and repeat.
3. **co-03 · the-message-history** — the conversation is an ordered list of messages (system, user,
   assistant, tool) that is the agent's entire working state.
4. **co-04 · system-prompt** — the system message sets the agent's role, constraints, and available
   behavior for the whole loop.
5. **co-05 · tool-call-request** — the model can respond with a structured request to call a named tool
   with arguments instead of a final answer.
6. **co-06 · tool-execution** — the loop dispatches the requested tool, runs it, and captures its result.
7. **co-07 · tool-result-message** — the tool's result is appended to the history as a tool message the
   model reads on the next turn.
8. **co-08 · final-answer-detection** — when the model responds without a tool call, the loop treats it
   as the final answer and stops.
9. **co-09 · stop-conditions** — explicit conditions (final answer, max turns, budget, an explicit stop
   tool) that terminate the loop safely.
10. **co-10 · max-turns-guard** — a hard turn cap prevents an infinite or runaway loop.
11. **co-11 · streaming-tokens** — streaming the model's output token-by-token gives responsive UX and
    early visibility into intent.
12. **co-12 · streaming-tool-calls** — tool-call requests can also stream; the loop assembles the full
    call before executing.
13. **co-13 · provider-adapter** — abstracting the provider behind an adapter keeps the loop
    provider-agnostic and testable.
14. **co-14 · error-handling-in-the-loop** — model errors, tool errors, and timeouts must be caught and
    either retried, surfaced to the model, or fail cleanly.
15. **co-15 · tool-error-feedback** — a tool failure is fed back to the model as a result so it can
    adapt, not crash the loop.
16. **co-16 · token-and-cost-budget** — tracking tokens/cost per turn and enforcing a ceiling bounds a
    session's expense.
17. **co-17 · multi-tool-turn** — a single model turn may request several tool calls; the loop runs them
    (sequentially or concurrently) and returns all results.
18. **co-18 · deterministic-testing** — replacing the model with a scripted fake makes the loop's control
    flow unit-testable without live calls.
19. **co-19 · loop-observability** — logging each turn's messages, tool calls, and results makes the
    agent's behavior inspectable.
20. **co-20 · idempotency-and-retries** — retrying a turn safely requires care that tool side effects are
    not double-applied.
21. **co-21 · conversation-turn-vs-loop-iteration** — distinguishing a user-facing turn from an internal
    tool iteration clarifies where stops and budgets apply.
22. **co-22 · minimal-agent-anatomy** — the smallest complete agent is a system prompt, a tool registry,
    the loop, and stop conditions — everything else is an extension.

## Tensions & trade-offs — when NOT to reach for this

- **Autonomy vs control**: a longer leash (more turns, more tools) lets the agent solve more but also
  wander, burn budget, and take unintended actions. Stop conditions and turn caps are the brakes — tune
  them to the task's risk, not maximally open.
- **Streaming vs simplicity**: streaming improves UX but complicates the loop (partial messages,
  assembling streamed tool calls). Start with a non-streaming loop, add streaming once the control flow
  is solid.
- **When NOT to build your own**: for production you often want a maintained framework's loop; build
  your own to _understand_ it (and when you need control a framework denies) — not to reinvent a solved
  wheel for a simple app.

## Lineage — why it beat the alternative

- Agents grew out of the observation that a model which can _request actions_ and _read their results_
  can do far more than one that only completes text — the ReAct pattern (interleaved reasoning and
  acting) formalized it. The loop is deliberately simple because the intelligence lives in the model;
  the engineering is the reliable control structure around it (stops, budgets, error feedback,
  observability). This module builds that core; `agent-tools-and-mcp`
  gives it capabilities, `agent-context-and-memory` manages its
  state, `agent-permissions-and-sandboxing` constrains it,
  and `agent-orchestration-subagents-and-observability`
  scales it — culminating in the [coding-agent capstone](./capstone-build-your-own-coding-agent.md).

## Worked examples

Colocated under `the-agent-loop/learning/code/`. Each builds part of an agent loop; a scripted fake
model makes the control flow deterministically testable (co-18), with a live-model variant behind a
config flag. Contiguous `ex-01..ex-48`. Every example cites the `co-NN` it exercises.

> **Volume-target floor**: this syllabus lists **48** of the required **≥75** (the 75–85 By-Example/
> Primer band, floor not cap — see
> [prd.md §Volume-target bands](../prd.md#new-course--capstone-specifications)).
> The maker adds **≥27** more `ex-NN` entries at authoring time, continuing the numbering and pattern
> taxonomy below, before this topic passes its by-example quality gate.

### Beginner (ex 01–16)

1. **ex-01 · single-model-call** — one LLM completion, no loop — verify a response comes back. (co-01)
2. **ex-02 · message-history-list** — build a system+user message list — verify the structure. (co-03,
   co-04)
3. **ex-03 · fake-model-adapter** — a scripted fake model returning canned turns — verify determinism.
   (co-13, co-18)
4. **ex-04 · minimal-loop-no-tools** — a loop that stops on the first final answer — verify one
   iteration. (co-02, co-08)
5. **ex-05 · detect-tool-call** — parse a tool-call request from a model turn — verify the tool name +
   args. (co-05)
6. **ex-06 · execute-one-tool** — dispatch a single registered tool — verify it runs with the args.
   (co-06)
7. **ex-07 · append-tool-result** — append the tool result as a tool message — verify the history grows.
   (co-07)
8. **ex-08 · loop-until-final** — loop calling model → tool → model until a final answer — verify the
   stop. (co-02, co-08)
9. **ex-09 · max-turns-guard** — cap the loop at N turns — verify it stops at the cap on a non-
   terminating fake. (co-10)
10. **ex-10 · stop-on-explicit-tool** — a `finish` tool that ends the loop — verify termination. (co-09)
11. **ex-11 · system-prompt-effect** — change the system prompt and observe behavior change (fake keyed
    on it) — verify the effect. (co-04)
12. **ex-12 · tool-registry** — a registry mapping names to callables — verify lookup + dispatch. (co-06,
    co-22)
13. **ex-13 · tool-error-feedback** — a tool raises; feed the error back as a result — verify the model
    sees it. (co-15, co-14)
14. **ex-14 · turn-vs-iteration-log** — log user turns vs internal iterations distinctly — verify the
    distinction. (co-21, co-19)
15. **ex-15 · token-count-per-turn** — record token usage per turn — verify a running total. (co-16)
16. **ex-16 · minimal-agent-end-to-end** — a smallest complete agent (prompt + one tool + loop + stop) —
    verify it solves a one-tool task. (co-22)

### Intermediate (ex 17–34)

1. **ex-17 · multi-tool-registry** — register several tools (calculator, clock, echo) — verify each
   dispatches. (co-06, co-22)
2. **ex-18 · multi-tool-turn** — a model turn requesting two tool calls — verify both run and both
   results return. (co-17)
3. **ex-19 · concurrent-tool-calls** — run independent tool calls concurrently — verify combined
   latency ≈ the slowest. (co-17, co-14)
4. **ex-20 · budget-ceiling-stop** — stop when a token/cost budget is exceeded — verify the halt. (co-16,
   co-09)
5. **ex-21 · retry-model-error** — retry a transient model error with backoff — verify eventual success
   or clean failure. (co-14)
6. **ex-22 · timeout-a-tool** — bound a slow tool with a timeout, feed a timeout result back — verify
   the loop continues. (co-14, co-15)
7. **ex-23 · streaming-final-answer** — stream the model's final tokens to stdout — verify incremental
   output. (co-11)
8. **ex-24 · assemble-streamed-tool-call** — assemble a streamed tool-call before executing — verify the
   full call is built. (co-12)
9. **ex-25 · provider-adapter-swap** — swap the fake for a second adapter with the same interface —
   verify the loop is unchanged. (co-13)
10. **ex-26 · loop-transcript-log** — log every turn's messages/tools/results to a transcript — verify a
    replayable record. (co-19)
11. **ex-27 · replay-a-transcript** — reconstruct a session from its transcript against the fake — verify
    identical behavior. (co-18, co-19)
12. **ex-28 · idempotent-tool-side-effect** — make a side-effecting tool safe under retry — verify no
    double-apply. (co-20)
13. **ex-29 · tool-args-validation** — validate tool arguments before executing — verify a bad arg is
    rejected with feedback. (co-05, co-15)
14. **ex-30 · final-answer-vs-tool-ambiguity** — handle a turn with both text and a tool call — verify
    the loop resolves it deterministically. (co-08, co-05)
15. **ex-31 · conversation-continuation** — continue a session with a new user turn preserving history —
    verify context carries. (co-03, co-21)
16. **ex-32 · cost-report** — summarize a session's total tokens/cost/turns — verify the report. (co-16)
17. **ex-33 · structured-final-output** — require the final answer in a structured schema — verify it
    validates. (co-08)
18. **ex-34 · multi-step-tool-task** — a task needing 3+ tool iterations (read → compute → write) —
    verify the loop reaches the goal. (co-02, co-17)

### Advanced (ex 35–48)

1. **ex-35 · file-editing-agent** — an agent with read/write/list tools that edits a file to spec —
   verify the file matches the target. (co-06, co-22)
2. **ex-36 · shell-running-agent** — an agent with a (bounded) shell tool that runs a command and reads
   output — verify the command result feeds back. (co-06, co-15)
3. **ex-37 · tdd-driving-agent** — an agent given a failing test that iterates to green — verify the
   red→green transition. (co-02, co-15)
4. **ex-38 · streaming-full-loop** — a fully streaming loop (streamed text + streamed tool calls) —
   verify correctness matches the non-streaming version. (co-11, co-12)
5. **ex-39 · budget-and-turn-limits-together** — enforce both a turn cap and a budget — verify whichever
   trips first stops the loop. (co-09, co-10, co-16)
6. **ex-40 · robust-error-recovery** — inject model + tool + timeout failures and recover from each —
   verify the loop survives and reports. (co-14, co-15)
7. **ex-41 · observable-agent-run** — structured per-turn logging + a run summary — verify the trace is
   complete and inspectable. (co-19)
8. **ex-42 · deterministic-test-suite** — a full `pytest` suite of the loop against the fake (stops,
   budgets, errors, multi-tool) — verify all pass with no live calls. (co-18)
9. **ex-43 · pluggable-stop-policy** — inject a stop-condition policy object — verify swapping policies
   changes termination. (co-09)
10. **ex-44 · human-in-the-loop-gate** — pause for human approval before a risky tool call — verify the
    loop waits and resumes. (co-09, co-14)
11. **ex-45 · resumable-session** — persist + resume a session from its message history — verify it
    continues correctly. (co-03, co-20)
12. **ex-46 · concurrent-agents** — run two independent agent loops concurrently — verify no shared-state
    interference. (co-03, co-17)
13. **ex-47 · agent-with-browser-tool** — wire the [CDP browser service](./browser-automation-with-cdp.md)
    as a tool so the agent can navigate + read a page — verify a browsing task completes. (co-06, co-22)
14. **ex-48 · capstone-mini-coding-agent** — a working mini coding agent: system prompt + file/shell
    tools + streaming + stops + budget + error feedback + transcript — verify it completes a small coding
    task end to end. (co-01–co-22)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: build a **minimal but complete coding agent loop** — a configurable provider adapter, a
  system prompt, a small tool registry (read/write/list files, run a bounded shell command), the
  read-eval-act loop with streaming, stop conditions (final answer, max turns, budget), tool-error
  feedback, and a replayable transcript — driving a small real coding task to completion.
- **Concepts exercised**: [ ] the loop + message history + system prompt (co-02–co-04) [ ] tool request/
  execute/result (co-05–co-07) [ ] stop conditions + max turns + budget (co-09, co-10, co-16)
  [ ] streaming text + tool calls (co-11, co-12) [ ] provider adapter + deterministic tests (co-13,
  co-18) [ ] error/tool-error feedback (co-14, co-15) [ ] observability transcript (co-19).
- **Ordered steps**:
  1. `the-agent-loop/learning/capstone/code/` — the provider adapter (with a fake for tests) + a tool
     registry. Verify the fake-backed loop is deterministic under `pytest`.
  2. Implement the read-eval-act loop with stop conditions + max turns + a budget. Verify it terminates
     on each condition.
  3. Add streaming, tool-error feedback, and a transcript log. Verify streaming parity and a replayable
     transcript.
  4. Run the agent against a small real coding task (edit a file to pass a test). Verify the red→green
     transition and a complete transcript.
- **Acceptance criteria**: the agent completes a small coding task via the loop; every stop condition
  works; tool and model errors are fed back and recovered; the run produces a complete, replayable
  transcript; the deterministic test suite passes with no live model calls.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

- **ReAct: Synergizing Reasoning and Acting in Language Models** — Yao et al. (2022). The foundational
  reasoning-and-acting pattern the loop implements. <https://arxiv.org/abs/2210.03629>
- **Building Effective Agents** — Anthropic (2024). Practical patterns distinguishing workflows from
  agents. <https://www.anthropic.com/engineering/building-effective-agents>

## In which paths

- `job-seeking-software-engineer` — Phase 3 · Deepening (shallow → deep) — AI & harness engineering
  (marquee build-your-own track).
- `software-engineer` — Stage 4 · Systems, data, architecture, security & ops depth (shallow → deep) —
  AI & harness engineering (marquee build-your-own track).

---

← Back to [README.md — course library catalog](./README.md)

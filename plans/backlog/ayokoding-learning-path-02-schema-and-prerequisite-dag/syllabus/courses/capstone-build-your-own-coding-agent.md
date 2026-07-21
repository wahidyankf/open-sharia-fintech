# Capstone: Build Your Own Coding Agent (Harness milestone, Python)

**Course ID**: `capstone-build-your-own-coding-agent` · **Kind**: Harness milestone · **Language**:
Python. **NEW** — the flagship of the harness-engineering cluster; an optional browser-driving bonus
ties the harness cluster and browser-automation course together.

**Scope note**: the marquee build — assemble the entire harness cluster (`the-agent-loop`,
`agent-tools-and-mcp`, `agent-context-and-memory`, `agent-permissions-and-sandboxing`,
`agent-orchestration-subagents-and-observability`) into **one working coding agent** the reader builds
themselves: a Claude-Code-shaped local coding assistant that reads a repo, plans, edits files, runs
tools/tests, manages its context, respects permissions and sandboxing, and is observable. **Optional
bonus**: drive the `browser-automation-with-cdp` service over MCP so the agent can also research on the
web — the `remotebrowser`↔MCP synergy payoff.

## Why this exists · the big idea

- **The problem before the solution**: the cluster taught each agent subsystem in isolation. Nothing yet
  proves the reader can integrate them into a coherent, safe, observable coding agent — which is the
  whole point of the cluster and the clearest demonstration that "AI coding agents" are buildable
  software, not magic.
- **Keep-this-if-you-forget-everything**: a coding agent is the loop (`the-agent-loop`) + real tools
  (`agent-tools-and-mcp`) + managed context (`agent-context-and-memory`) + guardrails
  (`agent-permissions-and-sandboxing`) + observability
  (`agent-orchestration-subagents-and-observability`) — build all five and you have demystified the
  tools you use daily.
- **Big ideas touched**: `abstraction-and-its-cost` (each subsystem is a clean seam), `determinism-vs-
emergence` (deterministic engineering around a stochastic core), `security-by-design` (a code-editing
  agent must be safe by construction).

## Prerequisites

- **Prior courses**: the full harness cluster (`the-agent-loop` through
  `agent-orchestration-subagents-and-observability`); `browser-automation-with-cdp` for the optional
  bonus; `async-python-and-fastapi-services` for the async/MCP substrate; `software-engineering-practices`
  for the TDD discipline the agent drives.
- **Tools & environment**: a macOS/Linux terminal; Python 3.x under `uv`; an LLM API with tool calling
  (provider-agnostic behind an adapter; keys via env); a container/OS sandbox; a vector store; an MCP
  library; `pytest`; Neovim/VSCode — all pinned CVE-clean at authoring.
- **Assumed knowledge**: every cluster subsystem individually; async Python; the no-secrets rule.

## Accuracy notes

> Pre-authoring `web-researcher` sweep pending (per this plan's Anti-Hallucination verification recipe).

- 2026-07-19 — `[Needs Verification]`: pin all cluster dependency versions (LLM SDK/adapter, MCP library,
  vector store, sandbox runtime, tracing/TUI libraries) at authoring; keep the model name configurable,
  never hard-coded. The integration architecture (loop + tools + context + permissions + observability)
  is stable.

## Concepts integrated

This capstone integrates the cluster's concepts; it introduces none of its own:

- [ ] The read-eval-act loop with streaming + stop conditions + budgets (`the-agent-loop`).
- [ ] Well-designed tools (fs read/write/list, bounded shell, test runner) + optional MCP servers
      (`agent-tools-and-mcp`).
- [ ] Context budgeting + compaction + retrieval over the repo + memory (`agent-context-and-memory`).
- [ ] Deny/ask/allow permissions + sandboxed execution + injection defense + secret hygiene + audit log
      (`agent-permissions-and-sandboxing`).
- [ ] Subagents (e.g. a research subagent) + tracing + metrics + an eval suite + a TUI
      (`agent-orchestration-subagents-and-observability`).
- [ ] (Optional bonus) The `browser-automation-with-cdp` service exposed over MCP for web research.

## Lineage & vocabulary — what the industry calls this, and whether it matters

- **The name the industry converged on**: what this cluster builds — the loop, the tools, the context
  management, the guardrails, the observability — began to be called **harness engineering** from late 2025. Anthropic used the framing on **2025-11-26**, OpenAI adopted it in its own agent material, and
  Birgitta Böckeler's Thoughtworks write-up (**2026-04-02**) gave it wider currency. The only academic
  definition of an **agent harness** (arXiv **2606.10106**) states four necessary conditions, and this
  cluster satisfies all four. `[Needs Verification]`: confirm every date, attribution, and the arXiv
  identifier against the primary source at authoring.
- **The term is contested — teach the disagreement, do not resolve it**. At time of writing the term is
  roughly five months old and named practitioners use it in **mutually contradictory** ways. OpenAI and
  Anthropic treat the **harness as the umbrella**, with context management as one component inside it.
  HumanLayer inverts the containment, treating the **harness as a subset of context engineering**. These
  are not compatible readings, and no authority has settled it. This course therefore **names the term
  and cites the disagreement** rather than adopting a side, and **nothing in this cluster is renamed
  after it** — building durable course structure on five-month-old contested vocabulary ages badly, and
  the material is stable in a way the vocabulary demonstrably is not. Note the adjacent precedent: the
  same cluster's context-management course records "prompt engineering" giving way to "context
  engineering" within 2025. The vocabulary in this field has already turned over once.
- **Does harness quality even matter? The evidence is genuinely contested.** Having just built one, the
  reader is well placed to weigh the dispute over whether it was worth building:
  - **METR** (independent, no vendor stake, **2026-02-13**) compared Claude Code against a generic ReAct
    scaffold and found Claude Code ahead in **50.7% of bootstrap samples** on Opus 4.5 — a coin flip.
    Codex beat Triframe in **14.5%** of samples.
  - **Scale AI / SWE-bench Pro** reports **large scaffold-driven swings**, with native scaffolds
    exploring substantially more than generic ones.
  - **A reconciliation — labelled as a synthesis, not a finding.** One way to hold both results together
    is that METR compared against a **competently built** generic baseline while Scale compared against
    **naive** ones, implying harness quality matters enormously **below a competence floor** and then
    flattens. **No single source makes this claim** — it is an inference across two bodies of evidence,
    and it is presented here as a synthesis the reader should interrogate, not as a result to memorize.
  - `[Needs Verification]`: re-verify both studies, their dates, the specific percentages, and the model
    versions evaluated at authoring. Benchmark results are revised and superseded.
  - **Do NOT cite the widely circulated 42%→78% scaffold claim.** It traces to no primary source.
- **Why this is durable content**: the vocabulary may turn over again and the benchmark numbers will be
  superseded, but the skill being taught here — weighing contested, vendor-interested evidence about a
  system you have just built yourself — survives both. That is the reason this section exists in a
  capstone rather than in a reading list.

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
6. (Optional bonus) Expose the `browser-automation-with-cdp` service as an MCP server and let the agent
   research a docs page before implementing. Verify the agent completes a task that required web
   research, driven over MCP.
7. **Weigh the evidence on your own build.** Benchmark the finished agent against a deliberately generic
   ReAct-style scaffold on the same task set, then write a short assessment reconciling your own result
   with the METR and Scale AI findings in the Lineage section above. Verify the write-up states which of
   the two your measurement resembles, identifies whether your generic baseline was competently or naively
   built (the variable the synthesis turns on), and distinguishes what your measurement can support from
   what it cannot — including whether it can distinguish the competence-floor synthesis from the
   alternative that harness quality simply matters less than assumed.

## Acceptance criteria

- The reader's own coding agent completes a real TDD coding task end to end — reading the repo, planning,
  editing files, running tests to green — while: staying within a context budget via compaction +
  retrieval; enforcing deny/ask/allow permissions and sandboxed execution that a red-team pass cannot
  escape or exfiltrate through; producing a complete trace + cost/latency metrics + a passing eval + an
  audit log; and driving interaction through a streaming TUI with an approval gate. The optional bonus
  additionally has the agent research the web over the browser MCP server before implementing. The
  deterministic test suite passes with no live model calls; no secret is ever committed or placed in the
  model's context.
- The reader additionally produces a written assessment of the contested evidence on whether harness
  quality matters, benchmarked against their own generic-scaffold baseline. It must name the
  competence-floor reconciliation **as a synthesis rather than as a finding any single source reports**,
  state the limits of the reader's own measurement, and cite neither the 42%→78% scaffold claim nor any
  harness-engineering definition as settled — the term's containment relationship is recorded as
  disputed, not resolved.

## Done bar

Runnable end-to-end (the agent completes a real coding task with every subsystem provably active) +
web-verified.

## In which paths

- `interview-ready/software-engineer` — Go deeper · AI & harness engineering — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · AI & harness engineering (marquee build-your-own track) — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 12 · AI & harness engineering (marquee build-your-own track).

---

← Back to [README.md — course library catalog](./README.md)

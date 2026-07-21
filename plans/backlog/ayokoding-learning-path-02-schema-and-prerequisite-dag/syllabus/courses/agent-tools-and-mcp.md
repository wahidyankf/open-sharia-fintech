# Agent Tools & MCP (By Example, Python)

**Course ID**: `agent-tools-and-mcp` · **Format**: By Example · **Language**: Python. **NEW** — the
same MCP `remotebrowser` exposes. Cluster language Python (matching `remotebrowser` and the series'
agentic-AI courses).

**Scope note**: giving an agent **capabilities** — designing tools (name, description, typed argument
schema), the function-calling contract the model uses to invoke them, and the **Model Context Protocol
(MCP)**: building an MCP **server** that exposes tools/resources/prompts and an MCP **client** the agent
loop consumes. Builds directly on `the-agent-loop` (which dispatches tools)
and connects to `browser-automation-with-cdp` (the browser
exposed as an MCP tool — the `remotebrowser` pattern).

## Why this exists · the big idea

- **The problem before the solution**: an agent loop with no tools can only talk. Its usefulness is
  exactly the tools it can call — and hand-wiring every tool into every agent does not scale. MCP is the
  standard that lets any tool provider expose capabilities once and any agent consume them, the way a
  web API decoupled clients from servers.
- **Keep-this-if-you-forget-everything**: a tool is a named function with a described, typed schema the
  model can choose to call; MCP is the open protocol that lets tools live in a separate server and be
  discovered and called over a standard interface.
- **Big ideas touched**: `abstraction-and-its-cost` (a schema is the contract between a stochastic model
  and deterministic code), `interfaces-over-implementations` (MCP decouples tool providers from agents).

## Prerequisites

- **Prior topics**: `the-agent-loop` (tool dispatch), `async-python-and-fastapi-services` (JSON-RPC-shaped servers, async),
  `api-design` (contract design), `just-enough-python`.
- **Tools & environment**: a macOS/Linux terminal; Python 3.x under `uv`; an MCP SDK/library (e.g.
  `fastmcp` or the reference MCP SDK, pinned CVE-clean at authoring); the agent loop from
  `the-agent-loop`; `pytest`; Neovim/VSCode.
- **Assumed knowledge**: JSON schemas, the agent loop's tool dispatch, async Python, and the request/
  response + event model.

## Accuracy notes

> Pre-authoring `web-researcher` sweep pending (per this plan's Anti-Hallucination verification recipe).

- 2026-07-18 — MCP is an **open protocol over JSON-RPC 2.0** with a Hosts / Clients / Servers
  architecture exposing **Resources, Prompts, and Tools**; this architecture is stable. `[Needs
Verification]`: the exact current spec revision (a dated schema is published) and any recent transport
  changes — cite the exact revision read at authoring.
- 2026-07-18 — `[Needs Verification]`: the tool/function-calling message schema differs by model
  provider — build tools against an adapter and pin the SDK versions at authoring.
- 2026-07-18 — `[Needs Verification]`: the chosen MCP library's API (`fastmcp` vs reference SDK) and its
  version — pin and re-verify at authoring.
- 2026-07-20 — **co-23 evidence, durability split**. The **effect** is durable spine: selection accuracy
  declines as tool count rises, so tool-surface size is a design constraint. The **measurements** are
  dated and belong here only. Reported evidence: the **Berkeley Function-Calling Leaderboard** shows a
  universal decline across evaluated models as tool count increases; a **GeoEngine** benchmark reports a
  model failing a task with **46 tools** available and succeeding with **19**. `[Needs Verification]`:
  re-verify both sources, their exact figures, and the model set evaluated before authoring — leaderboard
  contents and benchmark revisions change. Never place a specific tool-count threshold in the spine; the
  transferable claim is the direction of the effect, not a number.
- 2026-07-20 — **co-24 durability**: that tool results consume recurring context budget is architectural
  and durable. Any per-provider cost, truncation default, or context-window figure used to quantify it is
  volatile — read it from configuration and re-verify at authoring.

## Concepts

1. **co-01 · what-a-tool-is** — a tool is a named, described function with a typed argument schema that a
   model may choose to invoke.
2. **co-02 · tool-schema-design** — a good tool has a clear name, a precise description, and a strict
   argument schema so the model calls it correctly.
3. **co-03 · description-quality** — the description is prompt engineering: it is how the model decides
   when and how to use the tool.
4. **co-04 · typed-argument-schemas** — JSON-schema (or Pydantic-derived) argument definitions constrain
   and validate what the model passes.
5. **co-05 · function-calling-contract** — the model returns a structured call (name + args); the loop
   executes it and returns a typed result.
6. **co-06 · tool-result-shape** — a tool returns a structured, model-readable result (and a clear error
   shape on failure).
7. **co-07 · tool-granularity** — tools should be neither too coarse (ambiguous) nor too fine (too many
   calls); granularity is a design judgment.
8. **co-08 · what-mcp-is** — the Model Context Protocol is an open JSON-RPC-based standard connecting
   agents (clients) to capability providers (servers).
9. **co-09 · mcp-architecture** — Hosts embed Clients that connect to Servers exposing Resources,
   Prompts, and Tools.
10. **co-10 · mcp-tools** — an MCP server advertises callable tools with schemas that a client can
    discover and invoke.
11. **co-11 · mcp-resources** — an MCP server exposes readable resources (files, data) an agent can load
    into context.
12. **co-12 · mcp-prompts** — an MCP server can expose reusable, parameterized prompt templates.
13. **co-13 · mcp-transport** — MCP runs over a transport (stdio, HTTP/streaming) carrying JSON-RPC
    messages.
14. **co-14 · building-an-mcp-server** — implementing a server that registers tools/resources/prompts
    and handles discovery + invocation.
15. **co-15 · building-an-mcp-client** — a client connects to a server, lists its capabilities, and
    calls them.
16. **co-16 · connecting-mcp-to-the-loop** — the agent loop discovers MCP tools and dispatches the
    model's tool calls to the server.
17. **co-17 · tool-discovery** — an agent enumerates available tools at startup rather than hard-coding
    them.
18. **co-18 · error-and-validation-at-the-boundary** — the server validates arguments and returns clear
    errors; the client surfaces them to the model.
19. **co-19 · security-at-the-tool-boundary** — a tool executes real actions, so its inputs are untrusted
    and must be validated and constrained (links forward to `agent-permissions-and-sandboxing`).
20. **co-20 · versioning-and-compatibility** — tool/schema changes must stay backward compatible or be
    versioned so agents do not break.
21. **co-21 · composing-multiple-servers** — an agent can connect to several MCP servers at once,
    composing capabilities from many providers.
22. **co-22 · exposing-a-service-as-mcp** — wrapping an existing service (e.g. the
    [browser service](./browser-automation-with-cdp.md)) as an MCP server makes it usable by any agent
    — the `remotebrowser` pattern.
23. **co-23 · tool-count-degradation** — tool-selection accuracy **declines as the number of available
    tools rises**, and the decline is measurable rather than anecdotal. This is the quantified form of
    the granularity aside in Tensions & trade-offs: it is not merely that fifty micro-tools "confuse"
    the model, it is that every additional tool in the schema costs selection accuracy across models.
    This is the governing constraint on when to **split a tool surface across subagents** or **filter
    the advertised tool set per turn** rather than advertising everything the agent could ever call.
24. **co-24 · tool-result-token-efficiency** — a tool's **result shape is a context-budget decision**.
    Tool results enter the model's context and are re-read on every subsequent turn, so a verbose result
    is a recurring cost, not a one-off one. Returning the fields the model needs — rather than a
    service's full response payload — is a first-class part of tool design, alongside the name,
    description, and argument schema.

## Tensions & trade-offs — when NOT to reach for this

- **Standard protocol vs direct wiring**: MCP decouples tools from agents at the cost of a protocol
  layer. For a single agent with three fixed tools, direct wiring is simpler; MCP pays off when tools are
  reused across agents or provided by others.
- **Tool power vs safety**: the more a tool can do (run shell, write files, hit the network), the more
  damage a wrong call does. Powerful tools demand the validation and permission machinery of
  `agent-permissions-and-sandboxing` — do not ship a raw shell tool ungated.
- **Granularity**: one giant "do anything" tool is unusable by the model; fifty micro-tools bloat the
  schema and confuse it. The design skill is carving tools at the joints of the task. This is not only a
  judgment call — the degradation is measurable (co-23), which turns "how many tools is too many" from a
  matter of taste into something you can test on your own suite and act on by filtering per turn or
  splitting across subagents.
- **Capability vs recurring context cost**: every tool you advertise costs schema tokens on every turn,
  and every tool result costs context for the rest of the session (co-24). A tool surface is not free
  just because it is unused — reach for the smallest surface that covers the task, not the largest one
  you can assemble.

## Lineage — why it beat the alternative

- Early agent tools were hard-coded per agent, so every integration was bespoke and non-portable. MCP
  emerged (JSON-RPC-based, vendor-neutral) to do for agent capabilities what HTTP APIs did for services:
  a provider exposes tools/resources/prompts once, and any conforming agent consumes them. This turned a
  combinatorial integration problem into a standard one, and made services like `remotebrowser`
  reusable across harnesses by exposing an MCP server. This module gives the [agent
  loop](./the-agent-loop.md) its capabilities; `agent-permissions-and-sandboxing` constrains them and
  `agent-orchestration-subagents-and-observability` composes them.
- **What the industry calls this cluster**: from late 2025 this body of work — the loop, its tools, its
  context, its guardrails, its observability — began to be called **harness engineering** (Anthropic
  2025-11-26; OpenAI; Böckeler/Thoughtworks 2026-04-02). The term is **~5 months old and contested** —
  OpenAI and Anthropic treat the harness as the umbrella containing context management, while HumanLayer
  treats it as a subset of context engineering — so this cluster **names the term and cites the
  disagreement without adopting a side, and renames nothing**. Full treatment in the
  [coding-agent capstone](./capstone-build-your-own-coding-agent.md). `[Needs Verification]`: confirm
  dates and attributions at authoring; treat the vocabulary as volatile.

## Worked examples

Colocated under `agent-tools-and-mcp/learning/code/`. Tools + MCP servers/clients in Python, wired to
the `the-agent-loop`; a fake model keeps tests deterministic. Contiguous
`ex-01..ex-54`. Every example cites the `co-NN` it exercises.

> **Volume-target floor**: this syllabus lists **54** of the required **≥75** (the 75–85 By-Example/
> Primer band, floor not cap — see
> [prd.md §Volume-target bands](../../prd.md#new-course--capstone-specifications)).
> The maker adds **≥21** more `ex-NN` entries at authoring time, continuing the numbering and pattern
> taxonomy below, before this topic passes its by-example quality gate.

### Beginner (ex 01–16)

1. **ex-01 · define-a-tool** — a named function + description + typed args — verify the schema is
   well-formed. (co-01, co-02)
2. **ex-02 · pydantic-arg-schema** — derive a tool's argument schema from a Pydantic model — verify
   validation. (co-04)
3. **ex-03 · good-vs-bad-description** — contrast two descriptions and observe the fake model's tool
   choice — verify the clearer one is chosen. (co-03)
4. **ex-04 · function-calling-roundtrip** — model requests a tool, loop executes, result returns —
   verify the round-trip. (co-05, co-06)
5. **ex-05 · structured-tool-result** — return a structured result the model can read — verify the
   shape. (co-06)
6. **ex-06 · tool-error-shape** — return a clear error result on failure — verify the model receives it.
   (co-06, co-18)
7. **ex-07 · validate-args-before-run** — reject an out-of-schema argument — verify the rejection. (co-04,
   co-18)
8. **ex-08 · tool-granularity-contrast** — one coarse tool vs two focused tools for a task — verify the
   focused pair is easier for the model. (co-07)
9. **ex-09 · hello-mcp-server** — a minimal MCP server exposing one tool — verify it starts and
   advertises the tool. (co-08, co-14)
10. **ex-10 · hello-mcp-client** — a client that connects + lists the server's tools — verify discovery.
    (co-15, co-17)
11. **ex-11 · call-an-mcp-tool** — the client invokes the server's tool — verify the JSON-RPC result.
    (co-10, co-15)
12. **ex-12 · mcp-over-stdio** — run the server/client over stdio transport — verify messages flow.
    (co-13)
13. **ex-13 · mcp-resource** — expose a readable resource on the server — verify the client reads it.
    (co-11)
14. **ex-14 · mcp-prompt-template** — expose a parameterized prompt — verify the client fetches it.
    (co-12)
15. **ex-15 · connect-mcp-to-loop** — the [agent loop](./the-agent-loop.md) discovers + calls an MCP
    tool — verify the model's call reaches the server. (co-16)
16. **ex-16 · tool-discovery-at-startup** — the agent enumerates tools at startup, none hard-coded —
    verify the tool list is dynamic. (co-17)

### Intermediate (ex 17–34)

1. **ex-17 · multi-tool-mcp-server** — a server exposing several tools (fs read, fs write, search) —
   verify each is callable. (co-10, co-14)
2. **ex-18 · mcp-over-http** — run the server over an HTTP/streaming transport — verify remote
   invocation. (co-13)
3. **ex-19 · argument-validation-server-side** — the server validates + rejects bad args — verify a
   clear error to the client. (co-18, co-04)
4. **ex-20 · compose-two-servers** — the agent connects to two MCP servers and uses tools from both —
   verify composition. (co-21)
5. **ex-21 · tool-namespacing** — namespace tools across servers to avoid collisions — verify
   disambiguation. (co-21, co-20)
6. **ex-22 · resource-into-context** — the agent loads an MCP resource into its context before a task —
   verify it is used. (co-11, co-16)
7. **ex-23 · prompt-template-reuse** — the agent uses an MCP prompt template for a task — verify the
   parameterized prompt. (co-12)
8. **ex-24 · fs-tool-with-bounds** — a filesystem tool restricted to a sandbox dir — verify an
   out-of-bounds path is rejected. (co-19)
9. **ex-25 · shell-tool-gated** — a shell tool that validates the command against an allow-list — verify
   a disallowed command is blocked. (co-19)
10. **ex-26 · versioned-tool-schema** — evolve a tool's schema backward-compatibly — verify old + new
    calls both work. (co-20)
11. **ex-27 · tool-result-truncation** — truncate a large tool result to fit context, noting truncation —
    verify the note. (co-06)
12. **ex-28 · concurrent-mcp-calls** — the agent issues concurrent MCP tool calls — verify results merge.
    (co-15, co-05)
13. **ex-29 · server-error-recovery** — the server tool fails; the client feeds the error to the model —
    verify recovery. (co-18, co-06)
14. **ex-30 · deterministic-mcp-tests** — test the server/client against a fake model + a test client —
    verify no live calls. (co-14, co-15)
15. **ex-31 · describe-for-the-model** — iterate a tool description until the fake model uses it
    correctly — verify improved selection. (co-03)
16. **ex-32 · schema-driven-client** — the client builds calls purely from discovered schemas — verify no
    hard-coded shapes. (co-17, co-04)
17. **ex-33 · resource-listing-and-read** — list + read multiple resources from a server — verify each.
    (co-11)
18. **ex-34 · mcp-inspector-check** — inspect a server's advertised capabilities with a tooling client —
    verify tools/resources/prompts are listed. (co-09, co-17)

### Advanced (ex 35–54)

1. **ex-35 · browser-mcp-server** — wrap the [CDP browser service](./browser-automation-with-cdp.md)
   as an MCP server exposing navigate/evaluate/screenshot tools — verify a client drives the browser via
   MCP. (co-22, co-14)
2. **ex-36 · agent-drives-browser-over-mcp** — the [agent loop](./the-agent-loop.md) uses the browser
   MCP server to complete a browsing task — verify the task completes. (co-16, co-22)
3. **ex-37 · compose-fs-shell-browser** — an agent composing filesystem, shell, and browser MCP servers
   — verify a task using all three. (co-21, co-22)
4. **ex-38 · remotebrowser-shaped-pool** — a browser MCP server backed by a bounded pool — verify
   concurrent agent tool calls are serviced. (co-22, co-19)
5. **ex-39 · tool-permission-boundary** — enforce per-tool allow/deny at the MCP boundary — verify a
   denied tool cannot be called. (co-19)
6. **ex-40 · streaming-tool-result** — stream a long tool result back incrementally — verify chunks
   arrive. (co-13, co-06)
7. **ex-41 · robust-tool-suite** — a tool suite with validation, errors, timeouts, and bounds — verify
   it survives hostile inputs. (co-18, co-19)
8. **ex-42 · schema-evolution-migration** — migrate an agent across a tool-schema version bump — verify
   no breakage. (co-20)
9. **ex-43 · capability-manifest** — generate a manifest of all connected servers' capabilities — verify
   it is complete. (co-09, co-21)
10. **ex-44 · tool-usage-analytics** — log which tools the agent calls and how often — verify the
    analytics. (co-16)
11. **ex-45 · sandboxed-tool-execution** — run a tool inside a sandbox boundary (preview of
    `agent-permissions-and-sandboxing`) — verify isolation. (co-19)
12. **ex-46 · multi-agent-shared-server** — two agents sharing one MCP server concurrently — verify no
    cross-talk. (co-21, co-19)
13. **ex-47 · design-review-a-tool-api** — critique + redesign a poorly-carved tool API — verify the
    redesign improves granularity + descriptions. (co-02, co-03, co-07)
14. **ex-48 · portable-tool-across-agents** — the same MCP tool used by two different agent loops —
    verify portability. (co-08, co-16)
15. **ex-49 · end-to-end-mcp-agent** — an agent using multiple MCP servers to complete a multi-tool task
    with validation + error handling — verify the goal. (co-16, co-18, co-21)
16. **ex-50 · tool-count-degradation-curve** — run the same task suite with 5, 19, and 46 tools
    advertised — verify selection accuracy declines as the count rises, and that the decline is measured
    on the learner's own suite rather than quoted from a benchmark. (co-23, co-07)
17. **ex-51 · filter-tools-per-turn** — advertise only the tools plausibly relevant to the current turn
    instead of the whole registry — verify selection accuracy recovers at the same total capability.
    (co-23, co-17)
18. **ex-52 · split-tool-surface-across-subagents** — partition a large tool surface across two
    specialized agents rather than exposing all of it to one — verify each agent's smaller surface
    outperforms the combined one. (co-23, co-21)
19. **ex-53 · trim-a-tool-result** — return only the fields the model needs instead of the service's full
    response payload — verify identical task success at materially fewer context tokens, and that the
    saving recurs on every subsequent turn. (co-24, co-06)
20. **ex-54 · capstone-tool-provider** — a complete MCP server (tools + resources + prompts, validated,
    versioned, bounded, token-efficient results, and a per-turn-filtered advertised surface) plus a
    client-integrated agent that uses it — verify the agent completes a task entirely through the server.
    (co-01–co-24)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: build a complete **MCP tool provider** — a server exposing well-designed tools (with typed
  schemas + clear descriptions), one resource, and one prompt template, validated and bounded — and wire
  it into the [agent loop](./the-agent-loop.md) so the agent discovers and uses it to complete a task,
  including (optionally) the [browser service](./browser-automation-with-cdp.md) exposed as MCP.
- **Concepts exercised**: [ ] tool schema + description design (co-01–co-04, co-07) [ ] function-calling
  contract + result shape (co-05, co-06) [ ] MCP server: tools + resources + prompts (co-09–co-14)
  [ ] MCP client + discovery + loop integration (co-15–co-17) [ ] boundary validation + security (co-18,
  co-19) [ ] service-as-MCP (co-22) [ ] a tool surface sized against measured selection degradation
  (co-23) [ ] token-efficient tool results (co-24).
- **Ordered steps**:
  1. `agent-tools-and-mcp/learning/capstone/server/` — an MCP server exposing 3+ validated tools + a
     resource + a prompt. Verify a test client lists + calls each capability.
  2. `agent-tools-and-mcp/learning/capstone/client/` — connect the agent loop to the server via
     discovery. Verify the agent calls a tool the server provides.
  3. Add boundary validation + a per-tool permission check + a clear error path. Verify a denied/invalid
     call is rejected cleanly.
  4. (Optional bonus) Expose the browser service as MCP and have the agent complete a browsing task.
     Verify the task completes through MCP.
- **Acceptance criteria**: the agent completes a task using only tools discovered from the MCP server;
  every tool validates its arguments and returns clear results/errors; a permission boundary blocks a
  disallowed tool; the deterministic test suite passes with no live model calls.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

- **Model Context Protocol specification** — the authoritative reference for the protocol, its
  architecture, and the dated schema revision (cite the exact revision at authoring).
- **Building Effective Agents** — Anthropic (2024). On tool design and agent capability patterns.
  <https://www.anthropic.com/engineering/building-effective-agents>

## In which paths

- `interview-ready/software-engineer` — Go deeper · AI & harness engineering — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · AI & harness engineering (marquee build-your-own track) — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 12 · AI & harness engineering (marquee build-your-own track).

---

← Back to [README.md — course library catalog](./README.md)

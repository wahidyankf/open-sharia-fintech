# Agent Context & Memory (Annotated-concept, Python)

**Course ID**: `agent-context-and-memory` · **Format**: Annotated-concept · **Language**: Python.
**NEW** — part of the harness-engineering cluster (cluster language Python, matching `remotebrowser`
and the series' agentic-AI courses).

**Scope note**: managing what an agent knows — the finite **context window** as a budget, **compaction**
(summarizing history to fit), **retrieval** (pulling in only relevant knowledge), and **memory**
(short-term working state vs long-term persisted memory). Annotated-concept: code where it clarifies
(token counting, a retrieval index, a compaction routine), prose + WCAG-accessible Mermaid diagrams
where architecture is the point. Extends `the-agent-loop` (whose message
history is the raw context) and draws on `creating-ai-powered-apps` (embeddings/RAG).

## Why this exists · the big idea

- **The problem before the solution**: the context window is finite and every token costs money and
  attention. A naive agent that appends everything eventually overflows, degrades (lost-in-the-middle),
  and gets expensive. Deciding _what the model sees_ is the single highest-leverage lever on agent
  quality and cost.
- **Keep-this-if-you-forget-everything**: context is a budget you curate, not a bucket you fill —
  compact what is stale, retrieve what is relevant, remember what matters, and drop the rest.
- **Big ideas touched**: `abstraction-and-its-cost` (a summary is a lossy compression of history — cheap
  but forgetful), `taming-state` (short-term vs long-term memory is the agent's state model).

## Prerequisites

- **Prior topics**: `the-agent-loop` (message history),
  `creating-ai-powered-apps` (embeddings, vector search, RAG),
  `search-and-information-retrieval` (retrieval fundamentals),
  `just-enough-python`.
- **Tools & environment**: a macOS/Linux terminal; Python 3.x under `uv`; a tokenizer library; an
  embedding model + a vector store (pinned CVE-clean at authoring); the agent loop from
  `the-agent-loop`; Neovim/VSCode.
- **Assumed knowledge**: the agent loop, embeddings + similarity search at a basic level, and JSON.

## Accuracy notes

> Pre-authoring `web-researcher` sweep pending (per this plan's Anti-Hallucination verification recipe).

- 2026-07-18 — context windows, tokenization, retrieval-augmented generation, and the short-term vs
  long-term memory distinction are **stable, vendor-independent** concepts.
- 2026-07-18 — `[Needs Verification]`: exact context-window sizes and tokenizer behavior are model-
  specific — never hard-code a window size; read it from config and re-verify at authoring.
- 2026-07-18 — `[Needs Verification]`: the chosen embedding model + vector store versions and APIs — pin
  at authoring; the "lost-in-the-middle" degradation is a documented, evolving research finding — cite
  the source read at authoring.
- 2026-07-20 — **co-23 durability split**. The **principle** is durable spine: order context
  stable-before-variable so a reusable prefix survives across calls. The **mechanism** is volatile and
  belongs only in this note — providers differ, and at time of writing Anthropic uses **explicit cache
  breakpoints** the caller places, while OpenAI applies an **automatic threshold reported as 1,024
  tokens**. `[Needs Verification]`: both mechanisms, the threshold figure, and any discount or TTL
  numbers are vendor-specific and change — re-verify against primary provider documentation at
  authoring, and never state co-23 in terms of one vendor's mechanism.

## Concepts

1. **co-01 · context-window-as-budget** — the model reasons only over a finite token window; every token
   spent on stale content is a token unavailable for the task.
2. **co-02 · tokenization-and-counting** — text is split into tokens; counting them is how you measure
   and enforce the budget.
3. **co-03 · what-goes-in-context** — the system prompt, task, relevant history, retrieved knowledge, and
   tool results all compete for the same budget.
4. **co-04 · context-degradation** — models attend unevenly across a long context ("lost in the
   middle"), so more context is not always better.
5. **co-05 · pruning-stale-context** — dropping irrelevant or superseded messages preserves budget and
   focus.
6. **co-06 · compaction-by-summarization** — replacing a long history span with a concise summary keeps
   the gist while freeing tokens.
7. **co-07 · summarization-tradeoffs** — a summary is lossy; what it omits is gone, so compaction must
   preserve decisions and open threads.
8. **co-08 · rolling-window** — keeping the most recent N turns verbatim plus a running summary of older
   ones bounds the history.
9. **co-09 · retrieval-augmented-context** — pulling only the relevant documents/snippets into context on
   demand beats loading everything.
10. **co-10 · embeddings-and-similarity** — embedding text into vectors lets similarity search find
    relevant knowledge for a query.
11. **co-11 · vector-store** — an index of embeddings supports fast nearest-neighbor retrieval.
12. **co-12 · chunking-strategy** — how documents are split into chunks shapes retrieval quality.
13. **co-13 · retrieval-relevance-and-reranking** — filtering and reranking retrieved candidates
    improves what actually enters context.
14. **co-14 · short-term-memory** — the current session's working state (recent turns, scratchpad) is
    short-term memory.
15. **co-15 · long-term-memory** — knowledge persisted across sessions (facts, preferences, prior
    outcomes) is long-term memory.
16. **co-16 · memory-write-policy** — deciding what is worth remembering (and what is noise) is a
    deliberate policy, not automatic.
17. **co-17 · memory-retrieval-policy** — deciding when and what to recall into context is as important
    as what to store.
18. **co-18 · memory-staleness-and-conflict** — remembered facts can go stale or conflict; memory needs
    updating and conflict resolution.
19. **co-19 · working-scratchpad** — an explicit scratchpad/notes area lets the agent externalize
    intermediate reasoning outside the message stream.
20. **co-20 · context-assembly-pipeline** — assembling each turn's context is a pipeline: system + task +
    memory + retrieval + recent history, budgeted.
21. **co-21 · cost-and-latency-of-context** — larger context means higher cost and latency; budgeting is
    an economic decision, not only a quality one.
22. **co-22 · privacy-and-memory** — persisted memory can hold sensitive data; what is stored must
    respect privacy and the no-secrets rule.
23. **co-23 · cache-aware-prefix-ordering** — order context by **staleness, not by logical grouping**:
    put the parts that rarely change first and the parts that change every turn last, so the stable
    prefix stays reusable across calls. The principle is stable-before-variable and is
    provider-independent; only the mechanism that exploits it differs (see the accuracy note). Logical
    grouping — "all the tool definitions here, all the user context there" — feels tidier and destroys
    the reusable prefix by interleaving volatile content into stable regions.

## Tensions & trade-offs — when NOT to reach for this

- **Recall vs budget**: keeping everything maximizes recall but overflows the window, degrades
  attention, and costs more; aggressive compaction saves budget but forgets. The art is compacting the
  stale while preserving decisions and open threads.
- **Retrieval vs stuffing**: retrieval adds infrastructure (embeddings, a vector store, chunking) and a
  relevance-quality risk; for a small, fixed knowledge set, just including it can beat retrieving it.
  Reach for RAG when the knowledge is large or dynamic.
- **When NOT to persist memory**: long-term memory that stores the wrong things becomes a liability —
  stale facts poison future turns, and sensitive data creates a privacy risk. Not everything should be
  remembered.

## Lineage — why it beat the alternative

- Early agents simply appended every message until they hit the window and broke. As tasks grew, three
  ideas emerged to manage the budget: compaction (summarize the old), retrieval (fetch the relevant on
  demand, RAG), and explicit memory (persist what matters across sessions). Each trades completeness for
  a bounded, focused, affordable context. This is the state-management discipline the [agent
  loop](./the-agent-loop.md) needs to run long tasks, and it draws its retrieval machinery from
  `search-and-information-retrieval` and `creating-ai-powered-apps`. It feeds
  `agent-orchestration-subagents-and-observability`, where subagents are a
  context-isolation strategy.
- **What the industry calls this**: in **June 2025** this discipline acquired a name — **context
  engineering** — as practitioners converged on the observation that curating what the model sees had
  become the dominant lever, displacing "prompt engineering" as the framing. Tobi Lütke used the term on
  **2025-06-19**, Andrej Karpathy on **2025-06-25**, and Simon Willison wrote it up on **2025-06-27**;
  Anthropic published an **Effective Context Engineering** methodology on **2025-09-29**. The course you
  are reading teaches that discipline concept-for-concept and predates the label — the material did not
  change when the vocabulary did, which is exactly why the spine is organized around budgeting,
  compaction, retrieval, and memory rather than around a term. The name is given here so a learner can
  connect this material to the job-market vocabulary they will meet.
  `[Needs Verification]`: confirm each date and attribution against the primary source at authoring, and
  treat the vocabulary itself as volatile — it shifted once within 2025 and may shift again.
- **And what the industry calls the surrounding cluster**: from late 2025 the wider body of work — the
  loop, its tools, this course's context management, the guardrails, the observability — began to be
  called **harness engineering** (Anthropic 2025-11-26; OpenAI; Böckeler/Thoughtworks 2026-04-02). That
  term is **~5 months old and contested**, and the disagreement bears directly on this course: OpenAI and
  Anthropic treat the harness as the **umbrella containing** context management, while HumanLayer treats
  the harness as a **subset of** context engineering — an inverted containment relationship that no
  authority has settled. This cluster therefore **names both terms and cites the disagreement without
  adopting a side, and renames nothing**. Full treatment in the
  [coding-agent capstone](./capstone-build-your-own-coding-agent.md).

## Worked examples

No fixed Beginner/Intermediate/Advanced bands (Annotated-concept); grouped by theme. Code where it
clarifies (token counting, retrieval, compaction), diagrams where architecture is the point. Colocated
under `agent-context-and-memory/learning/code/` (runnable) and `.../artifacts/` (diagrams). Contiguous
`ex-01..ex-48`. Every example cites the `co-NN` it exercises.

### Theme A · The context budget (ex 01–12)

1. **ex-01 · count-tokens** — count the tokens of a message list with a tokenizer — verify against a
   known value. (co-02)
2. **ex-02 · budget-a-context** — assemble a context under a token ceiling — verify the total fits.
   (co-01, co-03)
3. **ex-03 · context-composition-diagram** — a Mermaid diagram of what competes for the budget (system,
   task, history, retrieval, tools) — verify each source is shown. (co-03)
4. **ex-04 · overflow-detection** — detect when a context would exceed the window — verify the guard
   fires. (co-01, co-02)
5. **ex-05 · lost-in-the-middle-demo** — place a key fact early, middle, late and observe recall
   (fake/real) — verify the middle is weakest. (co-04)
6. **ex-06 · prune-stale-messages** — drop superseded messages from history — verify the budget drops
   and the task still succeeds. (co-05)
7. **ex-07 · relevance-scored-inclusion** — include history messages by a relevance score under budget —
   verify only relevant ones remain. (co-05, co-13)
8. **ex-08 · cost-of-context-report** — report tokens + estimated cost per context assembly — verify the
   figures. (co-21)
9. **ex-09 · latency-vs-size** — measure latency as context grows — verify the trend. (co-21)
10. **ex-10 · budget-allocation-policy** — allocate the budget across sources (e.g. 20% memory, 40%
    retrieval, 40% history) — verify the split. (co-03, co-20)
11. **ex-11 · truncate-tool-results** — truncate a huge tool result to fit, noting the truncation —
    verify the note + fit. (co-05, co-03)
12. **ex-12 · budgeted-assembly-pipeline** — a pipeline assembling a budgeted context from all sources —
    verify it always fits the window. (co-20)

### Theme B · Compaction & summarization (ex 13–22)

1. **ex-13 · summarize-a-history-span** — summarize an old span of turns — verify the summary preserves
   the decisions. (co-06, co-07)
2. **ex-14 · rolling-window-plus-summary** — keep recent N turns verbatim + a running summary — verify
   the window is bounded. (co-08)
3. **ex-15 · compaction-preserves-open-threads** — verify a compaction keeps unresolved tasks/questions,
   not just facts. (co-07)
4. **ex-16 · lossy-compaction-failure** — a compaction that drops a needed detail, then a fix that
   preserves it — verify the failure and the fix. (co-07)
5. **ex-17 · trigger-compaction-on-budget** — trigger compaction when the budget crosses a threshold —
   verify it fires and frees tokens. (co-06, co-01)
6. **ex-18 · summary-quality-check** — verify a summary against the original for omitted decisions —
   verify the check flags gaps. (co-07)
7. **ex-19 · incremental-summary-update** — update a running summary each turn instead of resummarizing
   all — verify equivalence at lower cost. (co-08, co-21)
8. **ex-20 · compaction-in-the-loop** — integrate compaction into the [agent loop](./the-agent-loop.md)
   for a long task — verify the task completes within budget. (co-06, co-20)
9. **ex-21 · compaction-diagram** — a Mermaid diagram of the rolling-window-plus-summary strategy —
   verify the flow. (co-08)
10. **ex-22 · compare-compaction-strategies** — compare truncation vs summarization on a task — verify
    the trade-off in quality + cost. (co-05, co-06, co-07)

### Theme C · Retrieval-augmented context (ex 23–34)

1. **ex-23 · embed-text** — embed documents into vectors — verify vector dimensionality. (co-10)
2. **ex-24 · similarity-search** — nearest-neighbor search over embeddings for a query — verify the top
   hit is relevant. (co-10, co-11)
3. **ex-25 · build-a-vector-store** — index a document set in a vector store — verify retrieval. (co-11)
4. **ex-26 · chunking-strategy-contrast** — compare two chunk sizes' retrieval quality — verify the
   better recall. (co-12)
5. **ex-27 · retrieve-into-context** — retrieve top-k relevant chunks into the agent's context for a
   query — verify they are used. (co-09, co-20)
6. **ex-28 · rerank-candidates** — rerank retrieved candidates before inclusion — verify improved
   relevance. (co-13)
7. **ex-29 · relevance-threshold** — drop retrievals below a similarity threshold — verify noise is
   excluded. (co-13)
8. **ex-30 · retrieval-vs-stuffing** — compare RAG against including the whole small corpus — verify
   when each wins. (co-09)
9. **ex-31 · citation-of-retrieved-source** — attach source citations to retrieved context — verify the
   agent cites them. (co-09, co-13)
10. **ex-32 · retrieval-in-the-loop** — wire retrieval into each loop turn's context assembly — verify
    relevant knowledge appears per turn. (co-09, co-20)
11. **ex-33 · stale-index-refresh** — refresh the vector index when source docs change — verify updated
    retrievals. (co-18, co-11)
12. **ex-34 · retrieval-architecture-diagram** — a Mermaid diagram of the RAG pipeline (chunk → embed →
    store → retrieve → rerank → context) — verify each stage. (co-09, co-12, co-13)

### Theme D · Memory: short-term & long-term, and cache-aware assembly (ex 35–48)

1. **ex-35 · short-term-scratchpad** — an explicit scratchpad the agent writes intermediate notes to —
   verify it persists within a session. (co-14, co-19)
2. **ex-36 · persist-long-term-memory** — store a fact across sessions — verify recall in a new
   session. (co-15)
3. **ex-37 · memory-write-policy** — decide what to remember from a session by a policy — verify noise
   is not stored. (co-16)
4. **ex-38 · memory-retrieval-policy** — recall only relevant memories into context — verify irrelevant
   ones stay out. (co-17)
5. **ex-39 · memory-staleness** — detect + update a stale memory — verify the corrected value is used.
   (co-18)
6. **ex-40 · memory-conflict-resolution** — resolve two conflicting stored facts — verify a defined
   resolution. (co-18)
7. **ex-41 · memory-privacy-gate** — refuse to persist a secret/PII into memory — verify the gate blocks
   it. (co-22)
8. **ex-42 · memory-backed-agent-task** — an agent that uses long-term memory to personalize a task —
   verify the memory changes the outcome. (co-15, co-17)
9. **ex-43 · short-vs-long-memory-diagram** — a Mermaid diagram distinguishing session state from
   persisted memory — verify both are shown. (co-14, co-15)
10. **ex-44 · full-context-pipeline** — a complete assembly: system + task + long-term memory + retrieval
    - rolling history, budgeted — verify it always fits + is relevant. (co-20, co-03)
11. **ex-45 · memory-audit** — audit what an agent has stored for staleness + privacy — verify the audit
    report. (co-18, co-22)
12. **ex-46 · order-by-staleness-not-grouping** — reorder a logically-grouped context into
    stable-before-variable order (system + tools + retrieved corpus first, recent turns + live tool
    results last) — verify the reusable prefix is longer and byte-identical across consecutive turns.
    (co-23, co-20)
13. **ex-47 · one-volatile-field-destroys-the-prefix** — inject a timestamp near the top of an otherwise
    stable prefix, then move it to the tail — verify the prefix reuse collapses and is restored, and
    annotate the provider-mechanism difference from the accuracy note without depending on either.
    (co-23, co-21)
14. **ex-48 · capstone-context-managed-agent** — an agent with budgeting, compaction, retrieval, and
    memory completing a long multi-session task — verify it stays within budget, retrieves relevant
    knowledge, recalls memory across sessions, and assembles context in stable-before-variable order.
    (co-01–co-23)

## Capstone spec — intra-topic (concept → full runnable)

- **Goal**: extend the [agent loop](./the-agent-loop.md) with a full **context-management layer** —
  token budgeting, rolling-window-plus-summary compaction, retrieval-augmented context over a vector
  store, and short-term + long-term memory with write/retrieval policies and a privacy gate — running a
  long, multi-session task that would overflow a naive context.
- **Concepts exercised**: [ ] token budgeting + overflow guard (co-01, co-02) [ ] compaction + rolling
  window (co-06, co-08) [ ] retrieval + vector store + reranking (co-09–co-13) [ ] short-term + long-term
  memory + policies (co-14–co-17) [ ] staleness/conflict + privacy (co-18, co-22) [ ] budgeted assembly
  pipeline (co-20) [ ] cache-aware stable-before-variable ordering (co-23).
- **Ordered steps**:
  1. `agent-context-and-memory/learning/capstone/code/` — a token-budgeted context assembler with an
     overflow guard. Verify it never exceeds the window.
  2. Add rolling-window compaction + summarization. Verify a long history stays bounded and preserves
     decisions.
  3. Add a vector-store retrieval stage with reranking. Verify relevant knowledge enters context per
     turn.
  4. Add short-term + long-term memory with write/retrieval policies + a privacy gate. Verify recall
     across a session boundary and that a secret is never persisted.
  5. Order the assembled context stable-before-variable so the prefix is reusable across turns. Verify
     the prefix is byte-identical between consecutive turns and that moving one volatile field into it
     measurably shortens the reusable region.
- **Acceptance criteria**: the agent completes a long, multi-session task; context always fits the
  budget; compaction preserves decisions; retrieval surfaces relevant knowledge; memory recalls across
  sessions; no secret/PII is persisted; and context is assembled staleness-ordered so a reusable prefix
  survives across consecutive turns.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

- **Lost in the Middle: How Language Models Use Long Contexts** — Liu et al. The documented context-
  degradation finding motivating budgeting (cite the version read at authoring).
- **Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks** — Lewis et al. (2020). The
  foundational RAG paper. <https://arxiv.org/abs/2005.11401>

## In which paths

- `interview-ready/software-engineer` — Go deeper · AI & harness engineering — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · AI & harness engineering (marquee build-your-own track) — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 12 · AI & harness engineering (marquee build-your-own track).

---

← Back to [README.md — course library catalog](./README.md)

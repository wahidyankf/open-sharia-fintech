# 56 · Creating AI-Powered Apps (By Example, Python)

**prd row**: Pass 3 · Build for the Real World · By Example · Python · Learn 156 / Drill 256 · Nvim-ready
Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: building applications on top of LLMs as an engineer, not a researcher — prompting,
structured output, retrieval-augmented generation (RAG), tool/function calling, the Model Context Protocol
(MCP), agentic loops, and — first-class — evaluation, cost, latency, and safety. Runnable in Python against
a local or mockable model so no paid key is required to learn the shapes (DD-20). Data plumbing builds on
[`37-data-engineering`](./37-data-engineering.md); it is served over a backend from
[`39-backend-at-scale`](./39-backend-at-scale.md).

## Why this exists · the big idea

- **The problem before the solution**: building on an LLM means building on a component that is
  non-deterministic, occasionally wrong with confidence, and attackable through its own input — the usual
  "it returns the right answer" contract no longer holds.
- **Keep-this-if-you-forget-everything**: treat the model as an unreliable subsystem you engineer around —
  ground it with retrieval, constrain it with structured output and tool schemas, and hold it accountable
  with evals, budgets, and injection guards.
- **Big ideas touched**: `determinism-vs-emergence` (probabilistic output is the defining constraint),
  `correctness-vs-pragmatism` (you manage "good enough" with evals and guardrails, not proofs).

## Prerequisites

- **Prior topics**: [topic 11 Backend Essentials](./11-backend-essentials.md) (serving the app + calling
  an API), [topic 4 Just Enough Python](./04-just-enough-python.md), and
  [topic 15 Software Testing](./15-software-testing.md) (the eval/testing mindset for non-deterministic
  output).
- **Tools & environment**: a macOS/Linux terminal; **Python 3.x** with a pinned CVE-clean model/SDK client;
  a **local or mockable model** + a local vector store for RAG so the examples run without a paid key
  (DD-20); no real API keys committed (secrets rule).
- **Assumed knowledge**: calling an HTTP/API from Python (topic 11); functions + JSON (topic 04); writing a
  test/assertion (topic 15).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified (TIME-SENSITIVE, re-check at authoring): the current **ratified** Model Context
  Protocol version is **2025-11-25**. A **release candidate for 2026-07-28** is public (stateless core,
  Extensions framework, Tasks, MCP Apps, auth hardening) targeting final publication ~2026-07-28 — inside
  the likely authoring window, so re-verify the MCP spec version immediately before authoring this topic.
  (modelcontextprotocol.io/specification/versioning)
- 2026-07-12 — verified: RAG (chunk/embed/retrieve), tool/function calling, structured output, agentic
  loops, eval harnesses, and prompt-injection guardrails are standard/stable framing as of 2026. Keep
  model-SDK API shapes version-unpinned; re-pull the current SDK surface at authoring time.

> DD-35 primary-source pass (2026-07-12). API shapes, event names, and spec definitions traced to primary
> sources (platform.claude.com, developers.openai.com, arXiv, github.com, genai.owasp.org) and fetched/read.
> **Provider doc domains moved** (docs.anthropic.com → platform.claude.com; platform.openai.com →
> developers.openai.com) and **every model ID/price/context-window number is a volatile snapshot** — flagged.

- **LLM API request** — Anthropic Messages API `POST /v1/messages`: required `model`, `messages` (array of
  `{role, content}` with roles `user`/`assistant` only), `max_tokens`; "there is no `"system"` role … use the
  top-level `system` parameter"; response `stop_reason` ∈ `end_turn`/`max_tokens`/`stop_sequence`/`tool_use`.
  OpenAI now recommends the **Responses API** over Chat Completions ("we recommend using the Responses API
  over the older Chat Completions API"), with the caveat "It is not safe to assume that the model's text
  output is present at `output[0].content[0].text`." Sources: [Anthropic Messages API](https://platform.claude.com/docs/en/api/messages), [OpenAI Text generation](https://developers.openai.com/api/docs/guides/text) (fetched, verbatim).
- **Prompt engineering** — Anthropic: few-shot works best with "3–5 examples," wrapped in `<example>` tags;
  "Put longform data at the top … Queries at the end can improve response quality by up to 30%." OpenAI: order
  Identity → Instructions → Examples → Context (context near the **end**) — a genuine, citable cross-provider
  difference, not a contradiction. Sources: [Anthropic prompting](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices), [OpenAI prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering) (fetched, verbatim).
- **Tokens** — dedicated counting endpoint `POST /v1/messages/count_tokens` (free, separate pool); "The same
  input text produces approximately 30% more tokens" on newer-tokenizer models — teach that tokenizers are
  **model-specific and not portable**, treat the 30% as version-bound. OpenAI's tokenizer page 403'd → the
  "≈4 chars/token" rule is `[Needs Verification]`. Source: [Anthropic token counting](https://platform.claude.com/docs/en/build-with-claude/token-counting) (fetched, verbatim).
- **Sampling** — Anthropic `temperature` "Defaults to `1.0` … Ranges from `0.0` to `1.0` … even with
  `temperature` of `0.0`, the results will not be fully deterministic"; `top_p` nucleus sampling "cut it off
  once it reaches a particular probability"; `top_k` samples "from the top K options." OpenAI's range is
  **0–2** (wider than Anthropic's) — a real difference; OpenAI's verbatim parameter text was secondary-sourced
  → `[Needs Verification]`. Source: [Anthropic Messages API](https://platform.claude.com/docs/en/api/messages) (fetched, verbatim).
- **Streaming** — Anthropic SSE order: `message_start` → (`content_block_start`, multiple
  `content_block_delta`, `content_block_stop`) → `message_delta` → `message_stop`; delta sub-types
  `text_delta`/`input_json_delta`/`thinking_delta`. OpenAI Chat Completions streams `chat.completion.chunk`
  objects; the classic `data: [DONE]` terminator is `[Needs Verification]` (conflicting signal). The Responses
  API uses named semantic events (`response.output_text.delta`, `response.completed`) — a three-way teachable
  difference. Sources: [Anthropic streaming](https://platform.claude.com/docs/en/build-with-claude/streaming), [OpenAI streaming](https://developers.openai.com/api/docs/guides/streaming-responses) (fetched, verbatim).
- **Structured output** — OpenAI Structured Outputs: `response_format: {type: "json_schema", json_schema:
{…, strict: true}}` requiring a `required` array listing all keys + `additionalProperties: false`; minimum
  `gpt-4o-mini`/`gpt-4o-2024-08-06`. Anthropic has no JSON-mode flag — the pattern is `tool_choice: {type:
"tool", name: …}` with `strict: true`. Sources: [OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs), [Anthropic tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) (fetched, verbatim).
- **Tool calling** — Anthropic `tools: [{name, description, input_schema}]` (name regex
  `^[a-zA-Z0-9_-]{1,64}$`); response `tool_use` block `{id, name, input}` (input is a **parsed object**);
  reply as `role: "user"` with a `tool_result` block `{tool_use_id, content}` that "must come FIRST in the
  content array"; `tool_choice` modes `auto`/`any`/`tool`/`none`. OpenAI wraps tools in a `function` object
  and returns `arguments` as a **JSON string** requiring parse — a clean compare/contrast. Sources:
  [Anthropic define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools), [Anthropic handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls), [OpenAI function calling](https://developers.openai.com/api/docs/guides/function-calling) (fetched, verbatim).
- **Embeddings** — OpenAI `text-embedding-3-small` (1536 dims) / `-3-large` (3072 dims); "The distance
  between two vectors measures their relatedness"; "Cosine similarity can be computed slightly faster using
  just a dot product" (embeddings pre-normalized to length 1). **Anthropic "does not offer its own embedding
  model"** and recommends Voyage AI — a must-teach fact. Sources: [OpenAI Embeddings](https://developers.openai.com/api/docs/guides/embeddings), [Anthropic Embeddings](https://platform.claude.com/docs/en/build-with-claude/embeddings) (fetched, verbatim).
- **Vector search / HNSW** — pgvector operators `<->` (L2), `<=>` (cosine), `<#>` (inner product); HNSW
  "has better query performance than IVFFlat … but has slower build times and uses more memory." HNSW paper:
  Malkov & Yashunin, arXiv:1603.09320 (2016, rev 2018), "approximate K-nearest neighbor search based on
  navigable small world graphs with controllable hierarchy." Sources: [pgvector](https://github.com/pgvector/pgvector), [arXiv:1603.09320](https://arxiv.org/abs/1603.09320) (fetched, verbatim).
- **RAG** — Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks,"
  arXiv:2005.11401 (NeurIPS 2020): models "combine pre-trained parametric and non-parametric memory," output
  "more specific, diverse and factual." Anthropic Contextual Retrieval (prepend chunk-specific context before
  embedding) cut retrieval-failure ~49% (Contextual Embeddings + BM25). Sources: [arXiv:2005.11401](https://arxiv.org/abs/2005.11401), [Anthropic Contextual Retrieval](https://www.anthropic.com/engineering/contextual-retrieval) (fetched, verbatim).
- **Chunking** — LlamaIndex defaults "chunk size is 1024 … chunk overlap is 20"; "A smaller chunk size means
  the embeddings are more precise … a larger chunk size … can miss fine-grained details." Recursive splitter
  uses `['\n\n','\n',' ','']`. Sources: [LlamaIndex strategies](https://developers.llamaindex.ai/python/framework/optimizing/basic_strategies/basic_strategies/), [Pinecone chunking](https://www.pinecone.io/learn/chunking-strategies/) (fetched, verbatim; specific Pinecone overlap numbers `[Needs Verification]`).
- **Context windows** — every model ID is "a pinned snapshot … not an evergreen pointer"; specific
  context-window / max-output numbers are **volatile** — teach "check the current model page," do not hardcode.
  Source: [Claude models overview](https://platform.claude.com/docs/en/about-claude/models/overview) (fetched; numbers flagged).
- **Multimodal** — Anthropic image block `{type: "image", source: {type: "base64"|"url"|"file"}}`; "Each patch
  is a 28×28-pixel block … an image … costs `⌈width/28⌉ × ⌈height/28⌉` visual tokens." OpenAI `input_image`
  with `detail: low|high|auto` (`low` → 512×512). Sources: [Anthropic vision](https://platform.claude.com/docs/en/build-with-claude/vision), [OpenAI vision](https://developers.openai.com/api/docs/guides/images-vision) (fetched, verbatim).
- **Hallucination** — Ji et al., "Survey of Hallucination in Natural Language Generation," arXiv:2202.03629:
  "deep learning based generation is prone to hallucinate unintended text, which degrades … performance."
  Grounding-via-retrieval = the RAG mechanism above. Source: [arXiv:2202.03629](https://arxiv.org/abs/2202.03629) (fetched, verbatim).
- **Evaluation** — Anthropic eval principles verbatim: "Be task-specific … Automate when possible …
  Prioritize volume over quality"; LLM-as-judge "best practice to use a different model to evaluate than the
  model used to generate." OpenAI Evals: schema data-spec + `testing_criteria` + golden JSONL. Sources:
  [Anthropic develop tests](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests), [OpenAI Evals](https://developers.openai.com/api/docs/guides/evals) (fetched, verbatim).
- **Cost / caching / batching** — Anthropic prompt caching `cache_control: {type: "ephemeral", ttl:
"5m"|"1h"}`; 5-min write = 1.25× input, 1-hr = 2×, read = 0.1× (90% off); `total_input_tokens =
cache_read + cache_creation + input`. Batch APIs give a **50% discount** (both providers). Sources:
  [Anthropic prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching), [Anthropic batch](https://platform.claude.com/docs/en/build-with-claude/batch-processing) (fetched, verbatim; OpenAI caching numbers `[Needs Verification]`).
- **Rate limits / moderation** — Anthropic uses a **token bucket** ("capacity is continuously replenished …
  rather than being reset at fixed intervals"); headers `retry-after`, `anthropic-ratelimit-*`. OpenAI headers
  `x-ratelimit-*` with exponential-backoff-with-jitter guidance. OpenAI moderation `POST /v1/moderations`
  (`omni-moderation-latest`, free) → `flagged`/`categories`/`category_scores` (`[Needs Verification]`, search-sourced). Sources: [Anthropic rate limits](https://platform.claude.com/docs/en/api/rate-limits), [OpenAI rate limits](https://developers.openai.com/api/docs/guides/rate-limits) (fetched, verbatim).
- **Prompt injection** — OWASP LLM01:2025: "A Prompt Injection Vulnerability occurs when user prompts alter
  the LLM's behavior or output in unintended ways" (direct vs indirect via "external sources like websites or
  files"). Anthropic tool docs: "Treat that content as untrusted: an attacker who can influence it may embed
  instructions that try to redirect Claude (indirect prompt injection)." Sources: [OWASP LLM01](https://genai.owasp.org/llmrisk/llm01-prompt-injection/), [Anthropic handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls) (fetched, verbatim; verify OWASP edition year at authoring).
- **Frameworks** — LangChain now frames itself around `create_agent` ("Agent = Model + Harness") — teach its
  non-agentic prompt/LLM primitives deliberately since agents are Topic 55; LlamaIndex "The leading framework
  for building LLM-powered agents over your data"; Vercel AI SDK "a TypeScript toolkit … build AI-powered
  applications and agents" with a unified multi-provider `generateText`/`streamText`. Sources: [LangChain](https://docs.langchain.com/oss/python/langchain/overview), [LlamaIndex](https://developers.llamaindex.ai/python/framework/), [Vercel AI SDK](https://ai-sdk.dev/docs/introduction) (fetched, verbatim).

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject). Each example below cites the co-NN it exercises. -->

- **co-01 · llm-api-request** — the chat/messages request shape: `model`, `messages`/`input`, `max_tokens`,
  and user/assistant/system roles.
- **co-02 · system-prompt** — a system/developer instruction, separate from and prioritized over user
  content.
- **co-03 · prompt-engineering** — instructions, few-shot examples, and instruction/context ordering steer
  the model.
- **co-04 · tokens-tokenization** — text is split into tokens; a tokenizer is model-specific and not
  portable.
- **co-05 · sampling-parameters** — temperature/top_p/top_k trade determinism for diversity (temp 0 is not
  fully deterministic).
- **co-06 · streaming** — server-sent events stream the response as incremental delta events.
- **co-07 · structured-output** — a JSON-schema / strict structured output makes the response machine-parseable.
- **co-08 · tool-calling** — the model calls typed tools via a tool_use → tool_result round-trip with
  argument validation.
- **co-09 · embeddings** — an embedding is a vector whose distance measures relatedness (normalized →
  cosine == dot product).
- **co-10 · vector-store** — a vector store does approximate nearest-neighbor search (e.g. an HNSW index).
- **co-11 · rag-pipeline** — retrieval-augmented generation: retrieve → augment → generate a grounded
  answer.
- **co-12 · chunking** — documents are chunked with overlap; chunk size trades precision for context.
- **co-13 · hybrid-retrieval** — combine dense (vector) + sparse (BM25) retrieval with re-ranking for
  better recall.
- **co-14 · context-window-limits** — each model has a token limit; prompt size must be budgeted against it.
- **co-15 · multimodal-vision** — chat APIs accept image input, priced in visual tokens.
- **co-16 · hallucination-grounding** — LLMs hallucinate unsupported text; retrieval + citations ground the
  output.
- **co-17 · agentic-loop** — a bounded plan → act → observe loop needs a stop condition to avoid runaway
  cost.
- **co-18 · mcp** — the Model Context Protocol standardizes tool/context servers across clients.
- **co-19 · evaluation** — an eval harness scores answers against golden datasets (including LLM-as-judge).
- **co-20 · cost-latency** — per-token pricing and latency are budgeted as first-class engineering
  constraints.
- **co-21 · prompt-caching** — caching a stable prompt prefix cuts repeated input cost and latency.
- **co-22 · batching** — async batch processing trades latency for a large cost discount.
- **co-23 · rate-limits-retries** — providers expose rate-limit headers; clients retry with exponential
  backoff.
- **co-24 · content-moderation** — a moderation endpoint / classifier flags unsafe input or output.
- **co-25 · prompt-injection** — direct and indirect prompt injection treat untrusted tool/retrieved
  content as a threat (OWASP LLM01).
- **co-26 · pii-output-validation** — redact PII and validate/filter model output before using it
  downstream.
- **co-27 · frameworks** — LangChain/LlamaIndex/Vercel AI SDK abstract prompting, retrieval, and provider
  calls.
- **co-28 · provider-abstraction** — swapping providers behind one interface; model IDs are pinned
  snapshots, not evergreen.
- **co-29 · observability-tracing** — tracing spans of an LLM call chain feed an evaluation feedback loop.
- **co-30 · secrets-no-committed-keys** — API keys come from the environment and are never committed.

## Tensions & trade-offs — when NOT to reach for this

- **RAG vs fine-tuning**: RAG grounds answers in retrievable data without retraining, but its accuracy
  depends entirely on retrieval quality — a well-tuned fine-tune can beat a poor retrieval pipeline, and
  RAG adds a whole indexing/retrieval system to operate and keep fresh.
- **Agentic loops vs a single call**: a bounded agentic loop unlocks multi-step tool use, but every extra
  iteration multiplies cost, latency, and the chance the model wanders off-task — reach for a single
  structured-output call first, and add a loop only when one call genuinely can't reach the answer.
- **When NOT to use it**: treating the model's output as ground truth. An LLM-powered feature that skips
  evals, budgets, and injection guards is the failure mode this topic exists to prevent — the
  accountability of evaluation, cost/latency limits, and prompt-injection defenses is what makes
  probabilistic output usable in production, not an optional hardening pass.

## Lineage — why it beat the alternative

- Before RAG (Lewis et al. 2020) and tool/function calling matured, LLM apps either fine-tuned a model
  per task — slow, expensive, and stale the moment the underlying facts changed — or stuffed everything
  into the prompt, bounded by the context window. Grounding via retrieval plus structured tool calls won
  because it keeps the model's knowledge current without retraining and lets it act on live systems,
  pushing the correctness burden onto retrieval quality, evals, and guardrails rather than the model's
  frozen weights — which is exactly why [`39-backend-at-scale`](./39-backend-at-scale.md) (serving the
  app) and this topic's eval/cost/injection disciplines matter as much as the model call itself.

## Worked examples

Colocated under `creating-ai-powered-apps/learning/code/`; each is typed, `pyright`-clean Python runnable
against a local/mockable model so no paid key is required (DD-20/DD-30/DD-34/DD-39). Contiguous `ex-01..ex-80`.
Every example cites the `co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · messages-request** — a chat/messages request (`model`, `messages`, `max_tokens`) — verify a
  response is returned. (co-01)
- **ex-02 · roles-user-assistant** — a user/assistant multi-turn conversation — verify roles alternate.
  (co-01)
- **ex-03 · system-prompt** — a system/developer instruction — verify it shapes the answer. (co-02)
- **ex-04 · few-shot** — 3–5 few-shot examples in the prompt — verify the pattern is followed. (co-03)
- **ex-05 · instruction-ordering** — annotate instruction/context/input ordering — verify the placement.
  (co-03)
- **ex-06 · xml-structured-prompt** — tag content blocks (`<context>`/`<input>`) — verify reduced
  misinterpretation. (co-03)
- **ex-07 · token-count** — count tokens for an input via the count endpoint — verify the count. (co-04)
- **ex-08 · tokenizer-model-specific** — annotate that a tokenizer differs per model (~30% shift) — verify
  the non-portability. (co-04)
- **ex-09 · context-window-check** — annotate reading the model's context-window limit — verify the
  budgeting step. (co-14)
- **ex-10 · temperature** — vary temperature for determinism vs creativity — verify output variance. (co-05)
- **ex-11 · top-p-nucleus** — annotate nucleus sampling `top_p` — verify the cumulative-probability cutoff.
  (co-05)
- **ex-12 · temperature-zero** — annotate that temp 0 is not fully deterministic — verify the caveat.
  (co-05)
- **ex-13 · stop-sequences** — a stop sequence terminating output — verify the response stops there. (co-05)
- **ex-14 · json-schema-output** — a JSON-schema structured output (strict) — verify it validates. (co-07)
- **ex-15 · structured-required-fields** — annotate `required` + `additionalProperties:false` for strict —
  verify the schema constraints. (co-07)
- **ex-16 · tool-for-structured** — annotate forcing a tool to guarantee a structured shape — verify the
  forced shape. (co-07)
- **ex-17 · parse-validate-output** — parse + validate model JSON with a typed model — verify invalid JSON
  is rejected. (co-07)
- **ex-18 · streaming-deltas** — stream response deltas (SSE) — verify incremental output. (co-06)
- **ex-19 · streaming-events** — annotate `message_start`/`content_block_delta`/`message_stop` events —
  verify the event order. (co-06)
- **ex-20 · embedding-vector** — get an embedding vector for text — verify the dimension. (co-09)
- **ex-21 · cosine-similarity** — cosine similarity between two embeddings — verify similar texts score
  higher. (co-09)
- **ex-22 · normalized-dot-product** — annotate normalized embeddings → dot product == cosine — verify the
  equivalence. (co-09)
- **ex-23 · embedding-provider-note** — annotate that Anthropic has no embedding model (uses Voyage) —
  verify the fact. (co-09)
- **ex-24 · chunk-fixed** — fixed-size chunking with overlap — verify chunk boundaries + overlap. (co-12)
- **ex-25 · chunk-recursive** — recursive separator-based chunking — verify it splits on natural
  boundaries. (co-12)
- **ex-26 · chunk-size-tradeoff** — annotate small vs large chunk tradeoff — verify the precision/context
  balance. (co-12)
- **ex-27 · vector-store-index** — index chunks in a vector store (HNSW) — verify the index is queryable.
  (co-10)

### Intermediate

- **ex-28 · nearest-neighbor-search** — top-k nearest-neighbor retrieval — verify the closest chunks return.
  (co-10)
- **ex-29 · hnsw-index** — annotate an HNSW index (`m`/`ef_construction`) — verify the speed/recall
  tradeoff. (co-10)
- **ex-30 · rag-retrieve-augment-generate** — a minimal RAG pipeline — verify the answer uses retrieved
  context. (co-11)
- **ex-31 · rag-citations** — a grounded answer citing retrieved chunks — verify each claim cites a chunk.
  (co-11)
- **ex-32 · rag-grounding** — annotate that grounding reduces hallucination — verify the grounding link.
  (co-16)
- **ex-33 · hallucination-annotate** — annotate why LLMs hallucinate — verify the failure mode. (co-16)
- **ex-34 · hybrid-dense-sparse** — combine vector + BM25 retrieval — verify both contribute results.
  (co-13)
- **ex-35 · reranking** — re-rank retrieved candidates — verify the top result improves. (co-13)
- **ex-36 · contextual-retrieval** — annotate the prepend-context technique — verify the recall gain.
  (co-13)
- **ex-37 · tool-definition** — define a typed tool (`name`/`description`/`input_schema`) — verify the tool
  is offered. (co-08)
- **ex-38 · tool-use-round-trip** — a `tool_use` → `tool_result` round trip — verify the result is
  incorporated. (co-08)
- **ex-39 · tool-argument-validation** — validate tool arguments before executing — verify invalid args are
  rejected. (co-08)
- **ex-40 · tool-choice-forced** — force a specific tool with `tool_choice` — verify that tool is called.
  (co-08)
- **ex-41 · openai-vs-anthropic-tools** — annotate flat vs function-wrapper shape + string-vs-object args —
  verify the difference. (co-08)
- **ex-42 · mcp-server** — annotate an MCP server exposing tools/context — verify the server contract.
  (co-18)
- **ex-43 · mcp-standard** — annotate MCP as the open tool/context standard — verify its cross-client role.
  (co-18)
- **ex-44 · agentic-loop-bounded** — a bounded plan → act → observe loop — verify it iterates on tool
  results. (co-17)
- **ex-45 · loop-stop-condition** — a stop condition + max iterations — verify the loop terminates. (co-17)
- **ex-46 · loop-budget-cap** — annotate a budget cap avoiding infinite loops — verify the cap halts a
  runaway. (co-17)
- **ex-47 · vision-image-input** — an image input to a chat call — verify the model describes the image.
  (co-15)
- **ex-48 · vision-token-cost** — annotate image patch / visual-token cost — verify the `⌈w/28⌉×⌈h/28⌉`
  math. (co-15)
- **ex-49 · eval-golden-set** — a golden-set eval asserting expected outputs — verify pass/fail per case.
  (co-19)
- **ex-50 · eval-llm-as-judge** — annotate LLM-as-judge with a different model — verify the judge-model
  separation. (co-19)
- **ex-51 · eval-schema-assert** — an eval asserting the output schema — verify a malformed output fails.
  (co-19)
- **ex-52 · cost-per-token** — compute cost from token usage — verify the price math. (co-20)
- **ex-53 · latency-budget** — assert a latency budget — verify a slow call breaches it. (co-20)
- **ex-54 · prompt-cache** — annotate caching a stable prefix (0.1× read) — verify the discount. (co-21)
- **ex-55 · cache-usage-math** — annotate `cache_read + cache_creation + input` token math — verify the
  sum. (co-21)

### Advanced

- **ex-56 · batch-processing** — annotate async batch at a 50% discount — verify the cost tradeoff. (co-22)
- **ex-57 · rate-limit-headers** — read rate-limit headers — verify remaining quota is parsed. (co-23)
- **ex-58 · exponential-backoff** — a retry with exponential backoff + jitter — verify it backs off on 429.
  (co-23)
- **ex-59 · token-bucket** — annotate token-bucket rate limiting — verify continuous replenishment. (co-23)
- **ex-60 · moderation-endpoint** — a content-moderation check — verify unsafe input is flagged. (co-24)
- **ex-61 · moderation-categories** — annotate moderation categories + scores — verify per-category output.
  (co-24)
- **ex-62 · prompt-injection-direct** — annotate a direct prompt injection — verify the attack shape.
  (co-25)
- **ex-63 · prompt-injection-indirect** — annotate indirect injection via retrieved content — verify the
  untrusted-source vector. (co-25)
- **ex-64 · injection-guard** — a guard treating tool/retrieved content as untrusted — verify instructions
  in data are ignored. (co-25)
- **ex-65 · injection-corpus-test** — a test that an injected instruction in the corpus is not obeyed —
  verify the loop resists it. (co-25)
- **ex-66 · owasp-llm01** — annotate OWASP LLM01 Prompt Injection — verify the direct/indirect distinction.
  (co-25)
- **ex-67 · pii-redaction** — redact PII before sending/logging — verify PII is removed. (co-26)
- **ex-68 · output-validation** — validate/filter model output before use — verify a bad output is
  rejected. (co-26)
- **ex-69 · output-encoding-downstream** — annotate encoding model output for downstream safety — verify no
  raw injection. (co-26)
- **ex-70 · langchain-abstraction** — annotate a LangChain prompt/LLM primitive — verify the composition.
  (co-27)
- **ex-71 · llamaindex-abstraction** — annotate LlamaIndex over-your-data framing — verify the
  index/query-engine role. (co-27)
- **ex-72 · vercel-ai-sdk** — annotate the Vercel AI SDK unified `generateText` API — verify the
  provider-agnostic call. (co-27)
- **ex-73 · provider-swap** — swap providers behind one interface — verify the app runs on either. (co-28)
- **ex-74 · model-id-pinned** — annotate that model IDs are pinned snapshots, not evergreen — verify the
  versioning caveat. (co-28)
- **ex-75 · tracing-spans** — annotate tracing spans of an LLM call chain — verify each call is a span.
  (co-29)
- **ex-76 · observability-eval-loop** — annotate the trace → eval feedback loop — verify traces feed evals.
  (co-29)
- **ex-77 · api-key-env** — load an API key from an env var, never committed — verify no key in source.
  (co-30)
- **ex-78 · no-key-required-mock** — a mockable model so no paid key is needed — verify the example runs
  offline. (co-30)
- **ex-79 · responses-vs-chat** — annotate the Responses API vs Chat Completions output shape — verify the
  `output`-array difference. (co-01)
- **ex-80 · aiapp-capstone** — a grounded QA app: RAG + cited output + tool call + bounded agentic loop +
  eval + cost/latency budget + injection guard — verify grounded cited answers, validated tool args, a
  terminating injection-resistant loop, and reproducible eval scores. (co-08, co-11, co-17, co-19, co-20,
  co-25)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: build a grounded question-answering app over a local corpus — RAG (chunk/embed/retrieve),
  structured/cited output, a tool-calling step for a live lookup, a bounded agentic loop with guardrails —
  and wrap it in an evaluation harness that scores answer quality, plus explicit cost/latency budgeting and
  a prompt-injection guard, all runnable against a local/mockable model.
- **Concepts exercised**: [ ] structured/validated output (co-07) [ ] a RAG pipeline with citations (co-11,
  co-16) [ ] tool/function calling with argument validation (co-08) [ ] a bounded agentic loop with a stop
  condition (co-17) [ ] an eval harness scoring quality (co-19) [ ] a cost/latency budget + an injection guard
  (co-20, co-25).
- **Ordered steps**:
  1. `.../learning/capstone/code/rag.py` — chunk + embed a local corpus + retrieve top-k + generate a cited
     answer. Verify answers cite retrieved chunks and a schema-validated shape.
  2. Add a tool-calling step (a typed lookup) with argument validation. Verify invalid arguments are
     rejected and the tool result is incorporated.
  3. Wrap in a bounded agentic loop with a stop condition + a prompt-injection guard. Verify the loop
     terminates and an injected instruction in the corpus is not obeyed.
  4. `eval.py` — a golden-set eval scoring answer quality + a cost/latency budget assertion. Verify the eval
     runs, reports scores, and flags a budget breach.
- **Acceptance criteria**: RAG answers are grounded + cited; tool arguments are validated; the agent loop is
  bounded and injection-resistant; the eval harness produces reproducible scores within the stated
  cost/latency budget; no API key is committed.
- **Done bar**: runnable end-to-end (local/mockable model) + web-verified.

## Read more

**Books**

- **Designing Machine Learning Systems** — Chip Huyen (2022). Widely adopted, practitioner-oriented reference for building production ML/AI systems end to end.

**Papers & articles**

- **Attention Is All You Need** — Ashish Vaswani et al. (2017). The paper introducing the Transformer architecture underlying virtually all modern LLMs. <https://arxiv.org/abs/1706.03762>
- **Language Models are Few-Shot Learners** — Tom B. Brown et al. (2020). The GPT-3 paper that established the modern prompting/few-shot paradigm for LLM applications. <https://arxiv.org/abs/2005.14165>
- **Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks** — Patrick Lewis et al. (2020). The paper that named and formalized RAG, now the standard pattern for grounding LLM apps in external data. <https://arxiv.org/abs/2005.11401>
- **OpenAI Prompt Engineering Guide** — OpenAI (ongoing). Widely used, vendor-authoritative practical reference for prompt design and evaluation. <https://platform.openai.com/docs/guides/prompt-engineering>

---

← Previous: [55 · CI/CD & Release Engineering](./55-cicd-and-release-engineering.md) · Next: [57 · Agentic AI](./57-agentic-ai.md) →

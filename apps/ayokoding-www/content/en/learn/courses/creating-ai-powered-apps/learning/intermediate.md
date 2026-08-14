---
title: "Intermediate Examples"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 20
---

Examples 28–55 compose offline retrieval, tool, bounded-loop, multimodal, evaluation, cost, and cache
mechanisms. Every artifact is an annotated local Python assertion with no network or credential dependency.

### Example 28: Nearest-Neighbor Search

**Brief explanation.** Top-k retrieval ranks local chunks by similarity. It supplies evidence before generation. **Diagram.** `query → scores → top-k chunks`. **Annotated code.** [example.py](learning/code/ex-28-nearest-neighbor-search/example.py). **Key takeaway.** Retrieve the closest chunks deliberately. **Why it matters.** Local ranking makes retrieval behavior testable before model output is involved.

### Example 29: HNSW Index

**Brief explanation.** HNSW exposes index construction and search tradeoffs. Tune recall against latency. **Diagram.** `graph layers → candidate search`. **Annotated code.** [example.py](learning/code/ex-29-hnsw-index/example.py). **Key takeaway.** Speed and recall are a deliberate tradeoff. **Why it matters.** Index parameters change product quality and cost.

### Example 30: RAG Retrieve Augment Generate

**Brief explanation.** RAG retrieves context before forming an answer. The answer must use that supplied evidence. **Diagram.** `query → retrieve → augment → generate`. **Annotated code.** [example.py](learning/code/ex-30-rag-retrieve-augment-generate/example.py). **Key takeaway.** Retrieve before generating. **Why it matters.** Grounded context makes answers auditable.

### Example 31: RAG Citations

**Brief explanation.** A grounded answer attaches source identifiers to claims. Citations connect output to retrieved chunks. **Diagram.** `claim → chunk ID`. **Annotated code.** [example.py](learning/code/ex-31-rag-citations/example.py). **Key takeaway.** Evidence needs an address. **Why it matters.** Users can inspect support instead of trusting a fluent answer blindly.

### Example 32: RAG Grounding

**Brief explanation.** Grounding constrains a response to supplied evidence. It reduces unsupported invention. **Diagram.** `retrieved context → bounded claim`. **Annotated code.** [example.py](learning/code/ex-32-rag-grounding/example.py). **Key takeaway.** Context is a guardrail, not proof by itself. **Why it matters.** Teams can test whether claims trace to known material.

### Example 33: Hallucination Annotate

**Brief explanation.** Models can produce plausible unsupported claims. Annotate the failure mode before designing mitigation. **Diagram.** `missing evidence → plausible fabrication`. **Annotated code.** [example.py](learning/code/ex-33-hallucination-annotate/example.py). **Key takeaway.** Fluency is not evidence. **Why it matters.** This distinction prevents unsafe confidence in generated output.

### Example 34: Hybrid Dense Sparse

**Brief explanation.** Hybrid retrieval combines semantic and lexical signals. Each can recover evidence the other misses. **Diagram.** `dense + BM25 → merge`. **Annotated code.** [example.py](learning/code/ex-34-hybrid-dense-sparse/example.py). **Key takeaway.** Combine complementary signals. **Why it matters.** Hybrid ranking improves recall across vocabulary mismatch.

### Example 35: Reranking

**Brief explanation.** Reranking refines an initial candidate set with a more precise scorer. It spends expensive work only on plausible results. **Diagram.** `candidates → reranker → best`. **Annotated code.** [example.py](learning/code/ex-35-reranking/example.py). **Key takeaway.** Retrieve broadly, rank precisely. **Why it matters.** Better top results improve downstream answer quality.

### Example 36: Contextual Retrieval

**Brief explanation.** Contextual retrieval prepends chunk context before indexing. The added framing makes isolated passages easier to recover. **Diagram.** `context + chunk → embedding`. **Annotated code.** [example.py](learning/code/ex-36-contextual-retrieval/example.py). **Key takeaway.** Index chunks with their missing context restored. **Why it matters.** Recall improves when snippets are meaningful alone.

### Example 37: Tool Definition

**Brief explanation.** A typed tool declares name, description, and input schema. The model is offered a constrained action surface. **Diagram.** `schema → offered tool`. **Annotated code.** [example.py](learning/code/ex-37-tool-definition/example.py). **Key takeaway.** Tool contracts are data. **Why it matters.** Schemas prevent ambiguous execution.

### Example 38: Tool Use Round Trip

**Brief explanation.** A tool call becomes a tool result before the model continues. The result is new conversation evidence. **Diagram.** `tool_use → execute → tool_result`. **Annotated code.** [example.py](learning/code/ex-38-tool-use-round-trip/example.py). **Key takeaway.** Tools close a typed feedback loop. **Why it matters.** The model can act on observed outcomes rather than guesses.

### Example 39: Tool Argument Validation

**Brief explanation.** Validate tool arguments before execution. Invalid input is rejected at the capability boundary. **Diagram.** `arguments → schema check → execute | reject`. **Annotated code.** [example.py](learning/code/ex-39-tool-argument-validation/example.py). **Key takeaway.** Never execute unvalidated model arguments. **Why it matters.** Validation limits unsafe side effects.

### Example 40: Tool Choice Forced

**Brief explanation.** A caller can force one named tool when the workflow requires it. This removes model discretion at a critical step. **Diagram.** `tool_choice → required tool`. **Annotated code.** [example.py](learning/code/ex-40-tool-choice-forced/example.py). **Key takeaway.** Constrain choice when policy requires it. **Why it matters.** Determinism matters for guarded operations.

### Example 41: OpenAI Vs Anthropic Tools

**Brief explanation.** Providers differ in tool wrapper and argument shapes. Normalize those differences at an adapter boundary. **Diagram.** `provider shape → common tool contract`. **Annotated code.** [example.py](learning/code/ex-41-openai-vs-anthropic-tools/example.py). **Key takeaway.** Provider syntax is not your domain contract. **Why it matters.** Adapters reduce vendor-specific coupling.

### Example 42: MCP Server

**Brief explanation.** An MCP server exposes tools and context to a client. The server contract separates capability hosting from model orchestration. **Diagram.** `client ↔ MCP server ↔ tools`. **Annotated code.** [example.py](learning/code/ex-42-mcp-server/example.py). **Key takeaway.** Tools can live behind a standard server boundary. **Why it matters.** Shared capabilities remain reusable across clients.

### Example 43: MCP Standard

**Brief explanation.** MCP is an open protocol for tool and context integration. Its cross-client role avoids bespoke per-model bridges. **Diagram.** `many clients ↔ one standard`. **Annotated code.** [example.py](learning/code/ex-43-mcp-standard/example.py). **Key takeaway.** Standard contracts outlive client implementations. **Why it matters.** Interoperability lowers integration maintenance.

### Example 44: Agentic Loop Bounded

**Brief explanation.** A plan-act-observe loop feeds tool results into the next step. Its loop is explicit and bounded. **Diagram.** `plan → act → observe → plan`. **Annotated code.** [example.py](learning/code/ex-44-agentic-loop-bounded/example.py). **Key takeaway.** Tool results drive the next action. **Why it matters.** Explicit loops are inspectable and stoppable.

### Example 45: Loop Stop Condition

**Brief explanation.** A loop stops on success or a maximum iteration count. Both conditions are part of the product contract. **Diagram.** `iteration → success | limit`. **Annotated code.** [example.py](learning/code/ex-45-loop-stop-condition/example.py). **Key takeaway.** Every agent loop needs an exit rule. **Why it matters.** Termination prevents runaway cost.

### Example 46: Loop Budget Cap

**Brief explanation.** A budget cap stops a loop even if it has remaining iterations. It bounds resource consumption independently of behavior. **Diagram.** `cost → cap → halt`. **Annotated code.** [example.py](learning/code/ex-46-loop-budget-cap/example.py). **Key takeaway.** Budget is a first-class stop condition. **Why it matters.** Cost safety survives unexpected loop behavior.

### Example 47: Vision Image Input

**Brief explanation.** A vision request includes an image alongside text. The model can describe visual evidence without a network fixture. **Diagram.** `image + prompt → description`. **Annotated code.** [example.py](learning/code/ex-47-vision-image-input/example.py). **Key takeaway.** Images are structured model input. **Why it matters.** Visual tasks need explicit input handling.

### Example 48: Vision Token Cost

**Brief explanation.** Image dimensions map to visual-token cost through patches. Estimate before submitting expensive images. **Diagram.** `width/28 × height/28 → tokens`. **Annotated code.** [example.py](learning/code/ex-48-vision-token-cost/example.py). **Key takeaway.** Visual input has measurable budget impact. **Why it matters.** Size-aware handling protects latency and cost.

### Example 49: Eval Golden Set

**Brief explanation.** A golden set compares expected and actual output per case. It provides a small deterministic regression signal. **Diagram.** `case → expected vs actual`. **Annotated code.** [example.py](learning/code/ex-49-eval-golden-set/example.py). **Key takeaway.** Known cases make regressions visible. **Why it matters.** Product changes need repeatable evaluation.

### Example 50: Eval LLM As Judge

**Brief explanation.** An LLM judge should be separate from the evaluated model. Separation reduces self-grading bias. **Diagram.** `candidate output → distinct judge`. **Annotated code.** [example.py](learning/code/ex-50-eval-llm-as-judge/example.py). **Key takeaway.** Judge and subject have different roles. **Why it matters.** Evaluation design affects trust in results.

### Example 51: Eval Schema Assert

**Brief explanation.** A schema assertion rejects malformed structured output. It checks a contract before semantic scoring. **Diagram.** `output → schema → pass | fail`. **Annotated code.** [example.py](learning/code/ex-51-eval-schema-assert/example.py). **Key takeaway.** Structure is testable behavior. **Why it matters.** Invalid output should fail clearly.

### Example 52: Cost Per Token

**Brief explanation.** Token usage multiplied by price gives explicit cost. Track input and output separately when rates differ. **Diagram.** `tokens × rate → cost`. **Annotated code.** [example.py](learning/code/ex-52-cost-per-token/example.py). **Key takeaway.** Cost is measurable usage, not guesswork. **Why it matters.** Budgets require reliable arithmetic.

### Example 53: Latency Budget

**Brief explanation.** A latency assertion compares observed duration to a defined limit. Slow calls become a testable breach. **Diagram.** `elapsed → budget check`. **Annotated code.** [example.py](learning/code/ex-53-latency-budget/example.py). **Key takeaway.** Performance needs an explicit threshold. **Why it matters.** Budgets make user-facing responsiveness enforceable.

### Example 54: Prompt Cache

**Brief explanation.** A stable prompt prefix can be cached at a discounted read price. Mark stable and changing sections separately. **Diagram.** `stable prefix → cache read discount`. **Annotated code.** [example.py](learning/code/ex-54-prompt-cache/example.py). **Key takeaway.** Prompt structure affects cost. **Why it matters.** Reuse lowers repeated-input spend.

### Example 55: Cache Usage Math

**Brief explanation.** Cache-read, cache-creation, and ordinary input tokens are distinct accounting values. Sum them explicitly before pricing. **Diagram.** `read + creation + input → total`. **Annotated code.** [example.py](learning/code/ex-55-cache-usage-math/example.py). **Key takeaway.** Cached usage needs separate measurement. **Why it matters.** Accurate accounting prevents misleading optimization claims.

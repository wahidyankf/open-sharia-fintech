---
title: "Beginner Examples"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 10
---

Examples 1–27 establish a deterministic provider boundary, prompting, structured output, streaming,
embeddings, chunking, and local vector retrieval. Each entry links to a colocated offline Python artifact.

## Example index

- [Example 1: Messages Request](#example-1-messages-request)
- [Example 2: Roles User Assistant](#example-2-roles-user-assistant)
- [Example 3: System Prompt](#example-3-system-prompt)
- [Example 4: Few Shot](#example-4-few-shot)
- [Example 5: Instruction Ordering](#example-5-instruction-ordering)
- [Example 6: XML Structured Prompt](#example-6-xml-structured-prompt)
- [Example 7: Token Count](#example-7-token-count)
- [Example 8: Tokenizer Model Specific](#example-8-tokenizer-model-specific)
- [Example 9: Context Window Check](#example-9-context-window-check)
- [Example 10: Temperature](#example-10-temperature)
- [Example 11: Top P Nucleus](#example-11-top-p-nucleus)
- [Example 12: Temperature Zero](#example-12-temperature-zero)
- [Example 13: Stop Sequences](#example-13-stop-sequences)
- [Example 14: JSON Schema Output](#example-14-json-schema-output)
- [Example 15: Structured Required Fields](#example-15-structured-required-fields)
- [Example 16: Tool for Structured Output](#example-16-tool-for-structured-output)
- [Example 17: Parse Validate Output](#example-17-parse-validate-output)
- [Example 18: Streaming Deltas](#example-18-streaming-deltas)
- [Example 19: Streaming Events](#example-19-streaming-events)
- [Example 20: Embedding Vector](#example-20-embedding-vector)
- [Example 21: Cosine Similarity](#example-21-cosine-similarity)
- [Example 22: Normalized Dot Product](#example-22-normalized-dot-product)
- [Example 23: Embedding Provider Note](#example-23-embedding-provider-note)
- [Example 24: Fixed Chunking](#example-24-fixed-chunking)
- [Example 25: Recursive Chunking](#example-25-recursive-chunking)
- [Example 26: Chunk Size Tradeoff](#example-26-chunk-size-tradeoff)
- [Example 27: Vector Store Index](#example-27-vector-store-index)

### Example 1: Messages Request

_ex-01 · exercises co-01_

A request boundary owns the model identifier, messages, and output limit; application code should not
scatter these fields through handlers. Use a mock at this boundary so request construction is testable offline.

**`learning/code/ex-01-messages-request/example.py`**

```python
from dataclasses import dataclass  # => typed request data

@dataclass(frozen=True)  # => immutable request prevents accidental mutation
class Message:
    role: str  # => protocol role
    content: str  # => message text

reply = Message("assistant", "mock response")  # => offline model result
assert reply.role == "assistant"  # => verifies a response shape
print("PASS: messages-request")  # => Output: PASS: messages-request
```

**Run**: `python3 learning/code/ex-01-messages-request/example.py`

**Key takeaway**: Treat a model call as a typed API request and make its boundary mockable.

**Why it matters**: A typed boundary prevents provider-specific payload fields from leaking across an
application. The mock keeps unit tests deterministic and credential-free while preserving the same contract
used by a real client. This is the foundation for validating every later model response.

### Example 2: Roles User Assistant

_ex-02 · exercises co-01_

Alternating `user` and `assistant` roles preserves conversation history without treating prior output as
developer instruction. Use explicit roles whenever a conversation has more than one turn.

**Annotated code**: [`example.py`](learning/code/ex-02-roles-user-assistant/example.py)

**Run**: `python3 learning/code/ex-02-roles-user-assistant/example.py`

**Key takeaway**: Conversation roles are typed protocol data, not display labels.

**Why it matters**: A role mistake changes the model contract and can weaken instruction boundaries. A local
fixture makes the ordering rule regression-testable without a provider account.

### Example 3: System Prompt

_ex-03 · exercises co-02_

A system or developer instruction establishes application policy separately from user content. Keep it stable
and test the behavior it requires with a mock response.

**Annotated code**: [`example.py`](learning/code/ex-03-system-prompt/example.py)

**Run**: `python3 learning/code/ex-03-system-prompt/example.py`

**Key takeaway**: Put durable product policy above untrusted user input.

**Why it matters**: Mixing policy into a user string makes it easier to override accidentally. A separate
instruction also creates a stable prefix that can be cached and reviewed.

### Example 4: Few Shot

_ex-04 · exercises co-03_

Few-shot examples demonstrate an input/output pattern without changing model weights. Keep the examples small
and directly representative of the format a downstream parser needs.

**Annotated code**: [`example.py`](learning/code/ex-04-few-shot/example.py)

**Run**: `python3 learning/code/ex-04-few-shot/example.py`

**Key takeaway**: Examples constrain format more reliably than vague prose alone.

**Why it matters**: A small fixture catches an output-format regression before it reaches a parser. It also
keeps prompt behavior testable when a real provider is unavailable.

### Example 5: Instruction Ordering

**Brief explanation.** Put instructions before context and user input so each role is legible. **Diagram.** `instruction → context → input`. **Annotated code.** [`example.py`](learning/code/ex-05-instruction-ordering/example.py). **Key takeaway.** Ordering is a safety boundary. **Why it matters.** Clear sections reduce accidental instruction conflict.

### Example 6: XML Structured Prompt

**Brief explanation.** XML tags separate untrusted context from the task. **Diagram.** `task + <context>`. **Annotated code.** [`example.py`](learning/code/ex-06-xml-structured-prompt/example.py). **Key takeaway.** Label data by role. **Why it matters.** Structure makes prompt boundaries reviewable.

### Example 7: Token Count

**Brief explanation.** Count input before sending it. **Diagram.** `text → tokens → budget`. **Annotated code.** [`example.py`](learning/code/ex-07-token-count/example.py). **Key takeaway.** Budget tokens early. **Why it matters.** Requests must fit cost and context limits.

### Example 8: Tokenizer Model Specific

**Brief explanation.** Tokenization varies by model. **Diagram.** `text → model tokenizer → count`. **Annotated code.** [`example.py`](learning/code/ex-08-tokenizer-model-specific/example.py). **Key takeaway.** Counts are model-specific. **Why it matters.** Portable character estimates are unsafe for budgets.

### Example 9: Context Window Check

**Brief explanation.** Reserve output tokens before adding context. **Diagram.** `input + output reserve ≤ window`. **Annotated code.** [`example.py`](learning/code/ex-09-context-window-check/example.py). **Key takeaway.** Leave response capacity. **Why it matters.** Oversized prompts fail or truncate.

### Example 10: Temperature

**Brief explanation.** Temperature adjusts sampling diversity. **Diagram.** `temperature → candidate spread`. **Annotated code.** [`example.py`](learning/code/ex-10-temperature/example.py). **Key takeaway.** Diversity trades against repeatability. **Why it matters.** Product behavior needs an intentional sampling setting.

### Example 11: Top P Nucleus

**Brief explanation.** Top-p limits candidates by probability mass. **Diagram.** `distribution → nucleus`. **Annotated code.** [`example.py`](learning/code/ex-11-top-p-nucleus/example.py). **Key takeaway.** Nucleus sampling narrows choices. **Why it matters.** It is a separate control from temperature.

### Example 12: Temperature Zero

**Brief explanation.** Zero temperature reduces sampling randomness but cannot promise cross-provider determinism. **Diagram.** `same prompt → provider-dependent output`. **Annotated code.** [`example.py`](learning/code/ex-12-temperature-zero/example.py). **Key takeaway.** Zero is not a universal guarantee. **Why it matters.** Tests should assert contracts, not prose identity.

### Example 13: Stop Sequences

**Brief explanation.** Stop sequences bound generation at a known delimiter. **Diagram.** `generation → stop token → finish`. **Annotated code.** [`example.py`](learning/code/ex-13-stop-sequences/example.py). **Key takeaway.** Stops constrain output. **Why it matters.** Bounded completions protect parsers and cost.

### Example 14: JSON Schema Output

**Brief explanation.** JSON schema makes machine-consumed output explicit. **Diagram.** `model JSON → schema`. **Annotated code.** [`example.py`](learning/code/ex-14-json-schema-output/example.py). **Key takeaway.** Validate structured output. **Why it matters.** Consumers need a contract, not plausible JSON.

### Example 15: Structured Required Fields

**Brief explanation.** Required keys and forbidden extras make a schema strict. **Diagram.** `object → required/extra check`. **Annotated code.** [`example.py`](learning/code/ex-15-structured-required-fields/example.py). **Key takeaway.** Strict fields prevent drift. **Why it matters.** Downstream code can trust validated shape.

### Example 16: Tool For Structured Output

**Brief explanation.** A forced tool can encode a typed response shape. **Diagram.** `tool schema → structured result`. **Annotated code.** [`example.py`](learning/code/ex-16-tool-for-structured/example.py). **Key takeaway.** Tools can enforce format. **Why it matters.** Typed calls reduce parser ambiguity.

### Example 17: Parse Validate Output

**Brief explanation.** Parse model JSON then validate it. **Diagram.** `bytes → parse → validate`. **Annotated code.** [`example.py`](learning/code/ex-17-parse-validate-output/example.py). **Key takeaway.** Reject malformed output. **Why it matters.** Failures remain contained at the boundary.

### Example 18: Streaming Deltas

**Brief explanation.** Streaming renders ordered incremental deltas. **Diagram.** `delta → buffer → UI`. **Annotated code.** [`example.py`](learning/code/ex-18-streaming-deltas/example.py). **Key takeaway.** Preserve event order. **Why it matters.** Users see progress without corrupting text.

### Example 19: Streaming Events

**Brief explanation.** Stream lifecycle events are a protocol. **Diagram.** `start → delta → complete`. **Annotated code.** [`example.py`](learning/code/ex-19-streaming-events/example.py). **Key takeaway.** Handle lifecycle explicitly. **Why it matters.** Cleanup and error states need reliable events.

### Example 20: Embedding Vector

**Brief explanation.** An embedding is a fixed-dimension numeric vector. **Diagram.** `text → vector`. **Annotated code.** [`example.py`](learning/code/ex-20-embedding-vector/example.py). **Key takeaway.** Store dimensions explicitly. **Why it matters.** Retrieval depends on compatible vector shapes.

### Example 21: Cosine Similarity

**Brief explanation.** Cosine compares vector direction. **Diagram.** `vectors → cosine score`. **Annotated code.** [`example.py`](learning/code/ex-21-cosine-similarity/example.py). **Key takeaway.** Higher score means closer direction. **Why it matters.** Ranking needs a measurable similarity rule.

### Example 22: Normalized Dot Product

**Brief explanation.** Unit-normalized vectors make dot product equal cosine. **Diagram.** `normalize → dot`. **Annotated code.** [`example.py`](learning/code/ex-22-normalized-dot-product/example.py). **Key takeaway.** Normalize before comparing. **Why it matters.** One score rule simplifies local retrieval.

### Example 23: Embedding Provider Note

**Brief explanation.** Embedding providers vary in dimension and quality. **Diagram.** `provider → vector contract`. **Annotated code.** [`example.py`](learning/code/ex-23-embedding-provider-note/example.py). **Key takeaway.** Choose deliberately. **Why it matters.** A provider change requires index compatibility planning.

### Example 24: Fixed Chunking

**Brief explanation.** Fixed chunks use a size and overlap. **Diagram.** `text → overlapping windows`. **Annotated code.** [`example.py`](learning/code/ex-24-chunk-fixed/example.py). **Key takeaway.** Overlap protects boundary facts. **Why it matters.** Retrieval loses less context at cuts.

### Example 25: Recursive Chunking

**Brief explanation.** Recursive chunking prefers natural separators. **Diagram.** `paragraph → sentence → character`. **Annotated code.** [`example.py`](learning/code/ex-25-chunk-recursive/example.py). **Key takeaway.** Preserve meaning before cutting. **Why it matters.** Natural chunks improve retrieval quality.

### Example 26: Chunk Size Tradeoff

**Brief explanation.** Chunk size balances precision and retained context. **Diagram.** `small precision ↔ large context`. **Annotated code.** [`example.py`](learning/code/ex-26-chunk-size-tradeoff/example.py). **Key takeaway.** Size is a retrieval parameter. **Why it matters.** Tune it against real queries.

### Example 27: Vector Store Index

**Brief explanation.** A vector index makes top-k similarity search queryable. **Diagram.** `vectors → index → neighbors`. **Annotated code.** [`example.py`](learning/code/ex-27-vector-store-index/example.py). **Key takeaway.** Indexes turn vectors into retrieval. **Why it matters.** Query performance is part of RAG quality.

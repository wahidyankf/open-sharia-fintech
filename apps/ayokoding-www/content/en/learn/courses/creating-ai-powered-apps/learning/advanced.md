---
title: "Advanced Examples"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 30
---

Examples 56–80 use deterministic local fixtures for operations, safety, framework boundaries,
providers, observability, and secrets. Run each artifact with `python3 example.py` from its directory.

### Example 56: Batch Processing

**Brief explanation**: A batch groups independent work to trade per-item latency for throughput and cost.
**Code**: `python3 learning/code/ex-56-batch-processing/example.py`
**Expected observation**: the fixture groups records into a bounded batch.
**Key takeaway**: batch only work whose delayed result is acceptable.
**Why it matters**: batching can lower cost without silently violating an interactive latency promise.

### Example 57: Read Rate-Limit Headers

**Brief explanation**: Provider headers expose remaining quota and the reset boundary for future calls.
**Code**: `python3 learning/code/ex-57-rate-limit-headers/example.py`
**Expected observation**: the fixture parses quota metadata into a local decision.
**Key takeaway**: make provider limits part of application control flow.
**Why it matters**: ignoring quota converts predictable backpressure into user-visible failures.

### Example 58: Exponential Backoff

**Brief explanation**: A retry delay increases after a transient failure while staying within a fixed budget.
**Code**: `python3 learning/code/ex-58-exponential-backoff/example.py`
**Expected observation**: the fixture produces increasing bounded retry delays.
**Key takeaway**: retry timing must be finite, observable, and operation-specific.
**Why it matters**: immediate retries can amplify an already overloaded provider.

### Example 59: Token Bucket

**Brief explanation**: A token bucket admits work only while an explicit local capacity token remains.
**Code**: `python3 learning/code/ex-59-token-bucket/example.py`
**Expected observation**: the fixture accepts work until its bucket is empty.
**Key takeaway**: backpressure belongs in the application, not only at the provider edge.
**Why it matters**: bounded admission protects cost, latency, and downstream reliability.

### Example 60: Moderate an Input

**Brief explanation**: Classify user input before it reaches a generative operation.
**Code**: `python3 learning/code/ex-60-moderation-endpoint/example.py`
**Expected observation**: the local moderation fixture returns an allow or block decision.
**Key takeaway**: moderation is a boundary check, not a post-hoc cleanup step.
**Why it matters**: unsafe input can influence tools, retrieval, and later user-visible output.

### Example 61: Inspect Moderation Categories

**Brief explanation**: A moderation decision should retain the category that drove it for review.
**Code**: `python3 learning/code/ex-61-moderation-categories/example.py`
**Expected observation**: the fixture identifies its matched safety category.
**Key takeaway**: keep category evidence separate from the content itself.
**Why it matters**: category-level signals make policy tuning and appeals possible.

### Example 62: Recognize Direct Prompt Injection

**Brief explanation**: Directly supplied instructions can attempt to override the application's policy.
**Code**: `python3 learning/code/ex-62-prompt-injection-direct/example.py`
**Expected observation**: the local guard marks the override-shaped instruction as untrusted.
**Key takeaway**: user text is data, never authority to replace system policy.
**Why it matters**: an injected instruction can redirect model behavior or tool selection.

### Example 63: Recognize Indirect Prompt Injection

**Brief explanation**: Retrieved documents can contain instructions that are untrusted data too.
**Code**: `python3 learning/code/ex-63-prompt-injection-indirect/example.py`
**Expected observation**: the fixture distinguishes document content from application instructions.
**Key takeaway**: retrieval does not grant a document control-plane authority.
**Why it matters**: indirect injection can arrive through otherwise useful external content.

### Example 64: Apply an Injection Guard

**Brief explanation**: A guard separates trusted task instructions from untrusted retrieved text.
**Code**: `python3 learning/code/ex-64-injection-guard/example.py`
**Expected observation**: the fixture preserves the trusted task while isolating unsafe content.
**Key takeaway**: make trust boundaries explicit in the prompt assembly path.
**Why it matters**: implicit trust assumptions are difficult to test and audit.

### Example 65: Test an Injection Corpus

**Brief explanation**: A corpus turns known injection patterns into repeatable safety regression tests.
**Code**: `python3 learning/code/ex-65-injection-corpus-test/example.py`
**Expected observation**: the local cases produce the expected guard decisions.
**Key takeaway**: test hostile inputs as deliberately as happy-path prompts.
**Why it matters**: a safety rule that is not regression-tested will drift.

### Example 66: Map OWASP LLM01

**Brief explanation**: Prompt injection is a named application risk with a concrete control boundary.
**Code**: `python3 learning/code/ex-66-owasp-llm01/example.py`
**Expected observation**: the fixture maps an unsafe instruction to its policy handling.
**Key takeaway**: connect threat vocabulary to executable controls.
**Why it matters**: a shared risk name helps teams review the right failure modes.

### Example 67: Redact PII

**Brief explanation**: Remove personal identifiers before a request crosses a model or log boundary.
**Code**: `python3 learning/code/ex-67-pii-redaction/example.py`
**Expected observation**: the fixture emits a redacted representation.
**Key takeaway**: minimize data before sending, storing, or tracing it.
**Why it matters**: prompts and traces can otherwise expose personal data unnecessarily.

### Example 68: Validate Output

**Brief explanation**: Validate model output against an expected application shape before use.
**Code**: `python3 learning/code/ex-68-output-validation/example.py`
**Expected observation**: the fixture accepts only a valid structured result.
**Key takeaway**: model text is untrusted until the application validates it.
**Why it matters**: downstream code needs a stable contract, not plausible prose.

### Example 69: Encode Output for Downstream Use

**Brief explanation**: Encode or escape model-derived data at the boundary where a renderer consumes it.
**Code**: `python3 learning/code/ex-69-output-encoding-downstream/example.py`
**Expected observation**: the fixture produces a safe downstream representation.
**Key takeaway**: output safety depends on the sink, not just the model response.
**Why it matters**: unencoded output can become an injection vector in another system.

### Example 70: Keep a LangChain Boundary

**Brief explanation**: A framework adapter should not own business policy or provider identity.
**Code**: `python3 learning/code/ex-70-langchain-abstraction/example.py`
**Expected observation**: the fixture keeps application policy outside the adapter.
**Key takeaway**: use frameworks behind ports that the application controls.
**Why it matters**: a provider/framework swap should not rewrite safety and product logic.

### Example 71: Keep a LlamaIndex Boundary

**Brief explanation**: Retrieval-framework integration should return application-facing data, not framework state.
**Code**: `python3 learning/code/ex-71-llamaindex-abstraction/example.py`
**Expected observation**: the fixture exposes a narrow retrieval result contract.
**Key takeaway**: isolate third-party abstractions at an adapter boundary.
**Why it matters**: framework details otherwise leak across the codebase.

### Example 72: Keep a Vercel AI SDK Boundary

**Brief explanation**: Streaming helpers are useful only when their provider-specific behavior stays contained.
**Code**: `python3 learning/code/ex-72-vercel-ai-sdk/example.py`
**Expected observation**: the fixture maps SDK output to an application result.
**Key takeaway**: own the application contract even when a framework owns the transport.
**Why it matters**: provider evolution should not become a product-wide migration.

### Example 73: Swap Providers Behind an Interface

**Brief explanation**: A stable interface makes a provider choice an implementation decision.
**Code**: `python3 learning/code/ex-73-provider-swap/example.py`
**Expected observation**: two fixture providers satisfy the same application contract.
**Key takeaway**: define what the product needs before selecting a provider.
**Why it matters**: switching providers is safer when behavior is tested at the port.

### Example 74: Pin a Model Identifier

**Brief explanation**: Pinning makes a model choice explicit and reproducible for an evaluation run.
**Code**: `python3 learning/code/ex-74-model-id-pinned/example.py`
**Expected observation**: the fixture records a single immutable model id.
**Key takeaway**: treat model selection as a versioned dependency decision.
**Why it matters**: silent model changes can invalidate cost and quality conclusions.

### Example 75: Trace Spans

**Brief explanation**: A trace span connects one model operation to timing and outcome evidence.
**Code**: `python3 learning/code/ex-75-tracing-spans/example.py`
**Expected observation**: the fixture emits a parent/child operation relationship.
**Key takeaway**: trace the boundary where an AI call affects user-visible work.
**Why it matters**: latency and failure diagnosis need more than a final response string.

### Example 76: Observe an Evaluation Loop

**Brief explanation**: An evaluation loop should emit observations without pretending it replaces deeper eval design.
**Code**: `python3 learning/code/ex-76-observability-eval-loop/example.py`
**Expected observation**: the fixture records a result suitable for a later evaluation decision.
**Key takeaway**: observability supplies evidence; evaluation defines what success means.
**Why it matters**: a trace alone cannot prove model quality or safety.

### Example 77: Read an API Key from the Environment

**Brief explanation**: Runtime configuration reads a key from the environment rather than a tracked file.
**Code**: `python3 learning/code/ex-77-api-key-env/example.py`
**Expected observation**: the fixture demonstrates the environment-only configuration seam.
**Key takeaway**: never commit a real key or put it in course prose.
**Why it matters**: version-control history is permanent and shared.

### Example 78: Use a No-Key Mock

**Brief explanation**: An offline mock lets tests exercise application behavior without provider access.
**Code**: `python3 learning/code/ex-78-no-key-required-mock/example.py`
**Expected observation**: the fixture produces a deterministic response with no credential.
**Key takeaway**: maintain a no-key seam for local tests and examples.
**Why it matters**: tests must remain reproducible when network or credentials are unavailable.

### Example 79: Normalize Responses and Chat Shapes

**Brief explanation**: Provider response formats differ, so normalize them at the integration boundary.
**Code**: `python3 learning/code/ex-79-responses-vs-chat/example.py`
**Expected observation**: the fixture maps two response forms to one application value.
**Key takeaway**: consume an application-owned result type, not a provider response object.
**Why it matters**: provider API changes should not ripple through business logic.

### Example 80: Compose the Guarded AI App Capstone

**Brief explanation**: The capstone combines validated input, guarded retrieval, bounded calls, and safe output.
**Code**: `python3 learning/code/ex-80-aiapp-capstone/example.py`
**Expected observation**: the offline fixture completes one guarded application flow.
**Key takeaway**: useful AI features emerge from explicit product and safety boundaries.
**Why it matters**: a production AI app is more than one successful model request.

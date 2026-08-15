---
title: "Retrieval-Augmented Context"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 30
---

Theme C is the source-defined retrieval level: Examples 23–34. Each entry has brief purpose, a compact
pipeline diagram, annotated local artifact, takeaway, and production boundary.

| Example                       | Brief / diagram                                       | Artifact                                                      | Key takeaway                                         |
| ----------------------------- | ----------------------------------------------------- | ------------------------------------------------------------- | ---------------------------------------------------- | -------------------------- |
| 23. Embed text                | `text → vector`                                       | [ex-23](code/ex-23-embed-text/example.py)                     | Record vector dimension.                             |
| 24. Similarity search         | `query → nearest`                                     | [ex-24](code/ex-24-similarity-search/example.py)              | Top hit must be relevant.                            |
| 25. Build vector store        | `docs → index`                                        | [ex-25](code/ex-25-build-a-vector-store/example.py)           | Indexing precedes retrieval.                         |
| 26. Chunking contrast         | `sizes → recall`                                      | [ex-26](code/ex-26-chunking-strategy-contrast/example.py)     | Chunking changes recall.                             |
| 27. Retrieve into context     | `top-k → prompt`                                      | [ex-27](code/ex-27-retrieve-into-context/example.py)          | Add relevant evidence only.                          |
| 28. Rerank candidates         | `candidates → rank`                                   | [ex-28](code/ex-28-rerank-candidates/example.py)              | Rank before inclusion.                               |
| 29. Relevance threshold       | `score → keep/drop`                                   | [ex-29](code/ex-29-relevance-threshold/example.py)            | Exclude noise.                                       |
| 30. Retrieval vs stuffing     | `RAG                                                  | full corpus`                                                  | [ex-30](code/ex-30-retrieval-vs-stuffing/example.py) | Choose by corpus and task. |
| 31. Citation retrieved source | `chunk → citation`                                    | [ex-31](code/ex-31-citation-of-retrieved-source/example.py)   | Preserve provenance.                                 |
| 32. Retrieval in loop         | `turn → retrieve → context`                           | [ex-32](code/ex-32-retrieval-in-the-loop/example.py)          | Refresh relevant context per turn.                   |
| 33. Stale index refresh       | `source change → reindex`                             | [ex-33](code/ex-33-stale-index-refresh/example.py)            | Retrieval freshness is operational.                  |
| 34. Retrieval architecture    | `chunk → embed → store → retrieve → rerank → context` | [ex-34](code/ex-34-retrieval-architecture-diagram/example.py) | Make pipeline stages visible.                        |

## Theme D · Memory and cache-aware assembly

Theme D is the source-defined memory level: Examples 35–48. Each exercise keeps its data local and
models the decision rule, not an external memory service.

### Example 35 · Short-term scratchpad

**Brief.** Preserve intermediate notes for the current session only.

**Diagram.** `turn → scratchpad → next turn`

**Artifact.** Run [ex-35](code/ex-35-short-term-scratchpad/example.py).

**Key takeaway.** Session notes may guide later turns without becoming durable facts.

**Production boundary.** Scope scratchpads to a session and expire them deliberately.

### Example 36 · Persist long-term memory

**Brief.** Save a useful fact so a new session can recall it.

**Diagram.** `session A → memory store → session B`

**Artifact.** Run [ex-36](code/ex-36-persist-long-term-memory/example.py).

**Key takeaway.** Persistence crosses a session boundary; a scratchpad does not.

**Production boundary.** Give durable records an owner, retention rule, and review path.

### Example 37 · Memory write policy

**Brief.** Store durable preferences while rejecting conversational noise.

**Diagram.** `session facts → policy → remember | discard`

**Artifact.** Run [ex-37](code/ex-37-memory-write-policy/example.py).

**Key takeaway.** A write policy prevents memory from becoming an untrusted transcript.

**Production boundary.** Make policy reasons inspectable before writing user-derived data.

### Example 38 · Memory retrieval policy

**Brief.** Recall only the memories relevant to a current task.

**Diagram.** `task + memories → filter → context`

**Artifact.** Run [ex-38](code/ex-38-memory-retrieval-policy/example.py).

**Key takeaway.** Irrelevant memories consume budget and can steer an answer wrongly.

**Production boundary.** Apply relevance filtering before a memory reaches model context.

### Example 39 · Memory staleness

**Brief.** Replace an old stored value with a corrected one.

**Diagram.** `observed correction → stale check → updated fact`

**Artifact.** Run [ex-39](code/ex-39-memory-staleness/example.py).

**Key takeaway.** Recall must prefer a corrected value over a familiar old value.

**Production boundary.** Track freshness evidence and offer a correction workflow.

### Example 40 · Memory conflict resolution

**Brief.** Resolve conflicting facts with a defined, reproducible rule.

**Diagram.** `fact A + fact B → resolver → selected fact`

**Artifact.** Run [ex-40](code/ex-40-memory-conflict-resolution/example.py).

**Key takeaway.** An explicit resolution rule is safer than accidental last-write-wins behavior.

**Production boundary.** Preserve conflict provenance for audit and correction.

### Example 41 · Memory privacy gate

**Brief.** Refuse to persist secrets or personally identifying information.

**Diagram.** `candidate fact → privacy gate → reject | store`

**Artifact.** Run [ex-41](code/ex-41-memory-privacy-gate/example.py).

**Key takeaway.** Privacy filtering belongs before persistence, not only at retrieval.

**Production boundary.** Combine deterministic gates with escalation for ambiguous cases.

### Example 42 · Memory-backed agent task

**Brief.** Use a saved preference to personalize a task outcome.

**Diagram.** `task + relevant preference → tailored result`

**Artifact.** Run [ex-42](code/ex-42-memory-backed-agent-task/example.py).

**Key takeaway.** Personalization is observable: the saved memory changes the result.

**Production boundary.** Reveal and let people revise the preference used for personalization.

### Example 43 · Short versus long memory diagram

**Brief.** Separate session state from persisted memory visually.

**Diagram.** `session scratchpad ⇢ ephemeral; memory store ⇢ durable`

**Artifact.** Run [ex-43](code/ex-43-short-vs-long-memory-diagram/example.py).

**Key takeaway.** Lifetime is the key distinction, even when both hold text.

**Production boundary.** Document expiry, access, and deletion separately for each store.

### Example 44 · Full context pipeline

**Brief.** Budget system, task, long-term memory, retrieval, and rolling history together.

**Diagram.** `system + task + memory + retrieval + history → budgeted context`

**Artifact.** Run [ex-44](code/ex-44-full-context-pipeline/example.py).

**Key takeaway.** Relevance and budget are simultaneous constraints on assembly.

**Production boundary.** Measure component budgets and reject overflow before invoking a model.

### Example 45 · Memory audit

**Brief.** Report stale and private material retained by a memory store.

**Diagram.** `stored memories → audit → findings`

**Artifact.** Run [ex-45](code/ex-45-memory-audit/example.py).

**Key takeaway.** Memory needs periodic operational review, not only write-time policy.

**Production boundary.** Route audit findings to correction, deletion, or human review.

### Example 46 · Order by staleness, not grouping

**Brief.** Put stable context before variable values to retain a reusable prefix.

**Diagram.** `stable system/tools/corpus → recent turns/live results`

**Artifact.** Run [ex-46](code/ex-46-order-by-staleness-not-grouping/example.py).

**Key takeaway.** Stable-before-variable ordering keeps consecutive prefixes byte-identical.

**Production boundary.** Treat cache-friendly ordering as an assembly concern, not a correctness proof.

### Example 47 · One volatile field destroys the prefix

**Brief.** Move a timestamp from the prefix to the tail and compare reuse.

**Diagram.** `volatile prefix → no reuse; volatile tail → stable prefix`

**Artifact.** Run [ex-47](code/ex-47-one-volatile-field-destroys-the-prefix/example.py).

**Key takeaway.** Provider cache mechanics and answer accuracy are related but distinct concerns.

**Production boundary.** Measure provider-specific reuse separately from task-quality evaluation.

### Example 48 · Capstone context-managed agent

**Brief.** Combine budgeting, compaction, retrieval, memory, and stable ordering across sessions.

**Diagram.** `session → compact/retrieve/remember → budgeted stable context → next session`

**Artifact.** Run [ex-48](code/ex-48-capstone-context-managed-agent/example.py).

**Key takeaway.** Context management is a system of coordinated safeguards, not one prompt trick.

**Production boundary.** Exercise the complete flow with real policies, observability, and review.

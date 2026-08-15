---
title: "Intermediate Examples"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 20
---

Examples 17–34 compose local, typed MCP-shaped providers. Every artifact runs without a credential,
network listener, browser, or third-party package.

### Example 17: Build a Multi-Tool MCP Server

**Brief explanation**: A server can advertise focused read, write, and search capabilities.

**Code**: Run `python3 code/ex-17-multi-tool-mcp-server/example.py`.

**Expected observation**: All three local tools are callable.

**Key takeaway**: One provider may expose several explicit contracts.

**Why it matters**: A client can discover a bounded surface rather than bespoke integration code.

### Example 18: Model MCP over HTTP

**Brief explanation**: HTTP transports a JSON request to a remote-looking server boundary.

**Code**: Run `python3 code/ex-18-mcp-over-http/example.py`.

**Expected observation**: A local request receives a typed JSON response.

**Key takeaway**: Transport does not change tool semantics.

**Why it matters**: The same contracts can cross process boundaries.

### Example 19: Validate Arguments Server-Side

**Brief explanation**: The server rejects malformed calls even when a client claims they are valid.

**Code**: Run `python3 code/ex-19-argument-validation-server-side/example.py`.

**Expected observation**: A bad `limit` returns a typed error.

**Key takeaway**: The executable boundary owns validation.

**Why it matters**: Client-side checks alone cannot protect a real action.

### Example 20: Compose Two Servers

**Brief explanation**: A client can combine capabilities from distinct local providers.

**Code**: Run `python3 code/ex-20-compose-two-servers/example.py`.

**Expected observation**: The composed client reads both server outputs.

**Key takeaway**: MCP composes providers rather than merging implementations.

**Why it matters**: Teams can publish independent capabilities.

### Example 21: Namespace Tools

**Brief explanation**: A server-qualified name prevents collisions between tools with the same short name.

**Code**: Run `python3 code/ex-21-tool-namespacing/example.py`.

**Expected observation**: `notes.search` and `docs.search` remain distinct.

**Key takeaway**: Namespaces preserve the provider boundary.

**Why it matters**: An ambiguous call can route work to the wrong authority.

### Example 22: Load a Resource into Context

**Brief explanation**: A resource becomes read-only context before a task decision.

**Code**: Run `python3 code/ex-22-resource-into-context/example.py`.

**Expected observation**: The task uses the loaded local policy.

**Key takeaway**: Resources enrich a loop without becoming actions.

**Why it matters**: A reader can reason from provider data with less authority.

### Example 23: Reuse a Prompt Template

**Brief explanation**: A client fetches a parameterized server prompt for repeated task framing.

**Code**: Run `python3 code/ex-23-prompt-template-reuse/example.py`.

**Expected observation**: The same template renders two task values.

**Key takeaway**: Prompt templates are reusable capability metadata.

**Why it matters**: Shared framing avoids copy-and-paste drift.

### Example 24: Bound a Filesystem Tool

**Brief explanation**: A file path must remain below an authorized sandbox directory.

**Code**: Run `python3 code/ex-24-fs-tool-with-bounds/example.py`.

**Expected observation**: An out-of-bounds path is rejected.

**Key takeaway**: A useful tool should still have a small authority boundary.

**Why it matters**: Path traversal must not escape the designated workspace.

### Example 25: Gate a Shell Tool

**Brief explanation**: A shell-shaped tool accepts a small allow-list rather than arbitrary commands.

**Code**: Run `python3 code/ex-25-shell-tool-gated/example.py`.

**Expected observation**: `status` is allowed and `rm` is blocked.

**Key takeaway**: A model request is never permission to run a command.

**Why it matters**: Shell authority has a high blast radius.

### Example 26: Version a Tool Schema

**Brief explanation**: An additive optional field keeps old and new callers compatible.

**Code**: Run `python3 code/ex-26-versioned-tool-schema/example.py`.

**Expected observation**: Both input versions return a greeting.

**Key takeaway**: Compatibility is a contract design choice.

**Why it matters**: Tool changes should not silently break an existing agent.

### Example 27: Truncate a Tool Result

**Brief explanation**: A long result is bounded and marked as truncated before entering context.

**Code**: Run `python3 code/ex-27-tool-result-truncation/example.py`.

**Expected observation**: The result carries `truncated: True`.

**Key takeaway**: Result shape is a context-budget decision.

**Why it matters**: Large unused payloads consume tokens on later turns.

### Example 28: Merge Concurrent MCP Calls

**Brief explanation**: Independent calls can run concurrently and merge typed observations.

**Code**: Run `python3 code/ex-28-concurrent-mcp-calls/example.py`.

**Expected observation**: Both local results arrive in one merged mapping.

**Key takeaway**: Concurrency needs correlation and a deterministic merge.

**Why it matters**: Parallel calls reduce waiting without confusing result ownership.

### Example 29: Recover from a Server Error

**Brief explanation**: A failure becomes an observation that lets the client choose a fallback.

**Code**: Run `python3 code/ex-29-server-error-recovery/example.py`.

**Expected observation**: A fallback result follows the typed error.

**Key takeaway**: Error results enable deliberate recovery.

**Why it matters**: A transient provider failure should not become an opaque loop crash.

### Example 30: Test MCP Deterministically

**Brief explanation**: A fake client and local server make an MCP contract test repeatable.

**Code**: Run `python3 code/ex-30-deterministic-mcp-tests/example.py`.

**Expected observation**: The assertion passes without a live service.

**Key takeaway**: Fakes turn protocol behavior into testable local state.

**Why it matters**: Credential-dependent tests are slow and nondeterministic.

### Example 31: Describe for the Model

**Brief explanation**: A revised description gives a selector enough evidence to choose the intended tool.

**Code**: Run `python3 code/ex-31-describe-for-the-model/example.py`.

**Expected observation**: The precise description wins the fake selection.

**Key takeaway**: Improve the contract before adding selection workarounds.

**Why it matters**: Description quality directly affects call accuracy.

### Example 32: Build a Schema-Driven Client

**Brief explanation**: The client constructs a call from discovered field definitions rather than a local stub.

**Code**: Run `python3 code/ex-32-schema-driven-client/example.py`.

**Expected observation**: The generated call contains the discovered `city` field.

**Key takeaway**: Discovery can drive call construction.

**Why it matters**: Server schema evolution need not require duplicate client shapes.

### Example 33: List and Read Resources

**Brief explanation**: A client enumerates several resources and reads each by its URI.

**Code**: Run `python3 code/ex-33-resource-listing-and-read/example.py`.

**Expected observation**: Both local resource texts are returned.

**Key takeaway**: Listing and reading are separate operations.

**Why it matters**: Resource discovery lets a client request only relevant context.

### Example 34: Inspect an MCP Server

**Brief explanation**: An inspector reports tools, resources, and prompts advertised by a provider.

**Code**: Run `python3 code/ex-34-mcp-inspector-check/example.py`.

**Expected observation**: The report lists every capability category.

**Key takeaway**: Inspection verifies what a server actually exposes.

**Why it matters**: A deployment review must see capabilities before an agent receives them.
